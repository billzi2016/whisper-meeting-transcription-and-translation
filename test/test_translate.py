import unittest

from translate import _build_system_prompt


class TranslatePromptTests(unittest.TestCase):
    def test_build_system_prompt_for_chinese(self) -> None:
        self.assertIn("简体中文", _build_system_prompt("zh"))

    def test_build_system_prompt_for_english(self) -> None:
        self.assertIn("英文", _build_system_prompt("en"))
