import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent.parent / "plugins/pi-commit/scripts"
SETUP = SCRIPTS / "setup.sh"
BLOCK = SCRIPTS / "block-no-verify.sh"
SH = shutil.which("sh") or "sh"
TEAM_REMOTE = "https://github.com/tycthailand/demo.git"
CODE = "1234"
HOOKS_PATH_SETTING = "~/.config/pi-claude-md/git-hooks"
TEMPLATE_SETTING = "~/.config/pi-claude-md/git-hooks/commit-template.txt"
GOOD = "fix(login): แก้ปุ่มบันทึกกดไม่ได้"
BAD = "แก้"
DROPPED_ENV = ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "GIT_AUTHOR_NAME", "GIT_AUTHOR_EMAIL",
               "GIT_COMMITTER_NAME", "GIT_COMMITTER_EMAIL", "GIT_CONFIG_GLOBAL", "XDG_CONFIG_HOME", "GIT_EDITOR", "EDITOR", "VISUAL")


class Sandbox(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)
        self.home = self.root / "home"
        self.repo = self.root / "repo"
        self.home.mkdir()
        self.repo.mkdir()
        self.env = {k: v for k, v in os.environ.items() if k not in DROPPED_ENV}
        self.env.update(HOME=str(self.home), USERPROFILE=str(self.home), GIT_CONFIG_NOSYSTEM="1", LC_ALL="C.UTF-8")
        self.git("config", "--global", "user.email", "demo@example.com", cwd=self.home)

    def run_cmd(self, args, cwd=None, stdin="", env=None):
        return subprocess.run(args, cwd=cwd or self.repo, input=stdin, env={**self.env, **(env or {})},
                              capture_output=True, text=True, encoding="utf-8", timeout=60)

    def git(self, *args, cwd=None, env=None, check=True):
        r = self.run_cmd(["git", *args], cwd=cwd, env=env)
        if check and r.returncode != 0:
            raise AssertionError(f"git {' '.join(args)} failed:\n{r.stdout}{r.stderr}")
        return r

    def setup_sh(self, *args, stdin=""):
        return self.run_cmd([SH, str(SETUP), *args], cwd=self.home, stdin=stdin)

    def global_config(self, key):
        return self.git("config", "--global", "--get", key, cwd=self.home, check=False).stdout.strip()

    def global_config_snapshot(self):
        path = self.home / ".gitconfig"
        return (path.read_text(encoding="utf-8") if path.exists() else "", (self.home / ".config/pi-claude-md").exists())

    def init_repo(self, remote=TEAM_REMOTE):
        self.git("init", "-q", "-b", "main")
        if remote:
            self.git("remote", "add", "origin", remote)

    def commit(self, *messages, extra=(), env=None):
        args = ["commit", "--allow-empty", *extra]
        for m in messages:
            args += ["-m", m]
        return self.git(*args, env=env, check=False)

    def commit_file(self, content, extra=()):
        path = self.root / "msg.txt"
        path.write_bytes(content.encode("utf-8"))
        return self.git("commit", "--allow-empty", "-F", str(path), *extra, check=False)

    def last_subject(self):
        return self.git("log", "-1", "--format=%s").stdout.strip()


class Installed(Sandbox):
    def setUp(self):
        super().setUp()
        r = self.setup_sh("install", CODE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.init_repo()

    def assertAccepted(self, r):
        self.assertEqual(r.returncode, 0, r.stderr)

    def assertRejected(self, r, problem):
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("pi-commit: commit rejected", r.stderr)
        self.assertIn(problem, r.stderr)


class MessageFormat(Installed):
    ACCEPTED = [
        "feat(tasks): เพิ่ม comment thread แนบไฟล์ได้",
        "fix: แก้ปุ่มบันทึกกดไม่ได้",
        "etc: ประชุมสรุป requirement",
        "perf(queries): add index for task list",
        "security(deps): bump next to patched version",
        "chore(ci/build): rename workflow step",
        "fix: แก้ปุ่มบัน",
        "fix: abcdefghij",
    ]
    REJECTED = [
        ("แก้", "first line must be"),
        ("update", "first line must be"),
        ("wip", "first line must be"),
        ("Feat: add thing here", "first line must be"),
        ("fix:แก้ปุ่มบันทึกกดไม่ได้", "first line must be"),
        ("fix:  แก้ปุ่มบันทึกกดไม่ได้", "first line must be"),
        ("fix(): แก้ปุ่มบันทึกกดไม่ได้", "first line must be"),
        ("fix (api): แก้ปุ่มบันทึกกดไม่ได้", "first line must be"),
        ("feature: add something new", 'unknown type "feature"'),
        ("fix: แก้บั๊ก", "too short"),
        ("fix: แก้ปุ่มบั", "too short"),
        ("fix: abcdefghi", "too short"),
        ("fix: update code", "too vague"),
        ("fix: Minor Changes", "too vague"),
        ("deploy! fix login page", "put deploy! on its own line"),
    ]

    def test_accepted_subjects(self):
        for subject in self.ACCEPTED:
            with self.subTest(subject=subject):
                self.assertAccepted(self.commit(subject))
                self.assertEqual(self.last_subject(), subject)

    def test_rejected_subjects(self):
        for subject, problem in self.REJECTED:
            with self.subTest(subject=subject):
                r = self.commit(subject)
                self.assertRejected(r, problem)
                self.assertIn(f"You wrote : {subject}", r.stderr)

    def test_rejection_shows_how_to_fix(self):
        r = self.commit(BAD)
        for hint in ["Expected  : type(scope): description", "Example   :", "Types     : feat fix perf refactor docs test style build ci chore security revert etc"]:
            self.assertIn(hint, r.stderr)

    def test_body_and_trailers_are_free_form(self):
        self.assertAccepted(self.commit(GOOD, "- รายละเอียดข้อ 1\n- detail two", "Co-Authored-By: Claude <noreply@anthropic.com>"))

    def test_leading_blank_lines_are_ignored(self):
        self.assertAccepted(self.commit_file(f"\n\n{GOOD}\n"))


class DeployAndExemptions(Installed):
    def test_bare_deploy_is_allowed(self):
        for message in ["deploy!", "  deploy!  ", "deploy!\n\ndeploy!"]:
            with self.subTest(message=message):
                self.assertAccepted(self.commit(message))

    def test_deploy_line_inside_normal_commit(self):
        self.assertAccepted(self.commit(GOOD, "deploy!"))
        self.assertIn("deploy!", self.git("log", "-1", "--format=%B").stdout)

    def test_deploy_line_does_not_excuse_bad_subject(self):
        self.assertRejected(self.commit(BAD, "deploy!"), "first line must be")

    def test_merge_commit(self):
        self.assertAccepted(self.commit(GOOD))
        self.git("checkout", "-q", "-b", "other")
        self.assertAccepted(self.commit("feat: งานบน branch อื่น"))
        self.git("checkout", "-q", "main")
        self.assertAccepted(self.commit("feat: งานบน main ระหว่างนั้น"))
        r = self.git("merge", "--no-ff", "--no-edit", "other", check=False)
        self.assertAccepted(r)
        self.assertTrue(self.last_subject().startswith("Merge branch 'other'"))

    def test_revert(self):
        (self.repo / "a.txt").write_text("a", encoding="utf-8")
        self.git("add", "a.txt")
        self.assertAccepted(self.git("commit", "-m", GOOD, check=False))
        self.assertAccepted(self.git("revert", "--no-edit", "HEAD", check=False))
        self.assertTrue(self.last_subject().startswith('Revert "'))

    def test_fixup_and_squash(self):
        self.assertAccepted(self.commit(GOOD))
        self.assertAccepted(self.git("commit", "--allow-empty", "--fixup", "HEAD", check=False))
        self.assertAccepted(self.git("commit", "--allow-empty", "--squash", "HEAD", "-m", "x", check=False))

    def test_empty_message_is_left_to_git(self):
        r = self.git("commit", "--allow-empty", "-m", "", check=False)
        self.assertNotIn("pi-commit", r.stderr)


class EdgeCases(Installed):
    def test_windows_line_endings(self):
        self.assertAccepted(self.commit_file(f"{GOOD}\r\n\r\nรายละเอียด\r\n"))
        self.assertRejected(self.commit_file(f"{BAD}\r\n"), "first line must be")

    def test_comment_lines_are_ignored(self):
        self.assertAccepted(self.commit_file(f"# note\n{GOOD}\n# trailing\n", extra=("--cleanup=strip",)))
        self.assertRejected(self.commit_file(f"# {GOOD}\n{BAD}\n", extra=("--cleanup=strip",)), "first line must be")

    def test_editor_with_template_and_verbose_diff(self):
        seen = self.root / "seen.txt"
        editor = self.root / "editor.py"
        editor.write_text(
            "import sys\n"
            f"seen = open(sys.argv[1], encoding='utf-8').read()\n"
            f"open({str(seen)!r}, 'w', encoding='utf-8').write(seen)\n"
            f"open(sys.argv[1], 'w', encoding='utf-8').write({GOOD!r} + '\\n' + seen)\n",
            encoding="utf-8")
        (self.repo / "b.txt").write_text("not-a-commit-type: added line\n", encoding="utf-8")
        self.git("add", "b.txt")
        editor_cmd = f'"{Path(sys.executable).as_posix()}" "{editor.as_posix()}"'
        r = self.git("commit", "-v", env={"GIT_EDITOR": editor_cmd}, check=False)
        self.assertAccepted(r)
        self.assertIn("type(scope): description", seen.read_text(encoding="utf-8"))
        message = self.git("log", "-1", "--format=%B").stdout
        self.assertEqual(message.strip(), f"{GOOD}\n\nEmp: {CODE}")

    def test_amend(self):
        self.assertAccepted(self.commit(GOOD))
        self.assertRejected(self.commit(BAD, extra=("--amend",)), "first line must be")
        self.assertAccepted(self.commit("fix(login): แก้ปุ่มบันทึกและข้อความเตือน", extra=("--amend",)))
        self.assertAccepted(self.git("commit", "--amend", "--no-edit", "--allow-empty", check=False))

    def test_team_remotes_are_checked(self):
        for url in ["https://github.com/tycthailand/demo.git", "git@github.com:tycthailand/demo.git",
                    "ssh://git@github.com/TycThailand/demo.git", "https://someone@github.com/tycthailand/demo"]:
            with self.subTest(url=url):
                self.git("remote", "set-url", "origin", url)
                self.assertRejected(self.commit(BAD), "first line must be")

    def test_other_remotes_are_not_checked(self):
        for url in ["https://github.com/ken1lnw/pi-claude-md.git", "https://github.com/tycthailand-fork/demo.git"]:
            with self.subTest(url=url):
                self.git("remote", "set-url", "origin", url)
                self.assertAccepted(self.commit(BAD))

    def test_repo_without_remote_is_not_checked(self):
        self.git("remote", "remove", "origin")
        self.assertAccepted(self.commit(BAD))

    def test_repo_hook_still_runs(self):
        marker = self.root / "repo-hook-ran"
        hook = self.repo / ".git/hooks/commit-msg"
        hook.write_text(f'#!/bin/sh\ntouch "{marker.as_posix()}"\n', encoding="utf-8")
        hook.chmod(0o755)
        self.assertAccepted(self.commit(GOOD))
        self.assertTrue(marker.exists())
        marker.unlink()
        self.assertRejected(self.commit(BAD), "first line must be")
        self.assertFalse(marker.exists())
        hook.write_text("#!/bin/sh\necho repo hook says no >&2\nexit 1\n", encoding="utf-8")
        r = self.commit(GOOD)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("repo hook says no", r.stderr)


class Identity(Installed):
    def test_installed_code_is_the_author(self):
        self.assertAccepted(self.commit(GOOD))
        self.assertEqual(self.git("log", "-1", "--format=%an").stdout.strip(), CODE)

    def test_non_code_names_are_rejected(self):
        for name in ["ken1lnw", "12345", "123", "1234 Ken"]:
            with self.subTest(name=name):
                self.git("config", "--global", "user.name", name)
                r = self.commit(GOOD)
                self.assertRejected(r, f'git user.name is "{name}"')
                self.assertIn("git config --global user.name", r.stderr)

    def test_repo_level_name_override_is_checked(self):
        self.git("config", "user.name", "someone")
        self.assertRejected(self.commit(GOOD), 'git user.name is "someone"')

    def test_identity_and_format_problems_are_reported_together(self):
        self.git("config", "--global", "user.name", "ken1lnw")
        r = self.commit(BAD)
        self.assertIn("git user.name is", r.stderr)
        self.assertIn("first line must be", r.stderr)


class EmployeeTrailer(Installed):
    def body(self):
        return self.git("log", "-1", "--format=%B").stdout.strip()

    def test_accepted_commit_gets_trailer(self):
        self.assertAccepted(self.commit(GOOD))
        self.assertEqual(self.body(), f"{GOOD}\n\nEmp: {CODE}")
        self.assertEqual(self.git("log", "-1", "--format=%(trailers:key=Emp,valueonly)").stdout.strip(), CODE)

    def test_trailer_joins_existing_trailers(self):
        self.assertAccepted(self.commit(GOOD, "รายละเอียด", "Co-Authored-By: Claude <noreply@anthropic.com>"))
        self.assertTrue(self.body().endswith(f"Co-Authored-By: Claude <noreply@anthropic.com>\nEmp: {CODE}"))

    def test_amend_replaces_instead_of_duplicating(self):
        self.assertAccepted(self.commit(GOOD))
        self.assertAccepted(self.commit("fix(login): แก้ปุ่มบันทึกและข้อความเตือน", "Emp: 9999", extra=("--amend",)))
        self.assertAccepted(self.git("commit", "--amend", "--no-edit", "--allow-empty", check=False))
        self.assertEqual(self.body().count("Emp:"), 1)
        self.assertIn(f"Emp: {CODE}", self.body())

    def test_windows_line_endings_stay_clean(self):
        self.assertAccepted(self.commit_file(f"{GOOD}\r\n\r\nรายละเอียด\r\n"))
        self.assertNotIn("\r", self.body())
        self.assertTrue(self.body().endswith(f"Emp: {CODE}"))

    def test_deploy_line_is_kept(self):
        self.assertAccepted(self.commit(GOOD, "deploy!"))
        self.assertEqual(self.body(), f"{GOOD}\n\ndeploy!\n\nEmp: {CODE}")

    def test_exempt_and_rejected_commits_are_untouched(self):
        self.assertAccepted(self.commit("deploy!"))
        self.assertEqual(self.body(), "deploy!")
        self.assertAccepted(self.commit('Revert "fix(login): แก้ปุ่มบันทึกกดไม่ได้"'))
        self.assertNotIn("Emp:", self.body())
        self.assertNotEqual(self.commit(BAD).returncode, 0)

    def test_other_repos_are_untouched(self):
        self.git("remote", "set-url", "origin", "https://github.com/ken1lnw/pi-claude-md.git")
        self.assertAccepted(self.commit(GOOD))
        self.assertEqual(self.body(), GOOD)


class Setup(Sandbox):
    def test_install_with_code(self):
        r = self.setup_sh("install", CODE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.global_config("user.name"), CODE)
        self.assertEqual(self.global_config("core.hooksPath"), HOOKS_PATH_SETTING)
        self.assertEqual(self.global_config("commit.template"), TEMPLATE_SETTING)
        self.assertTrue((self.home / ".config/pi-claude-md/git-hooks/commit-msg").is_file())
        self.assertTrue((self.home / ".config/pi-claude-md/git-hooks/commit-template.txt").is_file())
        self.assertIn("pi-commit installed", r.stdout)

    def test_interactive_retries_until_four_digits(self):
        r = self.setup_sh("install", stdin="abc\n12345\n1234\ny\n")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(r.stderr.count("Must be exactly 4 digits"), 2)
        self.assertEqual(self.global_config("user.name"), CODE)

    def test_interactive_enter_means_yes(self):
        self.assertEqual(self.setup_sh("install", stdin="1234\n\n").returncode, 0)
        self.assertEqual(self.global_config("user.name"), CODE)

    def test_console_line_endings_are_accepted(self):
        r = subprocess.run([SH, str(SETUP), "install"], cwd=self.home, input=b"1234\r\n\r\n", env=self.env,
                           capture_output=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr.decode("utf-8", "replace"))
        self.assertEqual(self.global_config("user.name"), CODE)

    def test_answer_no_changes_nothing(self):
        before = self.global_config_snapshot()
        r = self.setup_sh("install", stdin="1234\nn\n")
        self.assertEqual(r.returncode, 1)
        self.assertIn("nothing was changed", r.stderr)
        self.assertEqual(self.global_config_snapshot(), before)

    def test_cancel_mid_prompt_changes_nothing(self):
        before = self.global_config_snapshot()
        for stdin in ["", "12"]:
            with self.subTest(stdin=stdin):
                r = self.setup_sh("install", stdin=stdin)
                self.assertEqual(r.returncode, 1)
                self.assertIn("cancelled", r.stderr)
                self.assertEqual(self.global_config_snapshot(), before)

    def test_invalid_code_argument_changes_nothing(self):
        before = self.global_config_snapshot()
        for code in ["12a4", "123", "12345"]:
            with self.subTest(code=code):
                r = self.setup_sh("install", code)
                self.assertEqual(r.returncode, 1)
                self.assertIn("not a 4-digit employee code", r.stderr)
                self.assertEqual(self.global_config_snapshot(), before)

    def test_foreign_hooks_path_is_not_overwritten(self):
        self.git("config", "--global", "core.hooksPath", "~/.husky-global", cwd=self.home)
        before = self.global_config_snapshot()
        r = self.setup_sh("install", CODE)
        self.assertEqual(r.returncode, 1)
        self.assertIn('core.hooksPath is already set to "~/.husky-global"', r.stderr)
        self.assertIn("git config --global --unset core.hooksPath", r.stderr)
        self.assertEqual(self.global_config_snapshot(), before)

    def test_own_commit_template_is_kept(self):
        self.git("config", "--global", "commit.template", "~/my-template.txt", cwd=self.home)
        r = self.setup_sh("install", CODE)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(self.global_config("commit.template"), "~/my-template.txt")
        self.assertIn("kept your own", r.stdout)

    def test_rerun_updates_code_and_hook(self):
        self.git("config", "--global", "user.name", "ken1lnw", cwd=self.home)
        self.setup_sh("install", CODE)
        hook = self.home / ".config/pi-claude-md/git-hooks/commit-msg"
        hook.write_text("stale", encoding="utf-8")
        self.assertEqual(self.setup_sh("install", "5678").returncode, 0)
        self.assertEqual(self.global_config("user.name"), "5678")
        self.assertEqual(hook.read_bytes(), (SCRIPTS / "commit-msg").read_bytes())
        self.setup_sh("uninstall")
        self.assertEqual(self.global_config("user.name"), "ken1lnw")

    def test_uninstall_restores_previous_state(self):
        self.git("config", "--global", "user.name", "ken1lnw", cwd=self.home)
        self.setup_sh("install", CODE)
        r = self.setup_sh("uninstall")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('git user.name is now "ken1lnw"', r.stdout)
        self.assertEqual(self.global_config("user.name"), "ken1lnw")
        self.assertEqual(self.global_config("core.hooksPath"), "")
        self.assertEqual(self.global_config("commit.template"), "")
        self.assertFalse((self.home / ".config/pi-claude-md/git-hooks").exists())
        self.assertFalse((self.home / ".config/pi-claude-md/pi-commit.previous-name").exists())

    def test_uninstall_without_previous_name_unsets_it(self):
        self.setup_sh("install", CODE)
        self.setup_sh("uninstall")
        self.assertEqual(self.global_config("user.name"), "")

    def test_uninstalled_hook_stops_checking(self):
        self.setup_sh("install", CODE)
        self.init_repo()
        self.assertNotEqual(self.commit(BAD).returncode, 0)
        self.setup_sh("uninstall")
        self.git("config", "--global", "user.name", CODE, cwd=self.home)
        self.assertEqual(self.commit(BAD).returncode, 0)

    def test_status(self):
        r = self.setup_sh("status")
        self.assertEqual(r.returncode, 1)
        self.assertIn("/pi-commit:setup", r.stdout)
        self.setup_sh("install", CODE)
        r = self.setup_sh("status")
        self.assertEqual(r.returncode, 0)
        self.assertIn("OK", r.stdout)

    def test_unknown_command_shows_usage(self):
        r = self.setup_sh("bogus")
        self.assertEqual(r.returncode, 1)
        self.assertIn("usage:", r.stderr)


class ClaudeBypassGuard(unittest.TestCase):
    BLOCKED = [
        "git commit --no-verify -m 'fix: แก้ปุ่มบันทึกกดไม่ได้'",
        "git commit -n -m 'fix: x'",
        "git commit -anm 'fix: x'",
        "git commit -m 'fix: x' -n",
        "git add . && git commit -n -m \"fix: x\"",
        "git -c core.hooksPath=/dev/null commit -m 'fix: x'",
        "git -C ../repo commit --no-verify -m x",
        "git commit --no-verify -F - <<'EOF'\nfeat: เพิ่มกราฟรายเดือน\nEOF",
    ]
    ALLOWED = [
        "git status",
        "git commit -m 'fix(login): แก้ปุ่มบันทึกกดไม่ได้'",
        "git commit -am 'feat: เพิ่มกราฟรายเดือน'",
        "git commit --amend --no-edit",
        "git commit -m 'fix: handle --no-edit flag'",
        "git commit -m 'feat(api): support -nocache option'",
        "git log -n 5 && git commit -m 'fix: แก้ปุ่มบันทึกกดไม่ได้'",
        "git log --grep commit -n 5",
        "git push --no-verify",
        "npm test -- -n 3",
    ]

    def guard(self, command, tool="Bash"):
        payload = json.dumps({"tool_name": tool, "tool_input": {"command": command}})
        return subprocess.run([SH, str(BLOCK)], input=payload, capture_output=True, text=True, encoding="utf-8", timeout=30)

    def test_bypass_attempts_are_blocked(self):
        for command in self.BLOCKED:
            for tool in ["Bash", "PowerShell"]:
                with self.subTest(command=command, tool=tool):
                    r = self.guard(command, tool)
                    self.assertEqual(r.returncode, 2)
                    self.assertIn("pi-commit: blocked", r.stderr)

    def test_normal_commands_pass(self):
        for command in self.ALLOWED:
            with self.subTest(command=command):
                r = self.guard(command)
                self.assertEqual(r.returncode, 0, r.stderr)

    def test_scripts_keep_unix_line_endings_after_checkout(self):
        for script in SCRIPTS.iterdir():
            with self.subTest(script=script.name):
                self.assertNotIn(b"\r", script.read_bytes())

    def test_hooks_json_points_at_guard(self):
        hooks = json.loads((SCRIPTS.parent / "hooks/hooks.json").read_text(encoding="utf-8"))
        entry = hooks["hooks"]["PreToolUse"][0]
        self.assertEqual(entry["matcher"], "Bash|PowerShell")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/scripts/block-no-verify.sh", entry["hooks"][0]["command"])


if __name__ == "__main__":
    unittest.main()
