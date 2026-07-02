# srt_summarizer

[English Version](README.md)

读取上层流水线生成的字幕文件：
- `*.zh.srt` 生成中文 summary
- `*.en.srt` 生成英文 summary

程序会剥掉所有 SRT 格式，把纯文本发给本地 Ollama 做摘要，结果保存为对应语言的 `.summary.md` 文件。

## 依赖

```
pip install requests
pip install tiktoken
```

需要本地运行 Ollama，且已拉取 `gpt-oss:120b` 模型。

## Quickstart

从项目根目录运行：

```bash
python srt_summarizer/main.py
```

默认读取 `subtitles/*.zh.srt` 和 `subtitles/*.en.srt`，并生成：

```text
subtitles/video.mp4.zh.summary.md
subtitles/video.mp4.en.summary.md
```

更多示例见 [QUICKSTART.cn.md](QUICKSTART.cn.md)。

## 用法

从项目根目录运行：

```bash
python srt_summarizer/main.py
```

默认读取 `subtitles/*.zh.srt` 和 `subtitles/*.en.srt`，摘要写回同目录。

### 常见组合

只对中文字幕生成中文摘要：

```bash
python srt_summarizer/main.py --input ./subtitles
```

前提是目录里存在 `*.zh.srt`。

只对英文字幕生成英文摘要：

```bash
python srt_summarizer/main.py --input ./subtitles
```

前提是目录里存在 `*.en.srt`。

指定自定义字幕目录和摘要输出目录：

```bash
python srt_summarizer/main.py --input ./subs --output ./summaries
```

指定模型和 Ollama 地址：

```bash
python srt_summarizer/main.py --model gpt-oss:120b --ollama-url http://localhost:11434
```

### 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `--input` | `subtitles/` | `.zh.srt` / `.en.srt` 所在目录 |
| `--output` | 同 `--input` | 摘要输出目录 |
| `--ollama-url` | `http://localhost:11434` | Ollama 地址 |
| `--model` | `gpt-oss:120b` | 使用的模型 |
| `--chunk-size` | `100000` | 每块最大 token 数，基于 `cl100k_base` |

## 分块策略

模型上下文窗口 256k token。  
程序使用 `tiktoken` 的 `cl100k_base` 编码精确统计 token 数。

默认每块 **10 万 token**，留足 prompt 和回复空间。

超过一块时：先逐块摘要，再合并成最终摘要。

## 输出

```
subtitles/
  video.mp4.zh.srt          ← 中文字幕输入
  video.mp4.zh.summary.md   ← 中文摘要输出
  video.mp4.en.srt          ← 英文字幕输入
  video.mp4.en.summary.md   ← 英文摘要输出
```

`.summary.md` 已加入 `.gitignore`，不会提交。

## 测试

运行 `summary` 的小规模单元测试：

```bash
python3 -m unittest discover -s test -p 'test_srt_summarizer.py'
```

这组测试使用很短的输入和 mock，不会真实调用大规模摘要计算。
