import importlib.util
import os
import stat
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from unittest import mock
from pathlib import Path

SEND = Path(__file__).resolve().parent.parent / "plugins/ding/skills/ding/send.py"
TOKEN = "tok-3f9a1c77e2b54d0e"
CHANNEL = "00000000-0000-0000-0000-000000000000"


class DingCli(unittest.TestCase):
    def setUp(self):
        self.home = Path(tempfile.mkdtemp())
        self.env_file = self.home / ".config/pi-claude-md/ding.env"

    def run_send(self, *args):
        env = {**os.environ, "HOME": str(self.home), "USERPROFILE": str(self.home)}
        return subprocess.run([sys.executable, str(SEND), *args], env=env, capture_output=True, text=True, encoding="utf-8", timeout=30)

    def write_env(self, content):
        self.env_file.parent.mkdir(parents=True, exist_ok=True)
        self.env_file.write_text(content, encoding="utf-8")

    def message(self, text):
        path = self.home / "msg.md"
        path.write_text(text, encoding="utf-8")
        return str(path)

    def test_check_env_without_file_names_expected_path(self):
        r = self.run_send("--check-env")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(str(self.env_file), r.stdout + r.stderr)

    def test_init_env_creates_placeholder_that_fails_check(self):
        r = self.run_send("--init-env")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertTrue(self.env_file.is_file())
        self.assertNotEqual(self.run_send("--check-env").returncode, 0)

    @unittest.skipIf(os.name == "nt", "POSIX permissions")
    def test_init_env_is_private(self):
        self.run_send("--init-env")
        self.assertEqual(stat.S_IMODE(self.env_file.stat().st_mode), 0o600)

    def test_init_env_keeps_existing_token(self):
        self.write_env(f"SECRET_AUTH={TOKEN}\n")
        self.run_send("--init-env")
        self.assertIn(TOKEN, self.env_file.read_text(encoding="utf-8"))

    def test_empty_token_fails_check(self):
        self.write_env("SECRET_AUTH=\n")
        self.assertNotEqual(self.run_send("--check-env").returncode, 0)

    def test_valid_token_passes_check_without_leaking(self):
        self.write_env(f"SECRET_AUTH='{TOKEN}'\n")
        r = self.run_send("--check-env")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotIn(TOKEN, r.stdout + r.stderr)

    def test_dry_run_needs_no_token(self):
        r = self.run_send("--dry-run", "--channel", CHANNEL, "--hashtag", "test", "--message-file", self.message("hello"))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("DRY RUN", r.stdout)

    def test_dry_run_with_attachment_shows_expiry(self):
        attachment = self.home / "report.pdf"
        attachment.write_bytes(b"%PDF-1.4")
        r = self.run_send("--dry-run", "--channel", CHANNEL, "--hashtag", "t", "--message-file", self.message("x"), "--file", str(attachment))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("report.pdf", r.stdout)

    @unittest.skipIf(os.name == "nt", "Windows forbids \" in filenames")
    def test_filename_that_breaks_multipart_is_rejected(self):
        attachment = self.home / 'report "final".pdf'
        attachment.write_bytes(b"%PDF-1.4")
        r = self.run_send("--dry-run", "--channel", CHANNEL, "--hashtag", "t", "--message-file", self.message("x"), "--file", str(attachment))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("ชื่อไฟล์", r.stderr)

    def test_ambiguous_tag_is_rejected(self):
        r = self.run_send("--dry-run", "--channel", CHANNEL, "--hashtag", "t", "--tags", "1007", "--message-file", self.message("@1007 order 21007"))
        self.assertNotEqual(r.returncode, 0)

    def test_send_without_token_reports_env_path(self):
        r = self.run_send("--channel", CHANNEL, "--hashtag", "t", "--message-file", self.message("hi"))
        self.assertNotEqual(r.returncode, 0)
        self.assertIn(str(self.env_file), r.stdout + r.stderr)

    def test_send_requires_channel(self):
        r = self.run_send("--hashtag", "t", "--message-file", self.message("hi"))
        self.assertNotEqual(r.returncode, 0)


def load_send():
    spec = importlib.util.spec_from_file_location("send", SEND)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class DingNetworkErrors(unittest.TestCase):
    def setUp(self):
        self.send = load_send()

    def test_unreachable_host_exits_with_thai_hint(self):
        with mock.patch("urllib.request.urlopen", side_effect=urllib.error.URLError("Name or service not known")):
            with self.assertRaises(SystemExit) as cm:
                self.send.post({}, "t")
        self.assertIn("VPN", str(cm.exception.code))

    def test_error_text_survives_bad_json(self):
        headers = {"content-type": "application/json"}
        self.assertEqual(self.send.error_text(500, headers, "<html>oops</html>"), "<html>oops</html>")
        self.assertIn("x", self.send.error_text(500, headers, '["x"]'))
        self.assertEqual(self.send.error_text(422, headers, '{"detail":[{"loc":["body","tags"],"msg":"bad"}]}'), "body.tags: bad")


if __name__ == "__main__":
    unittest.main()
