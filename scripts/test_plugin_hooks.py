"""Tests for the kesekit plugin hooks (hooks/hooks.json + hooks/security-check-trigger.sh).

Run: python -m unittest discover -s scripts -p "test_*.py"
The shell tests run the script with `sh` (POSIX, or Git Bash on Windows) and are skipped when no sh is found.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HOOKS_JSON = ROOT / "hooks" / "hooks.json"
SCRIPT = ROOT / "hooks" / "security-check-trigger.sh"
SH = shutil.which("sh")


def run_hook(prompt: str | None, extra: dict | None = None) -> subprocess.CompletedProcess:
    payload = {"session_id": "t", "transcript_path": "/tmp/t.jsonl", "cwd": "/work", "hook_event_name": "UserPromptSubmit"}
    payload.update(extra or {})
    if prompt is not None:
        payload["prompt"] = prompt
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    return subprocess.run([SH, str(SCRIPT)], input=data, capture_output=True, timeout=20)


class HooksConfigTest(unittest.TestCase):
    def test_hooks_json_points_to_the_script(self):
        config = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))
        hooks = [h for entry in config["hooks"]["UserPromptSubmit"] for h in entry["hooks"]]
        self.assertEqual(len(hooks), 1)
        self.assertEqual(hooks[0]["type"], "command")
        self.assertIn("${CLAUDE_PLUGIN_ROOT}/hooks/security-check-trigger.sh", hooks[0]["command"])
        self.assertLessEqual(hooks[0]["timeout"], 10)

    def test_script_uses_lf_line_endings(self):
        self.assertNotIn(b"\r", SCRIPT.read_bytes())

    def test_gitattributes_pins_lf_for_shell_scripts(self):
        self.assertRegex((ROOT / ".gitattributes").read_text(encoding="utf-8"), r"(?m)^\*\.sh\s+text\s+eol=lf$")

    def test_skills_named_in_the_hint_exist(self):
        marketplace = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text(encoding="utf-8"))
        listed = {Path(s).name for p in marketplace["plugins"] for s in p["skills"]}
        named = set(re.findall(r"kesekit:(kesekit-[a-z-]+)", SCRIPT.read_text(encoding="utf-8")))
        self.assertTrue(named)
        self.assertLessEqual(named, listed)


@unittest.skipIf(SH is None, "sh is not available")
class TriggerScriptTest(unittest.TestCase):
    def assert_fires(self, prompt: str, extra: dict | None = None) -> None:
        proc = run_hook(prompt, extra)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        output = json.loads(proc.stdout)
        self.assertEqual(output["hookSpecificOutput"]["hookEventName"], "UserPromptSubmit")
        self.assertIn("kesekit:kesekit-start-ko", output["hookSpecificOutput"]["additionalContext"])

    def assert_silent(self, prompt: str | None, extra: dict | None = None) -> None:
        proc = run_hook(prompt, extra)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(proc.stdout.strip(), b"")

    def test_fires_on_security_check_requests(self):
        for prompt in ("보안점검해줘", "보안 점검 해 줘", "우리 서버 보안점검 좀 부탁해", "보안  점검"):
            with self.subTest(prompt=prompt):
                self.assert_fires(prompt)

    def test_silent_otherwise(self):
        for prompt in ("코드 리뷰해줘", "보안 업데이트 알려줘", "", "/kesekit-start-ko 보안점검"):
            with self.subTest(prompt=prompt):
                self.assert_silent(prompt)

    def test_folder_names_do_not_trigger(self):
        self.assert_silent("README 정리해줘", {"cwd": "C:/work/보안점검", "transcript_path": "/x/보안점검.jsonl"})

    def test_missing_prompt_and_garbage_input_exit_cleanly(self):
        self.assert_silent(None)
        proc = subprocess.run([SH, str(SCRIPT)], input=b"not json", capture_output=True, timeout=20)
        self.assertEqual((proc.returncode, proc.stdout), (0, b""))

    def test_prompt_with_quotes_and_newlines(self):
        self.assert_fires('서버 "web-01"\n보안점검 부탁해')


if __name__ == "__main__":
    unittest.main()
