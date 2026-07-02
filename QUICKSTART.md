# Quickstart

[中文版](QUICKSTART.cn.md)

## Auto Detection

Whisper detects the audio language automatically and writes subtitles with the matching language suffix:

```bash
python main.py
```

## Force Chinese Source Audio

If the audio is Chinese and auto detection gets it wrong, force Chinese:

```bash
python main.py --language zh
```

## Force English Source Audio

If the audio is English, or you want to skip auto detection, force English:

```bash
python main.py --language en
```

## Common Combinations

Chinese -> Chinese, generate only Chinese subtitles:

```bash
python main.py --language zh
```

Use this when the source audio is Chinese and you only need `xxx.zh.srt`.

Chinese -> English, generate Chinese subtitles and English translated subtitles:

```bash
python main.py --language zh --target-language en
```

Use this when the source audio is Chinese and you also need `xxx.en.srt`.

English -> Chinese, generate English subtitles and Chinese translated subtitles:

```bash
python main.py --language en --target-language zh
```

Use this when the source audio is English and you also need `xxx.zh.srt`.

English -> English, generate only English subtitles:

```bash
python main.py --language en
```

Use this when the source audio is English and you only need `xxx.en.srt`.

Use a custom media folder and output folder, transcribe as Chinese, then translate to English:

```bash
python main.py --input ./my_videos --output ./subs --language zh --target-language en
```
