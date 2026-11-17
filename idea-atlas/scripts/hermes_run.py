#!/usr/bin/env python3
"""Generate an independent atlas through a new one-shot Hermes CLI process."""

import argparse
from datetime import datetime, timezone
import os
from pathlib import Path
import stat
import subprocess
import tempfile

from agent_run import digest, finish, json_bytes, prepare


PROMPT = (
    "Read only task.txt in the current directory and execute its design task. "
    "Write the complete final JSON object to result.json in the current directory. "
    "Do not consult other files, sessions, past results or the network. "
    "After writing the file, reply RESULT_WRITTEN."
)
SESSION_VARIABLES = {
    "HERMES_SESSION_ID", "HERMES_SESSION_KEY", "HERMES_PARENT_SESSION_ID",
    "HERMES_RESUME_SESSION", "HERMES_RESUME_SESSION_ID", "HERMES_CONTINUE_LAST",
}


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def windows_launcher(path):
    # The Windows host may expose a PE launcher with no extension, or the
    # Python entry-point script under its Hermes virtual environment.
    if path.name.lower() not in ("hermes", "hermes.exe"):
        return None
    with path.open("rb") as stream:
        header = stream.readline(2048)
    if header.startswith(b"MZ"):
        return [str(path)]
    if path.name.lower() == "hermes" and header.startswith(b"#!") and b"python" in header.lower():
        for interpreter in (path.with_name("python.exe"), path.parent.parent / "Scripts" / "python.exe"):
            if interpreter.is_file():
                return [str(interpreter), str(path)]
    return None


def resolve_hermes(explicit=None):
    names = ("hermes.exe", "hermes") if os.name == "nt" else ("hermes",)
    if explicit is not None:
        if not explicit.is_absolute():
            raise ValueError("--hermes requires the absolute path to the Hermes launcher")
        candidates = [explicit]
    else:
        directories = (Path(entry) for entry in os.get_exec_path())
        candidates = (directory / name for directory in directories if directory.is_absolute() for name in names)
    for path in candidates:
        if not path.is_file():
            continue
        if os.name == "nt":
            command = windows_launcher(path)
            if command:
                return command
        elif os.access(path, os.X_OK):
            return [str(path)]
    raise FileNotFoundError("No usable Hermes launcher. Run on the Hermes host and set --hermes ABSOLUTE_FILE if needed.")


def read_regular(path):
    # Reject links, FIFOs, devices and Windows junctions before treating a worker's file as output.
    info = path.lstat()
    if (not stat.S_ISREG(info.st_mode) or info.st_nlink > 1
            or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT):
        raise ValueError(f"Expected a regular, unlinked {path.name}")
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0) | getattr(os, "O_NONBLOCK", 0) | getattr(os, "O_BINARY", 0)
    with os.fdopen(os.open(path, flags), "rb") as stream:
        opened = os.fstat(stream.fileno())
        if not stat.S_ISREG(opened.st_mode) or not os.path.samestat(info, opened):
            raise ValueError(f"{path.name} changed while opening it")
        return stream.read()


def save_worker(run, record):
    path = run / ".worker.tmp"
    path.write_bytes(json_bytes(record))
    path.replace(run / "worker.json")


def generate(run, hermes=None, ignore_rules=False):
    task = (run / "task.txt").read_bytes()
    env = {k: v for k, v in os.environ.items() if k.upper() not in SESSION_VARIABLES}
    record = {
        "status": "starting", "launcher": "hermes-one-shot", "started_at": timestamp(),
        "dispatch_sha256": digest(task), "isolation_scope": (
            "Fresh CLI process and temporary working directory; host profile is shared. "
            "Filesystem access is not sandboxed by this launcher. Provider-visible messages "
            "and host-injected context are not audited."
        ),
    }
    save_worker(run, record)
    try:
        command = resolve_hermes(hermes)
        flags = ["--ignore-rules"] if ignore_rules else []
        argv = [*command, *flags, "-z", PROMPT]
        record.update(argv=argv, flags=flags + ["-z"], ignore_rules_requested=bool(flags))
        with tempfile.TemporaryDirectory(prefix="atlas-worker-") as directory:
            work = Path(directory)
            (work / "task.txt").write_bytes(task)
            record.update(worker_directory=work.name, initial_files=["task.txt"])
            with subprocess.Popen(argv, cwd=work, env=env, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL) as child:
                record.update(status="running", pid=child.pid)
                save_worker(run, record)
                try:
                    record["returncode"] = child.wait()
                except KeyboardInterrupt:
                    child.kill()
                    child.wait()
                    raise

            # Preserve even malformed JSON or partial output on a nonzero exit.
            raw = run / "worker-result.json"
            if os.path.lexists(work / "result.json"):
                data = read_regular(work / "result.json")
                with raw.open("xb") as stream:
                    stream.write(data)
                record.update(raw_sha256=digest(data), raw_bytes=len(data))
            if record["returncode"] != 0:
                raise ValueError(f"Hermes exited with status {record['returncode']}")
            if not raw.is_file():
                raise ValueError("Hermes exited without result.json")
            if read_regular(work / "task.txt") != task:
                raise ValueError("The worker changed its task.txt")
            output = finish(run, raw, "fresh-worker")
            if digest((run / "generation.json").read_bytes()) != record["raw_sha256"]:
                raise ValueError("The archived generation differs from the worker result")
        record["status"] = "complete"
        return output
    except (Exception, KeyboardInterrupt) as exc:
        record.update(status="failed", error=str(exc) or type(exc).__name__)
        raise
    finally:
        record["finished_at"] = timestamp()
        save_worker(run, record)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brief", type=Path, required=True)
    parser.add_argument("--material", type=Path, action="append", default=[])
    parser.add_argument("--runs", type=Path, required=True)
    parser.add_argument("--hermes", type=Path, help="absolute path to the Hermes launcher (defaults to PATH)")
    parser.add_argument("--ignore-rules", action="store_true",
                        help="explicitly pass --ignore-rules to a Hermes CLI that supports it")
    args = parser.parse_args()
    run = None
    try:
        run = prepare(args.brief, args.material, args.runs)
        print(generate(run, args.hermes, args.ignore_rules))
    except (OSError, ValueError, KeyError, TypeError, KeyboardInterrupt) as exc:
        parser.exit(1, f"Atlas generation failed ({run or args.runs}): {exc or type(exc).__name__}\n")


if __name__ == "__main__":
    main()
