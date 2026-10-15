from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "handoff"
VALIDATOR = SKILL / "scripts" / "validate_handoff.py"
SNAPSHOT = SKILL / "scripts" / "collect_snapshot.py"
TEMPLATE = SKILL / "assets" / "HANDOFF.template.md"
EXAMPLE = ROOT / "examples" / "HANDOFF.example.md"
INSTALLER = ROOT / "install.py"


def run(script: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(script), *args], capture_output=True, text=True, check=False
    )


def validate_text(text: str) -> subprocess.CompletedProcess:
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "HANDOFF.md"
        path.write_text(text, encoding="utf-8")
        return run(VALIDATOR, str(path))


class SkillSpecTest(unittest.TestCase):
    """Checks the Agent Skills specification rules at agentskills.io/specification."""

    def test_frontmatter_follows_spec(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        frontmatter = text.split("---", 2)[1]
        name = re.search(r"(?m)^name:\s*(\S+)\s*$", frontmatter).group(1)
        description = re.search(r"(?m)^description:\s*(.+)$", frontmatter).group(1)
        self.assertEqual(name, SKILL.name)
        self.assertRegex(name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
        self.assertLessEqual(len(name), 64)
        self.assertLessEqual(len(description), 1024)

    def test_referenced_files_exist(self) -> None:
        text = (SKILL / "SKILL.md").read_text(encoding="utf-8")
        for relative in set(re.findall(r"(?:scripts|assets)/[\w.]+", text)):
            self.assertTrue((SKILL / relative).is_file(), relative)


class ValidatorTest(unittest.TestCase):
    def test_example_passes(self) -> None:
        result = run(VALIDATOR, str(EXAMPLE))
        self.assertEqual(result.returncode, 0, result.stdout)

    def test_unfilled_template_fails(self) -> None:
        result = run(VALIDATOR, str(TEMPLATE))
        self.assertEqual(result.returncode, 1)
        self.assertIn("Unresolved template placeholder", result.stdout)

    def test_missing_status_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace("Status: `active`\n", "")
        result = validate_text(text)
        self.assertEqual(result.returncode, 1)
        self.assertIn("Status", result.stdout)

    def test_closed_status_passes(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8").replace("Status: `active`", "Status: `closed`")
        self.assertEqual(validate_text(text).returncode, 0)

    def test_more_than_five_history_entries_fails(self) -> None:
        text = EXAMPLE.read_text(encoding="utf-8")
        entry = text.split("## 11. Handoff history", 1)[1].strip()
        result = validate_text(text + ("\n\n" + entry) * 5)
        self.assertEqual(result.returncode, 1)
        self.assertIn("keep at most 5", result.stdout)


class SnapshotTest(unittest.TestCase):
    def test_reports_rule_files_and_status(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            workspace = Path(tmp).resolve()
            subprocess.run(["git", "init", "-q"], cwd=workspace, check=True)
            (workspace / "AGENTS.md").write_text("rules\n", encoding="utf-8")
            (workspace / ".cursor" / "rules").mkdir(parents=True)
            (workspace / "docs").mkdir()
            (workspace / "docs" / "HANDOFF.md").write_text(
                EXAMPLE.read_text(encoding="utf-8"), encoding="utf-8"
            )
            result = run(SNAPSHOT, str(workspace))
        self.assertEqual(result.returncode, 0, result.stderr)
        snapshot = json.loads(result.stdout)
        self.assertTrue(snapshot["is_git_repository"])
        self.assertEqual(snapshot["handoff_status"], "active")
        self.assertEqual(
            snapshot["applicable_rule_files"],
            [str(workspace / "AGENTS.md"), str(workspace / ".cursor" / "rules")],
        )


class InstallerTest(unittest.TestCase):
    def setUp(self) -> None:
        self._tmp = tempfile.TemporaryDirectory()
        self.home = Path(self._tmp.name)
        (self.home / ".claude").mkdir()

    def tearDown(self) -> None:
        self._tmp.cleanup()

    def installer(self, *args: str) -> subprocess.CompletedProcess:
        return run(INSTALLER, "--home", str(self.home), *args)

    def test_install_links_every_detected_agent(self) -> None:
        self.assertEqual(self.installer().returncode, 0)
        for skills_dir in (".agents/skills", ".claude/skills"):
            link = self.home / skills_dir / "handoff"
            self.assertTrue(link.is_symlink())
            self.assertEqual(link.resolve(), SKILL.resolve())

    def test_skips_agents_that_are_not_installed(self) -> None:
        (self.home / ".claude").rmdir()
        self.installer()
        self.assertFalse((self.home / ".claude").exists())

    def test_never_overwrites_existing_skill(self) -> None:
        existing = self.home / ".claude" / "skills" / "handoff"
        existing.mkdir(parents=True)
        result = self.installer()
        self.assertEqual(result.returncode, 1)
        self.assertTrue(existing.is_dir() and not existing.is_symlink())

    def test_uninstall_removes_only_own_links(self) -> None:
        self.installer()
        other = self.home / ".agents" / "skills" / "handoff"
        other.unlink()
        other.mkdir()
        self.installer("--uninstall")
        self.assertFalse((self.home / ".claude" / "skills" / "handoff").exists())
        self.assertTrue(other.is_dir())


if __name__ == "__main__":
    unittest.main()
