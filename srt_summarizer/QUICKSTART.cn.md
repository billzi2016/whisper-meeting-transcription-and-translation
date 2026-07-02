# Quickstart

## 默认用法

从项目根目录运行：

```bash
python srt_summarizer/main.py
```

默认读取：

- `subtitles/*.zh.srt`
- `subtitles/*.en.srt`

默认输出：

- `subtitles/*.zh.summary.md`
- `subtitles/*.en.summary.md`

## 常见组合

中文字幕生成中文摘要：

```bash
python srt_summarizer/main.py --input ./subtitles
```

英文字幕生成英文摘要：

```bash
python srt_summarizer/main.py --input ./subtitles
```

指定自定义字幕目录：

```bash
python srt_summarizer/main.py --input ./subs
```

指定自定义输出目录：

```bash
python srt_summarizer/main.py --input ./subs --output ./summaries
```

指定分块 token 数：

```bash
python srt_summarizer/main.py --chunk-size 100000
```

指定模型和 Ollama 地址：

```bash
python srt_summarizer/main.py --model gpt-oss:120b --ollama-url http://localhost:11434
```

## 输出示例

```text
subtitles/
  meeting.mp4.zh.srt
  meeting.mp4.zh.summary.md
  meeting.mp4.en.srt
  meeting.mp4.en.summary.md
```

## 说明

- `*.zh.srt` 会生成中文摘要
- `*.en.srt` 会生成英文摘要
- 分块按 `cl100k_base` token 统计，不再使用字符数估算
