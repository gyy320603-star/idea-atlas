#!/usr/bin/env python3
"""Build and verify a WorkBuddy marketplace ZIP with Python 3.8+.

The package adds marketplace frontmatter and flattens its bundled example paths
for WorkBuddy's two-directory limit. Canonical source files stay unchanged.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile

from package_release import ROOT, SKILL, skill_version, write_zip


METADATA = ROOT / "integrations" / "workbuddy" / "skill-metadata.json"
TEXT_FIELDS = ("display_name", "display_name_en", "description_zh", "description_en")
EXAMPLE_FIELDS = ("examples_zh", "examples_en")
REQUIRED_FIELDS = ("name", "description") + TEXT_FIELDS + ("version", "author")
FLAT_EXAMPLES = {
    SKILL + "/examples/sideboard/" + filename:
    SKILL + "/examples/sideboard-" + filename
    for filename in ("atlas-data.json", "atlas.html", "preview.png")
}
CANVAS_REFERENCE = SKILL + "/references/canvas-data.md"


def flatten_reference(data):
    for original, flattened in FLAT_EXAMPLES.items():
        data = data.replace(original[len(SKILL) + 1:].encode("utf-8"),
                            flattened[len(SKILL) + 1:].encode("utf-8"))
    return data


def marketplace_files(source_files):
    missing = set(FLAT_EXAMPLES) - set(source_files)
    if missing:
        raise ValueError("Missing bundled example files: " + ", ".join(sorted(missing)))
    entries = {}
    for name, data in source_files.items():
        destination = FLAT_EXAMPLES.get(name, name)
        if len(Path(destination).parts) > 3:
            raise ValueError("WorkBuddy directory depth exceeded: " + destination)
        if destination in entries:
            raise ValueError("Duplicate flattened path: " + destination)
        entries[destination] = flatten_reference(data) if name == CANVAS_REFERENCE else data
    return entries


def digest(data):
    return hashlib.sha256(data).hexdigest()


def split_skill(data):
    if not data.startswith(b"---\n") or b"\n---\n" not in data[4:]:
        raise ValueError("SKILL.md must start with YAML frontmatter")
    return data[4:].split(b"\n---\n", 1)


def marketplace_skill(source, metadata, version):
    frontmatter, body = split_skill(source)
    text = frontmatter.decode("utf-8")
    expected_keys = set(TEXT_FIELDS + EXAMPLE_FIELDS)
    if set(metadata) != expected_keys:
        raise ValueError("Market metadata must contain: " + ", ".join(sorted(expected_keys)))
    for key in TEXT_FIELDS:
        if not isinstance(metadata[key], str) or not metadata[key].strip():
            raise ValueError(key + " must be nonempty text")
    for key in EXAMPLE_FIELDS:
        if not isinstance(metadata[key], list) or not metadata[key] or any(
                not isinstance(item, str) or not item.strip() for item in metadata[key]):
            raise ValueError(key + " must be a nonempty list of prompts")
    if not re.search(r"^name: " + re.escape(SKILL) + r"$", text, re.M):
        raise ValueError("Unexpected canonical skill name")
    author_match = re.search(r"^  author: (.+)$", text, re.M)
    if not author_match:
        raise ValueError("Missing metadata.author in canonical skill")
    author = author_match.group(1).strip()
    if author.startswith('"'):
        author = json.loads(author)
    elif author.startswith("'") and author.endswith("'"):
        author = author[1:-1].replace("''", "'")
    extra = dict(metadata, version=version, author=author)
    for key in extra:
        if re.search(r"^" + re.escape(key) + r":", text, re.M):
            raise ValueError("Canonical skill already defines market field " + key)
    # JSON-quoted scalars and arrays are valid YAML, without a PyYAML dependency.
    added = "\n".join(key + ": " + json.dumps(value, ensure_ascii=False)
                      for key, value in extra.items())
    result = b"---\n" + frontmatter + b"\n" + added.encode("utf-8") + b"\n---\n" + body
    packaged_frontmatter, packaged_body = split_skill(result)
    for key in REQUIRED_FIELDS:
        if not re.search(rb"^" + key.encode("ascii") + rb":\s*\S", packaged_frontmatter, re.M):
            raise ValueError("Missing WorkBuddy field " + key)
    if packaged_body != body:
        raise ValueError("The instruction body changed")
    return result


def runtime_files():
    files = {}
    for path in sorted((ROOT / SKILL).rglob("*")):
        relative = path.relative_to(ROOT / SKILL)
        if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
            continue
        if relative.parts[0] == "tests" or path.suffix in (".pyc", ".pyo"):
            continue
        if path.is_symlink():
            raise ValueError("Unexpected symlink: " + str(path))
        if path.is_file():
            files[SKILL + "/" + relative.as_posix()] = path.read_bytes()
    return files


def verify_archive(archive_path, source_files, entries):
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(entries):
            raise ValueError("ZIP contents failed verification")
        if any(len(Path(name).parts) > 3 for name in archive.namelist()):
            raise ValueError("ZIP exceeds WorkBuddy's root/subdirectory/file limit")
        for name, data in entries.items():
            if archive.read(name) != data:
                raise ValueError("ZIP bytes differ for " + name)
        with tempfile.TemporaryDirectory(prefix="idea-atlas-workbuddy-") as temporary:
            unpacked = Path(temporary)
            archive.extractall(unpacked)
            renderer = unpacked / SKILL / "scripts" / "render_canvas.py"
            cases = []
            inputs = [(case, ROOT / "docs" / case / "zh.json")
                      for case in ("cow-shoes", "sideboard")]
            inputs.append(("bundled-sideboard", unpacked / SKILL / "examples" /
                           "sideboard-atlas-data.json"))
            for case, manifest in inputs:
                output = unpacked / (case + ".html")
                subprocess.run([sys.executable, str(renderer), str(manifest), str(output)],
                               cwd=unpacked, check=True, capture_output=True, text=True)
                data = json.loads(manifest.read_text(encoding="utf-8"))
                html = output.read_text(encoding="utf-8")
                match = re.search(r'<script type="application/json" id="atlasData">(.*?)</script>',
                                  html, re.S)
                if not match:
                    raise ValueError("Rendered HTML has no embedded manifest")
                if json.loads(match.group(1)) != {key: value for key, value in data.items()
                                                 if key != "translations"}:
                    raise ValueError("Rendered HTML does not preserve source records")
                canonical_manifest = (ROOT / SKILL / "examples" / "sideboard" / "atlas-data.json"
                                      if case == "bundled-sideboard" else manifest)
                canonical_output = unpacked / (case + "-canonical.html")
                subprocess.run([sys.executable, str(ROOT / SKILL / "scripts" / "render_canvas.py"),
                                str(canonical_manifest), str(canonical_output)], cwd=unpacked,
                               check=True, capture_output=True, text=True)
                if output.read_bytes() != canonical_output.read_bytes():
                    raise ValueError("Packaged renderer differs from canonical output: " + case)
                cases.append({"case": case, "branches": len(data.get("readings") or data["lenses"]),
                              "cards": len(data["cards"]), "html_sha256": digest(output.read_bytes()),
                              "source_records_preserved": True, "matches_canonical_renderer": True})
    skill_path = SKILL + "/SKILL.md"
    if split_skill(source_files[skill_path])[1] != split_skill(entries[skill_path])[1]:
        raise ValueError("Packaged instructions differ from canonical instructions")
    for name, data in source_files.items():
        if name == skill_path:
            continue
        destination = FLAT_EXAMPLES.get(name, name)
        expected = flatten_reference(data) if name == CANVAS_REFERENCE else data
        if expected != entries[destination]:
            raise ValueError("Unapproved package adaptation: " + name)
    if set(entries) != {FLAT_EXAMPLES.get(name, name) for name in source_files}:
        raise ValueError("Unexpected packaged file paths")
    return cases


def build(output):
    source_files = runtime_files()
    skill_path = SKILL + "/SKILL.md"
    metadata = json.loads(METADATA.read_text(encoding="utf-8"))
    version = skill_version(ROOT / SKILL)
    entries = marketplace_files(source_files)
    entries[skill_path] = marketplace_skill(source_files[skill_path], metadata, version)
    output.mkdir(parents=True, exist_ok=True)
    basename = SKILL + "-workbuddy-" + version
    with tempfile.TemporaryDirectory(dir=output) as temporary:
        archive = Path(temporary) / (basename + ".zip")
        write_zip(archive, entries)
        cases = verify_archive(archive, source_files, entries)
        archive_hash = digest(archive.read_bytes())
        report = {
            "package": SKILL, "target": "workbuddy", "version": version,
            "requirements_source": "https://open.workbuddy.cn/docs/skill",
            "archive": archive.name, "archive_bytes": archive.stat().st_size,
            "archive_sha256": archive_hash, "required_fields": list(REQUIRED_FIELDS),
            "checks": {"single_skill_root": True, "zip_crc": True,
                       "maximum_path_depth": 3, "directory_depth_within_limit": True,
                       "marketplace_fields_present": True, "instruction_body_unchanged": True,
                       "only_declared_path_adaptations": True,
                       "renderer_and_example_data_unchanged": True,
                       "rendered_html_matches_canonical": True,
                       "extracted_renderer_passed": True},
            "canonical_skill_sha256": digest(source_files[skill_path]),
            "instruction_body_sha256": digest(split_skill(source_files[skill_path])[1]),
            "excluded": ["tests/", "hidden files", "__pycache__/", "*.pyc", "*.pyo"],
            "path_adaptations": {"moved_files": FLAT_EXAMPLES,
                                 "updated_reference": CANVAS_REFERENCE,
                                 "change": "Replace bundled example paths only"},
            "render_checks": cases,
            "limits": ["Local package and renderer checks only; not a WorkBuddy marketplace approval.",
                       "Existing source cases are rendered, not newly generated by WorkBuddy."],
            "files": [{"path": name, "bytes": len(data), "sha256": digest(data)}
                      for name, data in sorted(entries.items())],
        }
        destination = output / archive.name
        os.replace(archive, destination)
    (output / (basename + ".verification.json")).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / (basename + ".sha256")).write_text(
        archive_hash + "  " + destination.name + "\n", encoding="utf-8")
    print(destination)
    print("Verified %s files; directory depth <= 3; two demo cases and the bundled example preserved."
          % len(entries))
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist" / "workbuddy")
    build(parser.parse_args().out.resolve())
