import unittest
from pathlib import Path
from types import ModuleType
from unittest.mock import patch

import transcribe


class TranscribeFileTests(unittest.TestCase):
    def _fake_mlx_whisper(self, call_log: dict) -> ModuleType:
        module = ModuleType("mlx_whisper")

        def fake_transcribe(*args, **kwargs):
            call_log["args"] = args
            call_log["kwargs"] = kwargs
            return {
                "segments": [{"start": 0.0, "end": 1.0, "text": "hello"}],
                "language": kwargs.get("language") or "en",
            }

        module.transcribe = fake_transcribe
        return module

    def test_transcribe_file_passes_language_zh(self) -> None:
        call_log = {}
        file_path = Path("/virtual/sample.mp3")
        output_dir = Path("/virtual/out")
        fake_module = self._fake_mlx_whisper(call_log)
        with (
            patch.dict("sys.modules", {"mlx_whisper": fake_module}),
            patch("transcribe.save_srt"),
        ):
            result = transcribe.transcribe_file(file_path, output_dir, language="zh")

        self.assertIsNotNone(result)
        self.assertEqual(call_log["kwargs"]["language"], "zh")

    def test_transcribe_file_passes_language_en(self) -> None:
        call_log = {}
        file_path = Path("/virtual/sample.mp3")
        output_dir = Path("/virtual/out")
        fake_module = self._fake_mlx_whisper(call_log)
        with (
            patch.dict("sys.modules", {"mlx_whisper": fake_module}),
            patch("transcribe.save_srt"),
        ):
            result = transcribe.transcribe_file(file_path, output_dir, language="en")

        self.assertIsNotNone(result)
        self.assertEqual(call_log["kwargs"]["language"], "en")

    def test_transcribe_file_passes_none_when_language_not_set(self) -> None:
        call_log = {}
        file_path = Path("/virtual/sample.mp3")
        output_dir = Path("/virtual/out")
        fake_module = self._fake_mlx_whisper(call_log)
        with (
            patch.dict("sys.modules", {"mlx_whisper": fake_module}),
            patch("transcribe.save_srt"),
        ):
            result = transcribe.transcribe_file(file_path, output_dir)

        self.assertIsNotNone(result)
        self.assertIsNone(call_log["kwargs"]["language"])
