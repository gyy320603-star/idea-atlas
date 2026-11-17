"""Test the one-shot handoff without a model, provider or Hermes installation."""
import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import hermes_run


FAKE = """
from pathlib import Path
import sys
assert '-z' in sys.argv
assert sorted(x.name for x in Path.cwd().iterdir()) == ['task.txt']
Path('result.json').write_bytes(Path(__file__).with_name('response').read_bytes())
"""


class HermesHandoffTest(unittest.TestCase):
    def test_fresh_process_original_bytes_and_failed_handoff(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            stub = root / 'worker.py'
            stub.write_text(FAKE, encoding='utf-8')
            brief = root / 'brief'
            brief.write_text('Test brief', encoding='utf-8')
            raw = json.dumps({'scan': 'Open', 'manifest': {
                'project': {'title': 'Test'}, 'readings': {'R1': {
                    'name': 'Need', 'q': 'Who chooses?', 'premise': 'Unknown',
                    'audience': 'Buyer', 'check': 'Observe a choice'}},
                'cards': {}, 'grill': {}, 'handoff': []}}).encode()
            response = root / 'response'
            response.write_bytes(raw)
            def prepare():
                return hermes_run.prepare(brief, [], root / 'runs')
            with patch.object(hermes_run, 'resolve_hermes', return_value=[sys.executable, str(stub)]):
                first = prepare()
                hermes_run.generate(first)
                (first / 'worker-result.json').write_bytes(b'old result marker')
                second = prepare()
                html = hermes_run.generate(second, ignore_rules=True)
                self.assertTrue(html.is_file())
                self.assertEqual((first / 'task.txt').read_bytes(), (second / 'task.txt').read_bytes())
                self.assertEqual((second / 'worker-result.json').read_bytes(), raw)
                self.assertEqual((second / 'generation.json').read_bytes(), raw)
                records = [json.loads((r / 'worker.json').read_bytes()) for r in (first, second)]
                self.assertEqual(records[0]['flags'], ['-z'])
                self.assertEqual(records[1]['flags'], ['--ignore-rules', '-z'])
                self.assertNotEqual(records[0]['worker_directory'], records[1]['worker_directory'])
                failed = prepare()
                response.write_bytes(b'incomplete JSON')
                with self.assertRaises(ValueError):
                    hermes_run.generate(failed)
                self.assertFalse((failed / 'visual/atlas.html').exists())
                self.assertEqual((failed / 'worker-result.json').read_bytes(), response.read_bytes())
                self.assertEqual(json.loads((failed / 'worker.json').read_bytes())['status'], 'failed')
