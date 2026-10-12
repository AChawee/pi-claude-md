import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INSTALL = ROOT / "scripts/install.py"
TOKEN = "tok-3f9a1c77e2b54d0e"


@unittest.skipUnless(shutil.which("claude"), "claude CLI not on PATH")
class Installer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.home = Path(tempfile.mkdtemp())
        cls.env = {**os.environ, "HOME": str(cls.home), "USERPROFILE": str(cls.home), "CLAUDE_CONFIG_DIR": str(cls.home / ".claude")}
        cls.env_file = cls.home / ".config/pi-claude-md/ding.env"

    def run_install(self, *args):
        return subprocess.run([sys.executable, str(INSTALL), *args], env=self.env, capture_output=True, text=True, encoding="utf-8", timeout=300)

    def install(self, *names):
        return self.run_install("install", "--source", str(ROOT), *names)

    def listed(self):
        r = self.run_install("list")
        self.assertEqual(r.returncode, 0, r.stderr)
        return {p["name"]: p for p in json.loads(r.stdout)}

    def skills_of(self, name):
        r = subprocess.run([shutil.which("claude"), "plugin", "details", f"{name}@pi-claude-md"], env=self.env, capture_output=True, text=True, encoding="utf-8", timeout=60)
        return r.stdout

    def test_1_list_shows_every_marketplace_plugin(self):
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        plugins = self.listed()
        self.assertEqual(set(plugins), {p["name"] for p in marketplace["plugins"]})
        self.assertFalse(any(p["installed"] for p in plugins.values()))
        self.assertTrue(plugins["ding"]["needs_setup"])
        self.assertFalse(plugins["ding"]["setup_ok"])

    def test_2_install_selected_plugins_loads_their_skills(self):
        r = self.install("tyc-design-system", "create-guide")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        plugins = self.listed()
        self.assertTrue(plugins["tyc-design-system"]["installed"])
        self.assertTrue(plugins["create-guide"]["installed"])
        self.assertIn("Skills (1)", self.skills_of("create-guide"))

    def test_3_ding_is_skipped_until_env_is_filled(self):
        r = self.install("ding")
        self.assertIn(str(self.env_file), r.stdout)
        self.assertFalse(self.listed()["ding"]["installed"])

    def test_4_setup_creates_env_without_installing(self):
        r = self.run_install("setup", "ding")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.env_file.is_file())
        self.assertFalse(self.listed()["ding"]["installed"])

    def test_5_ding_installs_after_token_is_filled(self):
        self.env_file.write_text(f"SECRET_AUTH={TOKEN}\n", encoding="utf-8")
        r = self.install("ding")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertNotIn(TOKEN, r.stdout + r.stderr)
        self.assertTrue(self.listed()["ding"]["installed"])

    def test_6_rerun_is_idempotent(self):
        r = self.install("tyc-design-system", "ding")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("ติดตั้งอยู่แล้ว", r.stdout)

    def test_7_unknown_plugin_fails_without_blocking_others(self):
        r = self.install("does-not-exist", "create-guide")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("does-not-exist", r.stdout)
        self.assertTrue(self.listed()["create-guide"]["installed"])


if __name__ == "__main__":
    unittest.main()
