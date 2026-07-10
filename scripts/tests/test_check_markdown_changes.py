"""Offline tests for the changed-Markdown lint gate."""

from __future__ import annotations

import importlib.util
import subprocess
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[1] / "check_markdown_changes.py"
SPEC = importlib.util.spec_from_file_location(
    "check_markdown_changes_test", SCRIPT
)
gate = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(gate)


class MarkdownSelectionTests(unittest.TestCase):
    def test_only_exact_ignore_paths_are_exempt(self) -> None:
        exemptions = gate.load_explicit_exemptions()
        lint, exempt = gate.select_markdown_files(
            {
                "README.md",
                "research/research-assistant-v7.md",
                "research/new-prompt.md",
                "scripts/tool.py",
            },
            exemptions,
        )
        self.assertEqual(
            ["README.md", "research/new-prompt.md"], lint
        )
        self.assertEqual(
            ["research/research-assistant-v7.md"], exempt
        )

    def test_changed_paths_cover_all_git_states(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                [
                    "git", "-C", str(repo), "config", "user.email",
                    "test@example.invalid",
                ],
                check=True,
            )
            readme = repo / "README.md"
            readme.write_text("# Base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "base"],
                check=True,
            )
            base = gate._git_text(repo, "rev-parse", "HEAD")

            committed = repo / "committed.md"
            committed.write_text("# Committed\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo), "add", "committed.md"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "committed"],
                check=True,
            )

            staged = repo / "staged.md"
            staged.write_text("# Staged\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(repo), "add", "staged.md"], check=True
            )
            readme.write_text("# Unstaged\n", encoding="utf-8")
            (repo / "untracked.md").write_text(
                "# Untracked\n", encoding="utf-8"
            )

            self.assertEqual(
                {
                    "README.md",
                    "committed.md",
                    "staged.md",
                    "untracked.md",
                },
                gate.changed_paths(repo, base),
            )

    def test_approved_bootstrap_exemption_is_allowed(self) -> None:
        gate.validate_no_new_exemptions(
            {"research/research-assistant-v7.md"}, set()
        )

    def test_unapproved_exemption_is_rejected_by_base_comparison(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir)
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Test"],
                check=True,
            )
            subprocess.run(
                [
                    "git", "-C", str(repo), "config", "user.email",
                    "test@example.invalid",
                ],
                check=True,
            )
            (repo / ".markdownlintignore").write_text(
                "\n", encoding="utf-8"
            )
            (repo / "README.md").write_text("# Base\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "commit", "-qm", "base"],
                check=True,
            )
            base = gate._git_text(repo, "rev-parse", "HEAD")
            (repo / ".markdownlintignore").write_text(
                "unreviewed.md\n", encoding="utf-8"
            )
            self.assertEqual(
                set(), gate.load_base_explicit_exemptions(repo, base)
            )
            self.assertEqual(
                {"unreviewed.md"},
                gate.load_explicit_exemptions(repo / ".markdownlintignore"),
            )
            with self.assertRaises(gate.MarkdownGateError):
                gate.validate_no_new_exemptions({"unreviewed.md"}, set())


if __name__ == "__main__":
    unittest.main()
