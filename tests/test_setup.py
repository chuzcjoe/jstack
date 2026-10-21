import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SetupTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sandbox = tempfile.TemporaryDirectory(prefix="jstack-setup-")
        cls.base = Path(cls.sandbox.name).resolve()
        cls.env = dict(os.environ)
        cls.env.update(
            GIT_CONFIG_NOSYSTEM="1",
            GIT_CONFIG_GLOBAL=os.devnull,
            GIT_TERMINAL_PROMPT="0",
        )
        cls.source = cls.base / "source checkout"
        cls.source.mkdir()
        shutil.copy2(ROOT / "setup.sh", cls.source / "setup.sh")
        for directory in ("agents", "skills"):
            shutil.copytree(ROOT / directory, cls.source / directory)
        cls.git(cls.source, "init", "-q")
        cls.git(cls.source, "add", ".")
        cls.git(
            cls.source,
            "-c", "user.name=J Stack Setup Tests",
            "-c", "user.email=tests@example.invalid",
            "commit", "-qm", "Test source",
        )

    @classmethod
    def tearDownClass(cls):
        cls.sandbox.cleanup()

    @classmethod
    def git(cls, directory, *args):
        return subprocess.run(
            ["git", "-C", str(directory), *args],
            env=cls.env, check=True, capture_output=True, text=True,
        )

    def setUp(self):
        self.workspace = Path(tempfile.mkdtemp(dir=self.base, prefix="project "))
        self.project = self.workspace / "host project"
        self.project.mkdir()
        self.git(self.project, "init", "-q")
        self.git(
            self.project, "-c", "protocol.file.allow=always",
            "submodule", "add", "-q", str(self.source), "vendor/j stack",
        )
        self.submodule = self.project / "vendor/j stack"

    def setup(self, *args, source=None, success=True):
        result = subprocess.run(
            [str((source or self.submodule) / "setup.sh"), *args],
            cwd=self.base, env=self.env, capture_output=True, text=True,
        )
        if success:
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        else:
            self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        return result

    def assert_links(self, codex=True, claude=True):
        links = {}
        if codex:
            links.update({
                ".agents/skills/j-mode": "skills/j-mode",
                ".codex/agents/j-agent.toml": "agents/j-agent.toml",
                ".codex/agents/j-agent.md": "agents/j-agent.md",
            })
        if claude:
            links.update({
                ".claude/skills/j-mode": "skills/j-mode",
                ".claude/agents/j-agent.md": "agents/j-agent.md",
            })
        for destination, source in links.items():
            with self.subTest(destination=destination):
                link = self.project / destination
                self.assertTrue(link.is_symlink())
                self.assertFalse(os.path.isabs(os.readlink(link)))
                self.assertEqual(link.resolve(), (self.submodule / source).resolve())

    def test_detects_superproject_from_unrelated_working_directory(self):
        self.setup()
        self.assert_links()
        self.assertFalse((self.submodule / ".agents").exists())

    def test_can_select_codex_only(self):
        self.setup("--codex")
        self.assert_links(claude=False)
        self.assertFalse((self.project / ".claude").exists())

    def test_can_select_claude_only(self):
        self.setup("--claude")
        self.assert_links(codex=False)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / ".codex").exists())

    def test_can_select_both_explicitly(self):
        self.setup("--claude", "--codex")
        self.assert_links()

    def test_rerun_preserves_existing_project_configuration(self):
        files = {
            ".codex/config.toml": "[agents]\nenabled = false\n",
            "AGENTS.md": "Project instructions\n",
            "CLAUDE.md": "Claude project instructions\n",
            ".claude/skills/other/SKILL.md": "Another skill\n",
        }
        for name, content in files.items():
            file = self.project / name
            file.parent.mkdir(parents=True, exist_ok=True)
            file.write_text(content)
        self.setup()
        links = {path: os.readlink(path) for path in self.project.rglob("*") if path.is_symlink()}
        self.setup()
        self.assert_links()
        for path, target in links.items():
            self.assertEqual(os.readlink(path), target)
        for name, content in files.items():
            self.assertEqual((self.project / name).read_text(), content)

    def test_submodule_updates_are_visible_through_links(self):
        self.setup()
        skill = self.submodule / "skills/j-mode/SKILL.md"
        skill.write_text(skill.read_text() + "\nUpdated instructions.\n")
        role = self.submodule / "agents/j-agent.md"
        role.write_text(role.read_text() + "\nUpdated delegate instructions.\n")
        for name in (".agents/skills/j-mode", ".claude/skills/j-mode"):
            self.assertEqual((self.project / name / "SKILL.md").read_text(), skill.read_text())
        for name in (".codex/agents/j-agent.md", ".claude/agents/j-agent.md"):
            self.assertEqual((self.project / name).read_text(), role.read_text())

    def test_links_survive_moving_the_host_project(self):
        self.setup()
        destination = self.workspace / "moved host project"
        self.project.rename(destination)
        self.project = destination
        self.submodule = self.project / "vendor/j stack"
        self.assert_links()

    def test_conflict_is_reported_before_creating_any_links(self):
        conflict = self.project / ".claude/agents/j-agent.md"
        conflict.parent.mkdir(parents=True)
        conflict.write_text("Existing custom agent\n")
        self.setup(success=False)
        self.assertEqual(conflict.read_text(), "Existing custom agent\n")
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / ".codex").exists())

    def test_existing_skill_directory_is_preserved(self):
        skill = self.project / ".agents/skills/j-mode/SKILL.md"
        skill.parent.mkdir(parents=True)
        skill.write_text("Existing skill\n")
        self.setup(success=False)
        self.assertEqual(skill.read_text(), "Existing skill\n")
        self.assertFalse(skill.parent.is_symlink())

    def test_different_or_dangling_symlink_is_preserved(self):
        link = self.project / ".claude/agents/j-agent.md"
        link.parent.mkdir(parents=True)
        link.symlink_to("missing-custom-agent.md")
        self.setup(success=False)
        self.assertEqual(os.readlink(link), "missing-custom-agent.md")
        self.assertFalse((self.project / ".agents").exists())

    def test_matching_absolute_symlink_is_accepted(self):
        link = self.project / ".agents/skills/j-mode"
        link.parent.mkdir(parents=True)
        link.symlink_to(self.submodule / "skills/j-mode", target_is_directory=True)
        self.setup()
        self.assertEqual(link.resolve(), (self.submodule / "skills/j-mode").resolve())
        self.assertTrue((self.project / ".claude/skills/j-mode/SKILL.md").is_file())

    def test_parent_path_that_is_a_file_prevents_partial_install(self):
        conflict = self.project / ".claude"
        conflict.write_text("Existing file\n")
        self.setup(success=False)
        self.assertEqual(conflict.read_text(), "Existing file\n")
        self.assertFalse((self.project / ".agents").exists())

    def test_standalone_checkout_requires_an_explicit_target(self):
        self.setup(source=self.source, success=False)
        self.assertFalse((self.source / ".agents").exists())

    def test_explicit_target_uses_the_target_repository_root(self):
        nested = self.project / "src/nested"
        nested.mkdir(parents=True)
        self.setup("--target", str(nested), "--codex", source=self.source)
        self.assertTrue((self.project / ".agents/skills/j-mode/SKILL.md").is_file())
        self.assertFalse((nested / ".agents").exists())

    def test_help_and_invalid_arguments_do_not_install(self):
        self.setup("--help")
        for args in (("--unknown",), ("--target",), ("--target", str(self.base / "missing"))):
            with self.subTest(args=args):
                self.setup(*args, success=False)
        self.assertFalse((self.project / ".agents").exists())
        self.assertFalse((self.project / ".claude").exists())

    def test_codex_adapter_is_valid_toml(self):
        self.setup("--codex")
        adapter = self.project / ".codex/agents/j-agent.toml"
        metadata = tomllib.loads(adapter.read_text())
        self.assertEqual(metadata["name"], "j-agent")
        self.assertTrue(metadata["description"])
        self.assertTrue(metadata["developer_instructions"])
        self.assertTrue((self.project / ".codex/agents/j-agent.md").is_file())


if __name__ == "__main__":
    unittest.main()
