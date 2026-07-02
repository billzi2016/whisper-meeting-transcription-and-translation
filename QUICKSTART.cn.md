# Quickstart

## 默认自动识别

Whisper 默认会自动检测音频语言，并输出对应语言后缀的字幕文件：

```bash
python main.py
```

## 强制中文视频

当音频本来是中文，但自动识别错成英文时，可以强制指定中文：

```bash
python main.py --language zh
```

## 强制英文视频

当音频本来是英文，或者你希望跳过自动检测时，可以强制指定英文：

```bash
python main.py --language en
```

## 常见组合

中 -> 中，只生成中文字幕：

```bash
python main.py --language zh
```

适用于音频本身就是中文，只需要 `xxx.zh.srt`。

中 -> 英，生成中文字幕和英文翻译字幕：

```bash
python main.py --language zh --target-language en
```

适用于中文视频，需要额外得到 `xxx.en.srt`。

英 -> 中，生成英文字幕和中文字幕：

```bash
python main.py --language en --target-language zh
```

适用于英文视频，需要额外得到 `xxx.zh.srt`。

英 -> 英，只生成英文字幕：

```bash
python main.py --language en
```

适用于音频本身就是英文，只需要 `xxx.en.srt`。

指定自定义媒体目录和输出目录，并强制按中文转录后翻译成英文：

```bash
python main.py --input ./my_videos --output ./subs --language zh --target-language en
```

适用于你的媒体文件不放在默认 `media/` 目录里，或者你希望把字幕输出到单独目录时使用。
