import json
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
PLUGINS = {p["name"] for p in MARKETPLACE["plugins"]}
DOCS = ["README.md", "README.en.md", "INDEX.md", "CLAUDE.md"]
PLUGIN_ROW = re.compile(r"^\|\s*\[`?([a-z0-9-]+)`?\]\(\./plugins/", re.M)
LINK = re.compile(r"\]\((\./[^)#\s]+)")
LEAKS = {
    "home path": re.compile(r"/home/(?!<)[a-z0-9_-]+/|C:\\Users\\(?!<)\w+"),
    "real UUID": re.compile(r"\b(?!0{8}-|x{8}-)[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I),
    "secret value": re.compile(r"SECRET_AUTH\s*=\s*['\"]?(?!paste-token-here|\{|\$|['\"]?\s*$)[A-Za-z0-9._-]{8,}", re.M),
    "private IP": re.compile(r"\b(?:10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|192\.168)\.\d{1,3}\.\d{1,3}\b"),
}
TEXT_SUFFIXES = {".md", ".json", ".py", ".sh", ".yml", ".yaml", ".js", ".css", ".html", ".txt"}


def tracked_files():
    out = subprocess.run(["git", "ls-files", "-co", "--exclude-standard"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / f for f in out.splitlines() if (ROOT / f).suffix in TEXT_SUFFIXES and (ROOT / f).is_file()]


def frontmatter(skill_md):
    text = skill_md.read_text(encoding="utf-8")
    return text.split("\n---\n", 1)[0] if text.startswith("---\n") else ""


class Catalog(unittest.TestCase):
    def test_every_plugin_dir_is_in_marketplace(self):
        dirs = {d.name for d in (ROOT / "plugins").iterdir() if (d / ".claude-plugin/plugin.json").is_file()}
        self.assertEqual(dirs, PLUGINS)

    def test_manifest_name_and_version(self):
        for name in PLUGINS:
            manifest = json.loads((ROOT / "plugins" / name / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
            self.assertEqual(manifest["name"], name)
            self.assertRegex(manifest.get("version", ""), r"^\d+\.\d+\.\d+$", name)

    def test_skill_names_match_folders_and_have_metadata(self):
        for skill_md in (ROOT / "plugins").glob("*/skills/*/SKILL.md"):
            fm = frontmatter(skill_md)
            self.assertRegex(fm, rf"(?m)^name: {re.escape(skill_md.parent.name)}$", skill_md)
            self.assertRegex(fm, r"(?m)^description: \S", skill_md)
            self.assertRegex(fm, r"(?m)^metadata:\n(  \w+: .+\n?)+", skill_md)
            self.assertNotRegex(fm, r"(?m)^  version:", f"{skill_md}: version อยู่ใน plugin.json เท่านั้น")

    def test_docs_list_exactly_the_marketplace_plugins(self):
        for doc in ["README.md", "README.en.md", "INDEX.md"]:
            rows = set(PLUGIN_ROW.findall((ROOT / doc).read_text(encoding="utf-8")))
            self.assertEqual(rows, PLUGINS, doc)

    def test_readmes_have_matching_sections(self):
        count = lambda f: len(re.findall(r"(?m)^## ", (ROOT / f).read_text(encoding="utf-8")))
        self.assertEqual(count("README.md"), count("README.en.md"))

    def test_relative_links_resolve(self):
        for doc in DOCS:
            for link in LINK.findall((ROOT / doc).read_text(encoding="utf-8")):
                self.assertTrue((ROOT / link).exists(), f"{doc}: {link}")


class PublicRepoHygiene(unittest.TestCase):
    def test_no_private_data_in_repo(self):
        found = []
        for path in tracked_files():
            text = path.read_text(encoding="utf-8", errors="replace")
            for label, pattern in LEAKS.items():
                found += [f"{path.relative_to(ROOT)}: {label}: {m.group(0)[:40]}" for m in pattern.finditer(text)]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
