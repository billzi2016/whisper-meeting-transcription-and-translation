# Quickstart

[中文版](QUICKSTART.cn.md)

## Default Usage

Run from the project root:

```bash
python srt_summarizer/main.py
```

By default it reads:

- `subtitles/*.zh.srt`
- `subtitles/*.en.srt`

By default it writes:

- `subtitles/*.zh.summary.md`
- `subtitles/*.en.summary.md`

## Common Combinations

Generate a Chinese summary from Chinese subtitles:

```bash
python srt_summarizer/main.py --input ./subtitles
```

Generate an English summary from English subtitles:

```bash
python srt_summarizer/main.py --input ./subtitles
```

Use a custom subtitle directory:

```bash
python srt_summarizer/main.py --input ./subs
```

Use a custom output directory:

```bash
python srt_summarizer/main.py --input ./subs --output ./summaries
```

Set the chunk token limit:

```bash
python srt_summarizer/main.py --chunk-size 100000
```

Specify model and Ollama URL:

```bash
python srt_summarizer/main.py --model gpt-oss:120b --ollama-url http://localhost:11434
```

## Output Example

```text
subtitles/
  meeting.mp4.zh.srt
  meeting.mp4.zh.summary.md
  meeting.mp4.en.srt
  meeting.mp4.en.summary.md
```

## Notes

- `*.zh.srt` produces a Chinese summary
- `*.en.srt` produces an English summary
- Chunking uses `cl100k_base` token counting instead of character-based estimation
