import json
from html.parser import HTMLParser
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


RENDERER = Path(__file__).resolve().parents[1] / "scripts" / "render_canvas.py"


class JsonScripts(HTMLParser):
    """Read the actual HTML script elements that the offline reader consumes."""

    def __init__(self):
        super().__init__()
        self.blocks = {}
        self.current = None

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == "script" and attributes.get("type") == "application/json":
            self.current = attributes["id"]
            self.blocks[self.current] = ""

    def handle_data(self, text):
        if self.current is not None:
            self.blocks[self.current] += text

    def handle_endtag(self, tag):
        if tag == "script":
            self.current = None


def source_manifest():
    return {
        "project": {"title": "点心台"},
        "lenses": {"备餐": {"name": "备餐", "q": "怎么准备？", "code": "A"},
                   "提前备料": {"name": "提前备料", "q": "何时分装？", "code": "B"}},
        "cards": {
            "A01": {"id": "A01", "lens": "备餐", "title": "便当盒", "status": "live",
                    "evidence": "grey", "proof": "拟用两个周末验证", "links": ["B01"],
                    "short": {"rank": 1, "why": "方便携带"},
                    "scores": {"specificity": 4, "fit": 3}, "score": 7},
            "B01": {"id": "B01", "lens": "提前备料", "title": "分装盘", "status": "seed"},
        },
        "handoff": ["A01"],
        "grill": {"A01": {"verdict": "narrow", "note": "先做一份。",
                          "rounds": [{"q": "需要多大？", "consider": "午餐份量。", "decision": "缩小。"}]}},

    }


class RenderCanvasTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.input = self.root / "input.json"
        self.output = self.root / "output.html"

    def invoke(self, manifest):
        self.input.write_text(json.dumps(manifest, ensure_ascii=False), encoding="utf-8")
        # Use an arbitrary cwd, as an agent will when rendering a user's project.
        return subprocess.run([sys.executable, str(RENDERER), str(self.input), str(self.output)],
                              cwd=self.root, capture_output=True, text=True)

    def embedded_source(self, manifest):
        result = self.invoke(manifest)
        self.assertEqual(result.returncode, 0, result.stderr)
        parser = JsonScripts()
        parser.feed(self.output.read_text(encoding="utf-8"))
        self.assertEqual(list(parser.blocks), ["atlasData"])
        return json.loads(parser.blocks["atlasData"])

    def test_source_fields_preserve_branches_decisions_and_scores(self):
        data = source_manifest()
        self.assertEqual(self.embedded_source(data), data)

    def test_previous_bilingual_manifest_uses_only_source_copy(self):
        data = source_manifest()
        data["language"] = "zh"
        data["translations"] = {"en": {"project": {"title": "Stale translated draft title"}}}
        self.assertEqual(self.embedded_source(data), {k: v for k, v in data.items() if k != "translations"})
        self.assertNotIn("Stale translated draft title", self.output.read_text(encoding="utf-8"))

    def test_third_language_reading_with_no_ideas(self):
        data = {"language": "fr-CA", "project": {"title": "Un comptoir partagé"}, "cards": {},
                "readings": {"R1": {"name": "Rangement", "q": "Où ranger les tasses ?",
                                    "premise": "Le comptoir est partagé.", "audience": "Les collègues",
                                    "check": "Observer une pause-café."}}}
        self.assertEqual(self.embedded_source(data), data)

    def test_source_text_can_include_script_delimiters_and_template_markers(self):
        data = source_manifest()
        data["grill"]["A01"]["rounds"][0]["decision"] = 'narrow：先检查 </ScRiPt><p>&</p> __ATLAS_DATA__'
        self.assertEqual(self.embedded_source(data), data)

    def test_invalid_source_does_not_replace_the_last_good_output(self):
        data = source_manifest()
        self.embedded_source(data)
        previous = self.output.read_bytes()
        data["cards"]["A01"]["lens"] = "未声明的视角"
        self.assertNotEqual(self.invoke(data).returncode, 0)
        self.assertEqual(self.output.read_bytes(), previous)


if __name__ == "__main__":
    unittest.main()
