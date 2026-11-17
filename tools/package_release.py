#!/usr/bin/env python3
"""Build the full release and the single-folder skill ZIP with Python 3.8+."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL = "idea-atlas"
COMPANION = "idea-to-positioning"


def skill_version(directory):
    frontmatter = (directory / "SKILL.md").read_text(encoding="utf-8").split("---", 2)[1]
    match = re.search(r'^  version: ["\']?(\d+\.\d+\.\d+)["\']?\s*$', frontmatter, re.M)
    if not match:
        raise ValueError("Missing semantic version in " + str(directory))
    return match.group(1)


def release_files():
    items = [ROOT / name for name in ("README.md", "README.zh-CN.md", "LICENSE")]
    for folder in (SKILL, "companions", "docs", "tools"):
        for path in (ROOT / folder).rglob("*"):
            if any(part.startswith(".") or part == "__pycache__" for part in path.relative_to(ROOT).parts):
                continue
            if path.is_symlink():
                raise ValueError("Unexpected symlink: " + str(path))
            if path.is_file() and path.suffix not in (".pyc", ".pyo"):
                items.append(path)
    return {path.relative_to(ROOT).as_posix(): path.read_bytes() for path in sorted(items)}


def write_zip(path, entries, prefix=""):
    with zipfile.ZipFile(path, "w") as archive:
        for name, data in sorted(entries.items()):
            info = zipfile.ZipInfo(prefix + name, date_time=(1980, 1, 1, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            archive.writestr(info, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    with zipfile.ZipFile(path) as archive:
        failed = archive.testzip()
        if failed:
            raise ValueError("CRC check failed: " + failed)


def build(output):
    version = skill_version(ROOT / SKILL)
    base = SKILL + "-" + version
    files = release_files()
    manifest = {"package": SKILL, "version": version,
                "companion": {"name": COMPANION, "version": skill_version(ROOT / "companions" / COMPANION)},
                "files": [{"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}
                          for name, data in files.items()]}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    files["MANIFEST.json"] = manifest_bytes
    output.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(dir=output) as stage:
        full = Path(stage) / (base + ".zip")
        install = Path(stage) / (SKILL + "-skill-" + version + ".zip")
        write_zip(full, files, base + "/")
        write_zip(install, {name: data for name, data in files.items() if name.startswith(SKILL + "/")})
        (ROOT / "MANIFEST.json").write_bytes(manifest_bytes)
        for archive in (full, install):
            destination = output / archive.name
            os.replace(archive, destination)
            print(destination)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ROOT / "dist")
    build(parser.parse_args().out.resolve())
