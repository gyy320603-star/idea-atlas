#!/usr/bin/env python3
"""Prepare a repeatable host-agent task or render the host's returned atlas locally."""

import argparse
from contextlib import contextmanager
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

from atlas_records import write_atlas
from render_canvas import unique_object


PROTOCOL = Path(__file__).resolve().parent.parent / "references" / "generation-protocol.md"
HANDOFF = (
    "Work only from this task. During ideation use no tools or workspace access. "
    "For file-based delivery only, you may read the single task file designated by the host "
    "and write the final JSON to the single output file designated by the host. "
    "Do not inspect directories, other files, memory, previous runs or the network. "
    "Return only the JSON object as the final result."
)
MODES = ("fresh-worker", "current-chat", "fresh-chat")


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n").encode("utf-8")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def prepare(brief_file, materials, runs):
    # Decoding bytes directly preserves literal CRLFs and trailing whitespace.
    brief = brief_file.read_bytes().decode("utf-8")
    if not brief.strip():
        raise ValueError("brief must contain nonempty UTF-8 text")
    input_data = json_bytes({
        "brief": brief,
        "materials": [path.read_bytes().decode("utf-8") for path in materials],
    })
    protocol = PROTOCOL.read_bytes().decode("utf-8").rstrip()
    task = (HANDOFF + "\n\n" + protocol + "\n\n## Input JSON\n\n").encode("utf-8") + input_data
    receipt = {
        "status": "prepared",
        "input_sha256": digest(input_data),
        "dispatch_sha256": digest(task),
        "dispatch_hash_scope": "Exact UTF-8 bytes of task.txt only. Provider input is unobserved.",
    }
    runs.mkdir(parents=True, exist_ok=True)
    run = Path(tempfile.mkdtemp(prefix="run-", dir=runs)).resolve()
    try:
        (run / "input.json").write_bytes(input_data)
        (run / "task.txt").write_bytes(task)
        (run / "receipt.json").write_bytes(json_bytes(receipt))
        (run / ".finish.lock").write_bytes(b"0")
    except OSError:
        shutil.rmtree(run)
        raise
    return run


@contextmanager
def finish_lock(run):
    # The lock file remains in place. OS locks release automatically on process exit.
    with (run / ".finish.lock").open("r+b") as lock:
        if os.name == "nt":
            import msvcrt
            msvcrt.locking(lock.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl
            fcntl.flock(lock, fcntl.LOCK_EX)
        yield


def reject_constant(token):
    raise ValueError(f"invalid JSON number: {token}")


def finish(run, result_file, mode):
    if run.is_symlink() or not run.is_dir():
        raise ValueError("supply a directory allocated by prepare")
    run = run.resolve()
    result = result_file.read_bytes()
    pending = run / ".publishing"
    receipt_path = run / "receipt.json"
    output = run / "visual" / "atlas.html"
    with finish_lock(run):
        receipt = json.loads(receipt_path.read_bytes())
        input_data = (run / "input.json").read_bytes()
        if (digest(input_data) != receipt["input_sha256"]
                or digest((run / "task.txt").read_bytes()) != receipt["dispatch_sha256"]):
            raise ValueError("frozen input or dispatch text changed after prepare")
        generation_hash = digest(result)
        if receipt["status"] == "complete":
            if receipt["generation_sha256"] != generation_hash or receipt["host_declared_mode"] != mode:
                raise ValueError("run already completed with a different generation or host declaration")
            if digest((run / "generation.json").read_bytes()) != generation_hash or not output.is_file():
                raise ValueError("completed run's archived generation or HTML is missing or changed")
            if pending.is_dir() and not pending.is_symlink():
                pending.rmdir()  # Recover if interrupted immediately after publishing the receipt.
            return output
        if receipt["status"] != "prepared":
            raise ValueError("unrecognized run status")
        completed = dict(receipt, status="complete", generation_sha256=generation_hash,
                         host_declared_mode=mode)
        if not os.path.lexists(pending):
            envelope = json.loads(result.decode("utf-8-sig"), object_pairs_hook=unique_object,
                                  parse_constant=reject_constant)
            with tempfile.TemporaryDirectory(prefix=".render-", dir=run) as tmp:
                bundle = Path(tmp) / "bundle"
                bundle.mkdir()
                write_atlas(bundle, envelope, json.loads(input_data)["brief"])
                (bundle / "generation.json").write_bytes(result)
                for item in bundle.iterdir():
                    if os.path.lexists(run / item.name):
                        raise ValueError(f"run already contains {item.name}")
                (bundle / "receipt.json").write_bytes(json_bytes(completed))
                bundle.rename(pending)

        # The pending directory holds only the files still to publish. A retry can
        # resume an interrupted rename sequence only with the same result and mode.
        if pending.is_symlink() or not pending.is_dir():
            raise ValueError("invalid pending publication directory")
        if json.loads((pending / "receipt.json").read_bytes()) != completed:
            raise ValueError("interrupted publication requires the original generation and host declaration")
        for item in pending.iterdir():
            if item.name == "receipt.json":
                continue
            dest = run / item.name
            if os.path.lexists(dest):
                raise ValueError(f"run already contains {item.name}")
            item.rename(dest)
        (pending / "receipt.json").replace(receipt_path)
        pending.rmdir()
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    start = commands.add_parser("prepare", help="freeze the input and print its new run directory")
    start.add_argument("--brief", type=Path, required=True)
    start.add_argument("--runs", type=Path, required=True)
    start.add_argument("--material", type=Path, action="append", default=[])
    end = commands.add_parser("finish", help="archive the generation and print the rendered HTML path")
    end.add_argument("--run", type=Path, required=True)
    end.add_argument("--result", type=Path, required=True)
    end.add_argument("--mode", choices=MODES, default="unspecified",
                     help="host-declared context used for generation")
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            print(prepare(args.brief, args.material, args.runs))
        else:
            print(finish(args.run, args.result, args.mode))
    except (KeyError, OSError, ValueError) as exc:
        parser.exit(1, f"Cannot {args.command} run: {exc}\n")


if __name__ == "__main__":
    main()
