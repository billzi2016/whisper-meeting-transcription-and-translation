# srt_summarizer

[中文版](README.cn.md)

This tool reads subtitle files produced by the main pipeline:

- `*.zh.srt` -> Chinese summary
- `*.en.srt` -> English summary

It strips SRT formatting, sends plain text to local Ollama, and writes the summary back as a language-specific `.summary.md` file.

## Dependencies

```bash
pip install requests
pip install tiktoken
```

You also need a local Ollama service with `gpt-oss:120b` already pulled.

## Quickstart

Run from the project root:

```bash
python srt_summarizer/main.py
```

By default it reads `subtitles/*.zh.srt` and `subtitles/*.en.srt`, then generates:

```text
subtitles/video.mp4.zh.summary.md
subtitles/video.mp4.en.summary.md
```

More examples are in [QUICKSTART.md](QUICKSTART.md).

## Usage

Run from the project root:

```bash
python srt_summarizer/main.py
```

By default, summaries are written back into the same directory.

### Common Combinations

Generate Chinese summaries from Chinese subtitles:

```bash
python srt_summarizer/main.py --input ./subtitles
```

Generate English summaries from English subtitles:

```bash
python srt_summarizer/main.py --input ./subtitles
```

Use a custom subtitle directory and output directory:

```bash
python srt_summarizer/main.py --input ./subs --output ./summaries
```

Specify model and Ollama URL:

```bash
python srt_summarizer/main.py --model gpt-oss:120b --ollama-url http://localhost:11434
```

### Parameters

| Argument | Default | Description |
|----------|---------|-------------|
| `--input` | `subtitles/` | Directory containing `.zh.srt` / `.en.srt` files |
| `--output` | same as `--input` | Summary output directory |
| `--ollama-url` | `http://localhost:11434` | Ollama URL |
| `--model` | `gpt-oss:120b` | Model name |
| `--chunk-size` | `100000` | Max tokens per chunk, based on `cl100k_base` |

## Chunking Strategy

The model context window is 256k tokens.  
The tool uses `tiktoken` with `cl100k_base` for exact token counting.

The default chunk size is **100k tokens**, leaving room for prompts and responses.

If the content exceeds one chunk, the tool summarizes each chunk first and then merges the chunk summaries into a final summary.

## Output

```text
subtitles/
  video.mp4.zh.srt
  video.mp4.zh.summary.md
  video.mp4.en.srt
  video.mp4.en.summary.md
```

`.summary.md` is already ignored by `.gitignore`.

## Testing

Run the small summary unit test suite with:

```bash
python3 -m unittest discover -s test -p 'test_srt_summarizer.py'
```

These tests use very short inputs and mocks, so they do not trigger expensive real summary computation.
