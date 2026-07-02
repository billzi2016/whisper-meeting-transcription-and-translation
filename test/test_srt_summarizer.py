import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from srt_summarizer.main import (
    _build_summarize_prompt,
    _detect_summary_language,
    _split_text_by_tokens,
    main,
    summarize,
)


class SummaryLanguageTests(unittest.TestCase):
    def test_detect_summary_language_zh(self) -> None:
        self.assertEqual(_detect_summary_language(Path("demo.zh.srt")), "zh")

    def test_detect_summary_language_en(self) -> None:
        self.assertEqual(_detect_summary_language(Path("demo.en.srt")), "en")

    def test_detect_summary_language_unsupported(self) -> None:
        self.assertIsNone(_detect_summary_language(Path("demo.ja.srt")))

    def test_build_summarize_prompt_for_chinese(self) -> None:
        self.assertIn("中文摘要", _build_summarize_prompt("zh"))

    def test_build_summarize_prompt_for_english(self) -> None:
        self.assertIn("英文摘要", _build_summarize_prompt("en"))


class TokenSplitTests(unittest.TestCase):
    def test_split_text_by_tokens_returns_multiple_chunks(self) -> None:
        chunks = _split_text_by_tokens("hello world " * 20, 5, "cl100k_base")
        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunks))


class SummarizeTests(unittest.TestCase):
    def test_summarize_single_chunk_calls_ollama_once(self) -> None:
        out_path = Path("/virtual/out.md")
        with patch("srt_summarizer.main._call_ollama", return_value="summary") as mock_call:
            result = summarize(
                "short text",
                "zh",
                "http://localhost:11434",
                "gpt-oss:120b",
                100000,
                "cl100k_base",
                out_path,
            )

        self.assertEqual(result, "summary")
        self.assertEqual(mock_call.call_count, 1)

    def test_summarize_multi_chunk_calls_merge(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            out_path = Path(tmpdir) / "demo.zh.summary.md"
            chunks = _split_text_by_tokens("hello world " * 40, 10, "cl100k_base")
            responses = [f"part{i}" for i in range(len(chunks))] + ["merged"]
            with patch("srt_summarizer.main._call_ollama", side_effect=responses) as mock_call:
                result = summarize(
                    "hello world " * 40,
                    "en",
                    "http://localhost:11434",
                    "gpt-oss:120b",
                    10,
                    "cl100k_base",
                    out_path,
                )

        self.assertEqual(result, "merged")
        self.assertEqual(mock_call.call_count, len(chunks) + 1)


class MainTests(unittest.TestCase):
    def test_main_generates_language_specific_summary_files(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            input_dir = Path(tmpdir) / "subs"
            input_dir.mkdir()
            zh_path = input_dir / "meeting.zh.srt"
            en_path = input_dir / "meeting.en.srt"
            zh_path.write_text("1\n00:00:00,000 --> 00:00:01,000\n你好\n", encoding="utf-8")
            en_path.write_text("1\n00:00:00,000 --> 00:00:01,000\nhello\n", encoding="utf-8")

            def fake_summarize(
                text: str,
                summary_language: str,
                ollama_url: str,
                model: str,
                chunk_size: int,
                encoding_name: str,
                out_path: Path,
            ) -> str:
                return f"{summary_language}:{text}"

            with patch(
                "sys.argv",
                ["main.py", "--input", str(input_dir), "--output", str(input_dir)],
            ), patch("srt_summarizer.main.summarize", side_effect=fake_summarize):
                main()

            zh_summary = input_dir / "meeting.zh.summary.md"
            en_summary = input_dir / "meeting.en.summary.md"
            self.assertTrue(zh_summary.exists())
            self.assertTrue(en_summary.exists())
            self.assertIn("zh:", zh_summary.read_text(encoding="utf-8"))
            self.assertIn("en:", en_summary.read_text(encoding="utf-8"))
