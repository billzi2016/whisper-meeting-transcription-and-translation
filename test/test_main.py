import unittest

from main import build_parser


class BuildParserTests(unittest.TestCase):
    def setUp(self) -> None:
        self.parser = build_parser()

    def test_language_zh(self) -> None:
        args = self.parser.parse_args(["--language", "zh"])
        self.assertEqual(args.language, "zh")

    def test_language_en(self) -> None:
        args = self.parser.parse_args(["--language", "en"])
        self.assertEqual(args.language, "en")

    def test_language_default_is_none(self) -> None:
        args = self.parser.parse_args([])
        self.assertIsNone(args.language)
        self.assertIsNone(args.target_language)

    def test_invalid_language_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--language", "ja"])

    def test_target_language_zh(self) -> None:
        args = self.parser.parse_args(["--target-language", "zh"])
        self.assertEqual(args.target_language, "zh")

    def test_target_language_en(self) -> None:
        args = self.parser.parse_args(["--target-language", "en"])
        self.assertEqual(args.target_language, "en")

    def test_invalid_target_language_rejected(self) -> None:
        with self.assertRaises(SystemExit):
            self.parser.parse_args(["--target-language", "ja"])
