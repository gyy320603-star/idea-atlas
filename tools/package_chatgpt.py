#!/usr/bin/env python3
"""Build and verify an Idea Atlas skills-only ChatGPT plugin with Python 3.8+."""

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import struct
import subprocess
import sys
import tempfile
from urllib.parse import urlsplit
import zipfile

from package_release import ROOT, SKILL, skill_version, write_zip


INTEGRATION = ROOT / "integrations" / "chatgpt"
SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
AUTHOR = "yuyang gong（龚雨旸）"
SKILL_PREFIX = "skills/" + SKILL + "/"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def text_field(owner, key, limit):
    value = owner.get(key)
    if not isinstance(value, str) or not value.strip() or len(value) > limit:
        raise ValueError("Invalid or overlong field: " + key)
    if any(ord(char) < 32 and char != "\n" for char in value):
        raise ValueError("Control character in " + key)
    return value


def https_field(owner, key, limit):
    value = text_field(owner, key, limit)
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.netloc or parsed.username or parsed.password:
        raise ValueError("Expected a public HTTPS URL for " + key)


def verify_manifest(manifest, entries):
    if manifest.get("$schema") != SCHEMA or manifest.get("name") != SKILL:
        raise ValueError("Unexpected portable plugin identity")
    text_field(manifest, "name", 64)
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", manifest["name"]):
        raise ValueError("Invalid plugin name")
    if manifest.get("version") != skill_version(ROOT / SKILL):
        raise ValueError("Plugin and skill versions differ")
    text_field(manifest, "description", 4000)
    if manifest.get("author", {}).get("name") != AUTHOR:
        raise ValueError("Unexpected author")
    text_field(manifest["author"], "name", 120)
    https_field(manifest["author"], "url", 2048)
    https_field(manifest, "homepage", 2048)
    https_field(manifest, "repository", 2048)
    extension = manifest.get("extensions", {}).get("com.openai", {})
    if any(key in extension for key in ("apps", "hooks", "mcpServers")):
        raise ValueError("This package must contain skills only")
    review = extension.get("review", {})
    if not isinstance(review, dict) or set(review) - {"prompts"}:
        raise ValueError("This skills-only package supports review prompts only")
    review_prompts = review.get("prompts", [])
    if not isinstance(review_prompts, list) or len(review_prompts) > 20:
        raise ValueError("Provide at most 20 review prompts")
    for prompt in review_prompts:
        text_field({"prompt": prompt}, "prompt", 4000)
    publication = extension.get("publication", {})
    if not isinstance(publication, dict):
        raise ValueError("Publication metadata must be an object")
    if "release_notes" in publication:
        text_field(publication, "release_notes", 4000)
    for locale, translated in publication.get("translations", {}).items():
        if not isinstance(locale, str) or not locale.strip() or not isinstance(translated, dict):
            raise ValueError("Invalid listing translation")
        if "subtitle" in translated:
            text_field(translated, "subtitle", 30)
        if "description" in translated:
            text_field(translated, "description", 4000)
    interface = extension.get("interface", {})
    limits = {"displayName": 30, "shortDescription": 30,
              "longDescription": 4000, "developerName": 80}
    for key, limit in limits.items():
        text_field(interface, key, limit)
    if interface["developerName"] != AUTHOR:
        raise ValueError("Developer name differs from author")
    if interface.get("category") not in (
            "Business & Operations", "Communication", "Creativity", "Data & Analytics",
            "Developer Tools", "Education & Research", "Entertainment", "Finance",
            "Healthcare", "Other", "Productivity", "Scientific Research", "Security", "Travel"):
        raise ValueError("Unsupported public directory category")
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        if key in interface:
            https_field(interface, key, 1024)
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3:
        raise ValueError("Provide one to three starter prompts")
    for prompt in prompts:
        text_field({"prompt": prompt}, "prompt", 128)
        if "@" in prompt or "\n" in prompt:
            raise ValueError("Starter prompts must be single-line and omit app @mentions")
    if len({" ".join(prompt.split()) for prompt in prompts}) != len(prompts):
        raise ValueError("Starter prompts must be unique")
    for key in ("logo", "composerIcon"):
        value = interface.get(key, "")
        path = PurePosixPath(value)
        if not value.startswith("./assets/") or ".." in path.parts:
            raise ValueError("Invalid asset reference: " + key)
        data = entries.get(path.as_posix())
        if not data or len(data) > 5 * 1024 * 1024:
            raise ValueError("Missing or oversized asset: " + value)
        if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
            raise ValueError("Expected a PNG icon")
        width, height = struct.unpack(">II", data[16:24])
        minimum = 256 if key == "logo" else 48
        if width != height or not minimum <= width <= 4096:
            raise ValueError("Icon dimensions do not meet the public listing requirements")
    if not re.fullmatch(r"#[0-9a-fA-F]{6}", interface.get("brandColor", "")):
        raise ValueError("Expected a six-digit brand color")
    return {key: {"length": len(interface[key]), "maximum": limit}
            for key, limit in limits.items()}


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
            files[SKILL_PREFIX + relative.as_posix()] = path.read_bytes()
    return files


def verify_archive(archive_path, entries, runtime):
    with zipfile.ZipFile(archive_path) as archive:
        if archive.testzip() is not None or set(archive.namelist()) != set(entries):
            raise ValueError("Archive contents failed verification")
        for name, data in entries.items():
            if archive.read(name) != data:
                raise ValueError("Archive bytes differ for " + name)
        if any(name in entries for name in ("mcp.json", ".mcp.json", ".app.json")):
            raise ValueError("Unexpected MCP or app configuration")
        with tempfile.TemporaryDirectory(prefix="idea-atlas-chatgpt-") as temporary:
            unpacked = Path(temporary)
            archive.extractall(unpacked)
            renderer = unpacked / SKILL_PREFIX / "scripts" / "render_canvas.py"
            checks = []
            for case in ("cow-shoes", "sideboard"):
                for language in ("en", "zh"):
                    manifest_path = ROOT / "docs" / case / (language + ".json")
                    output = unpacked / (case + "-" + language + ".html")
                    subprocess.run([sys.executable, str(renderer), str(manifest_path), str(output)],
                                   cwd=unpacked, check=True, capture_output=True, text=True)
                    html = output.read_text(encoding="utf-8")
                    source = json.loads(manifest_path.read_text(encoding="utf-8"))
                    embedded = re.search(
                        r'<script type="application/json" id="atlasData">(.*?)</script>', html, re.S)
                    if not embedded or json.loads(embedded.group(1)) != {
                            key: value for key, value in source.items() if key != "translations"}:
                        raise ValueError("Source records changed for " + case + "/" + language)
                    canonical = unpacked / (case + "-" + language + "-canonical.html")
                    subprocess.run([sys.executable, str(ROOT / SKILL / "scripts" / "render_canvas.py"),
                                    str(manifest_path), str(canonical)], cwd=unpacked, check=True,
                                   capture_output=True, text=True)
                    if output.read_bytes() != canonical.read_bytes():
                        raise ValueError("Packaged rendering differs from canonical output")
                    checks.append({"case": case, "language": language,
                                   "cards": len(source["cards"]),
                                   "source_records_preserved": True,
                                   "matches_canonical_renderer": True,
                                   "html_sha256": digest(output.read_bytes())})
    if any(entries.get(name) != data for name, data in runtime.items()):
        raise ValueError("Canonical runtime changed in the plugin")
    return checks


def build(output):
    manifest_data = (INTEGRATION / "plugin.json").read_bytes()
    manifest = json.loads(manifest_data)
    runtime = runtime_files()
    entries = dict(runtime)
    entries["plugin.json"] = manifest_data
    entries["LICENSE"] = (ROOT / "LICENSE").read_bytes()
    for path in sorted((INTEGRATION / "assets").rglob("*")):
        if path.is_symlink():
            raise ValueError("Unexpected asset symlink: " + str(path))
        if path.is_file() and not path.name.startswith("."):
            entries[path.relative_to(INTEGRATION).as_posix()] = path.read_bytes()
    field_lengths = verify_manifest(manifest, entries)
    output.mkdir(parents=True, exist_ok=True)
    basename = SKILL + "-chatgpt-" + manifest["version"]
    with tempfile.TemporaryDirectory(dir=output) as temporary:
        archive = Path(temporary) / (basename + ".zip")
        write_zip(archive, entries)
        render_checks = verify_archive(archive, entries, runtime)
        archive_hash = digest(archive.read_bytes())
        missing_links = [key for key in ("privacyPolicyURL", "termsOfServiceURL")
                         if not manifest["extensions"]["com.openai"]["interface"].get(key)]
        report = {
            "package": SKILL, "target": "chatgpt-skills-only-plugin",
            "version": manifest["version"], "archive": archive.name,
            "archive_bytes": archive.stat().st_size, "archive_sha256": archive_hash,
            "requirements_sources": ["https://developers.openai.com/plugins/build/plugins",
                                     "https://developers.openai.com/plugins/deploy/submission"],
            "checks": {"root_plugin_manifest": True, "zip_crc": True,
                       "all_canonical_runtime_bytes_preserved": True,
                       "referenced_icons_present_and_square": True,
                       "documented_listing_limits": True,
                       "four_extracted_renderer_checks": True},
            "field_lengths": field_lengths, "render_checks": render_checks,
            "publication_links_not_yet_set": missing_links,
            "limits": ["Local package checks; not a complete JSON Schema or platform validation.",
                       "Existing examples were rendered; new ChatGPT Work generation remains unverified.",
                       "No official directory upload, review or publication is implied.",
                       "Public URLs were checked syntactically, not for live availability."],
            "excluded": ["tests/", "hidden files", "__pycache__/", "*.pyc", "*.pyo"],
            "files": [{"path": name, "bytes": len(data), "sha256": digest(data)}
                      for name, data in sorted(entries.items())]
        }
        destination = output / archive.name
        os.replace(archive, destination)
    (output / (basename + ".verification.json")).write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (output / (basename + ".sha256")).write_text(
        archive_hash + "  " + destination.name + "\n", encoding="utf-8")
    print(destination)
    print("Verified %s files and four bilingual example renders; canonical runtime preserved."
          % len(entries))
    return destination


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist" / "chatgpt")
    build(parser.parse_args().out.resolve())
