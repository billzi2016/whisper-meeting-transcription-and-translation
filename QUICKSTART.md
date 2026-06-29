# Quickstart

## 默认自动识别

Whisper 默认会自动检测音频语言：

```bash
python main.py
```

## 强制中文

当音频本来是中文，但自动识别错成英文时，可以强制指定中文：

```bash
python main.py --language zh
```

## 强制英文

当音频本来是英文，或者你希望跳过自动检测时，可以强制指定英文：

```bash
python main.py --language en
```

## 常见组合

只生成中文原文字幕，不做翻译：

```bash
python main.py --language zh --no-translate
```

适用于音频本身就是中文，你只想拿到中文转录结果，不需要再生成 `.zh.srt` 翻译文件。

只生成英文原文字幕，不做翻译：

```bash
python main.py --language en --no-translate
```

适用于音频本身就是英文，你只想保留英文转录结果，不需要立刻生成中文字幕。

指定自定义媒体目录和输出目录，并强制按中文转录：

```bash
python main.py --input ./my_videos --output ./subs --language zh
```

适用于你的媒体文件不放在默认 `media/` 目录里，或者你希望把字幕输出到单独目录时使用。
