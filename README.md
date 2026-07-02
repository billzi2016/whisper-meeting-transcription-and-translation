# Whisper Meeting Transcription and Translation

[中文版](README.cn.md)

Local subtitle generation for audio and video, plus Chinese-English translation. The project uses [mlx-whisper](https://github.com/ml-explore/mlx-examples) for MLX-accelerated transcription on Apple Silicon and runs `gpt-oss:120b` through local [Ollama](https://ollama.com) for fully offline translation.

## Requirements

- Apple Silicon Mac (M1 / M2 / M3 / M4)
- Python 3.11+
- [ffmpeg](https://ffmpeg.org) for media decoding
- [Ollama](https://ollama.com) for translation (optional)

## Install

```bash
# Install ffmpeg
brew install ffmpeg

# Install Python dependencies
pip install -r requirements.txt
# Or install from pyproject.toml
pip install -e .

# Pull the translation model on first use
ollama pull gpt-oss:120b
```

## Usage

Put your audio or video files into the `media/` folder, then run:

```bash
python main.py
```

Subtitles are written to `subtitles/` and keep the original media extension in the filename:

```text
media/lecture.mp4   ->   subtitles/lecture.mp4.zh.srt
                    ->   subtitles/lecture.mp4.en.srt
```

## Quickstart

By default, Whisper detects the language automatically and only generates subtitles in that detected language:

```bash
python main.py
```

If auto detection is wrong, you can force the source language:

```bash
python main.py --language zh   # force Chinese transcription
python main.py --language en   # force English transcription
```

More examples are in [QUICKSTART.md](QUICKSTART.md).

### Common Options

```bash
python main.py --force
python main.py --no-translate
python main.py --language zh
python main.py --language en
python main.py --target-language zh
python main.py --target-language en
python main.py --input ./my_videos
python main.py --output ./subs
python main.py --whisper-model mlx-community/whisper-large-v3-mlx
python main.py --ollama-model gpt-oss:120b
python main.py --ollama-url http://localhost:11434
```

### Parameters

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | `media/` | Media folder |
| `--output` | `subtitles/` | Subtitle output folder |
| `--force` | false | Overwrite existing subtitle files |
| `--no-translate` | false | Transcribe only, skip translation |
| `--whisper-model` | `mlx-community/whisper-large-v3-mlx` | MLX Whisper model |
| `--language` | auto detect | Force source language, supports `zh` / `en` |
| `--target-language` | no translation | Translation target language, supports `zh` / `en` |
| `--ollama-model` | `gpt-oss:120b` | Ollama model |
| `--ollama-url` | `http://localhost:11434` | Ollama service URL |

### Common Combinations

Chinese -> Chinese, generate only Chinese subtitles:

```bash
python main.py --language zh
```

Chinese -> English, generate Chinese subtitles plus English translated subtitles:

```bash
python main.py --language zh --target-language en
```

English -> Chinese, generate English subtitles plus Chinese translated subtitles:

```bash
python main.py --language en --target-language zh
```

English -> English, generate only English subtitles:

```bash
python main.py --language en
```

## Supported Formats

The project probes audio streams with `ffprobe`, so any format that ffmpeg can decode is supported, including but not limited to:

`.mp4` `.mov` `.mkv` `.avi` `.webm` `.m4v` `.mp3` `.wav` `.m4a` `.flac` `.aac` `.ogg` `.ts`

## Whisper Model Comparison

| Model | Speed | Accuracy |
|-------|-------|----------|
| `mlx-community/whisper-large-v3-mlx` | slower | highest (default) |
| `mlx-community/whisper-large-v3-turbo` | fast | high |
| `mlx-community/whisper-medium-mlx` | faster | medium |

The model is downloaded from Hugging Face and cached locally on first use.

## Notes

- `media/` and `subtitles/` are already in `.gitignore`
- The Docker image does not support MLX acceleration and is only intended for Ollama-related deployment work

## Testing

Run the small `srt_summarizer` unit test suite with:

```bash
python3 -m unittest discover -s test -p 'test_srt_summarizer.py'
```

These tests use very short inputs and mocks, so they do not trigger expensive real summary computation.
