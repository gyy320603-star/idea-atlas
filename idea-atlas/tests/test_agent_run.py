import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import agent_run


class AgentRunTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.brief = self.root / "original.txt"
        self.brief.write_bytes("甲\r\n  乙  \n".encode())
        self.source = self.root / "source.txt"
        self.source.write_text("材料", encoding="utf-8")
        self.runs = self.root / "runs"

    def prepare(self):
        return agent_run.prepare(self.brief, [self.source], self.runs)

    def result(self, name):
        file = self.root / (name + ".json")
        manifest = {
            "project": {"title": name},
            "readings": {"R1": {"name": "Choices", "q": "Who chooses?", "premise": "A decision",
                                 "audience": "The buyer", "check": "Observe one choice."}},
            "cards": {}, "grill": {}, "handoff": [],
        }
        manifest["language"] = "en"
        file.write_bytes(agent_run.json_bytes({"scan": "No supported candidates.", "manifest": manifest}))
        return file

    def test_repeat_dispatch_and_frozen_brief(self):
        first = self.prepare()
        self.brief.rename(self.root / "renamed")
        self.brief = self.root / "renamed"
        second = self.prepare()
        self.assertNotEqual(first, second)
        packet = (first / "task.txt").read_bytes()
        self.assertEqual(packet, (second / "task.txt").read_bytes())
        frozen = json.loads((first / "input.json").read_bytes())
        self.assertEqual(frozen, {"brief": "甲\r\n  乙  \n", "materials": ["材料"]})
        self.assertNotIn(str(self.root).encode(), packet)
        self.brief.write_text("new prompt", encoding="utf-8")
        result = self.result("A")
        html = agent_run.finish(first, result, "fresh-worker")
        self.assertIn("  乙  ", (first / "00_BRIEF.md").read_text(encoding="utf-8"))
        self.assertTrue((first / "01_SCAN.md").read_text(encoding="utf-8").startswith("# Scan\n"))
        self.assertEqual((first / "generation.json").read_bytes(), result.read_bytes())
        self.assertEqual(agent_run.finish(first, result, "fresh-worker"), html)
        self.assertTrue(html.is_file())
        receipt = json.loads((first / "receipt.json").read_bytes())
        self.assertEqual(receipt["dispatch_sha256"], agent_run.digest(packet))
        self.assertEqual(receipt["generation_sha256"], agent_run.digest(result.read_bytes()))

    def test_failed_validation_and_file_collision_leave_run_prepared(self):
        run = self.prepare()
        result = self.result("A")
        valid = result.read_bytes()
        result.write_text('{"scan":"one","scan":"two"}', encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate JSON key"):
            agent_run.finish(run, result, "fresh-chat")
        result.write_bytes(valid)
        (run / "01_SCAN.md").write_bytes(b"existing")
        with self.assertRaisesRegex(ValueError, "already contains"):
            agent_run.finish(run, result, "fresh-chat")
        self.assertEqual((run / "01_SCAN.md").read_bytes(), b"existing")
        self.assertFalse((run / "generation.json").exists())
        self.assertEqual(json.loads((run / "receipt.json").read_bytes())["status"], "prepared")
        (run / "01_SCAN.md").unlink()
        agent_run.finish(run, result, "fresh-chat")

    def test_prepared_run_accepts_original_worker_language(self):
        for previous_version in (False, True):
            with self.subTest(previous_version=previous_version):
                run = self.prepare()
                if previous_version:
                    receipt_file = run / "receipt.json"
                    receipt = json.loads(receipt_file.read_bytes())
                    receipt["requires_bilingual"] = True
                    receipt_file.write_bytes(agent_run.json_bytes(receipt))
                result = self.result("Parapluies")
                envelope = json.loads(result.read_bytes())
                envelope["manifest"]["language"] = "fr"
                envelope["scan"] = "Une piste à vérifier."
                raw = json.dumps(envelope, ensure_ascii=False, indent=4).encode("utf-8")
                result.write_bytes(raw)
                self.assertTrue(agent_run.finish(run, result, "fresh-chat").is_file())
                self.assertEqual((run / "generation.json").read_bytes(), raw)
                self.assertIn(envelope["scan"], (run / "01_SCAN.md").read_text(encoding="utf-8"))

    def test_interrupted_publication(self):
        run = self.prepare()
        result = self.result("A")
        original_rename = Path.rename
        published = []

        def interrupt(item, target):
            if item.parent == run / ".publishing":
                if published:
                    raise OSError("interrupted")
                published.append(item.name)
            return original_rename(item, target)

        with patch.object(Path, "rename", interrupt), self.assertRaisesRegex(OSError, "interrupted"):
            agent_run.finish(run, result, "current-chat")
        self.assertEqual(len(published), 1)
        with self.assertRaisesRegex(ValueError, "original generation"):
            agent_run.finish(run, self.result("B"), "current-chat")
        self.assertTrue(agent_run.finish(run, result, "current-chat").is_file())
        self.assertFalse((run / ".publishing").exists())

    def test_simultaneous_finishes_preserve_one_generation(self):
        run = self.prepare()
        files = [self.result("A"), self.result("B")]
        calls = [
            subprocess.Popen([sys.executable, str(SCRIPTS / "agent_run.py"), "finish", "--run", str(run),
                              "--result", str(file), "--mode", "fresh-worker"],
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
            for file in files
        ]
        for call in calls:
            call.communicate(timeout=20)
        self.assertEqual(sorted(call.returncode for call in calls), [0, 1])
        winner = next(file for file, call in zip(files, calls) if call.returncode == 0)
        self.assertEqual((run / "generation.json").read_bytes(), winner.read_bytes())


if __name__ == "__main__":
    unittest.main()
