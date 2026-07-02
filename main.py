#!/usr/bin/env python3
import argparse
import sys
from pathlib import Path

from tqdm import tqdm

from transcribe import DEFAULT_MODEL as DEFAULT_WHISPER_MODEL
from transcribe import find_media_files, transcribe_file
from translate import DEFAULT_MODEL as DEFAULT_OLLAMA_MODEL
from translate import DEFAULT_OLLAMA_URL, translate_srt


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="MLX Whisper 会议转录 + 中英字幕翻译")
    p.add_argument("--input", type=Path, default=Path("media"), metavar="DIR")
    p.add_argument("--output", type=Path, default=Path("subtitles"), metavar="DIR")
    p.add_argument("--force", action="store_true", help="强制重新处理已有字幕")
    p.add_argument("--no-translate", action="store_true", help="只转录，不翻译")
    p.add_argument("--whisper-model", default=DEFAULT_WHISPER_MODEL, metavar="MODEL")
    p.add_argument("--language", choices=["zh", "en"], help="强制指定转录语言")
    p.add_argument("--target-language", choices=["zh", "en"], help="指定翻译目标语言")
    p.add_argument("--ollama-url", default=DEFAULT_OLLAMA_URL, metavar="URL")
    p.add_argument("--ollama-model", default=DEFAULT_OLLAMA_MODEL, metavar="MODEL")
    return p


def main() -> None:
    args = build_parser().parse_args()

    if not args.input.exists():
        print(f"[ERROR] 媒体文件夹不存在: {args.input}")
        sys.exit(1)

    args.output.mkdir(parents=True, exist_ok=True)

    print(f"扫描媒体文件: {args.input}")
    media_files = find_media_files(args.input)

    if not media_files:
        print("未找到任何媒体文件")
        sys.exit(0)

    print(f"找到 {len(media_files)} 个媒体文件\n")
    print(f"Whisper 模型 : {args.whisper_model}")
    if not args.no_translate:
        print(f"翻译模型     : {args.ollama_model} @ {args.ollama_url}")
    print()

    stats = {"ok": 0, "skip": 0, "fail": 0, "translated": 0}

    for i, file_path in enumerate(tqdm(media_files, desc="Total", unit="file"), 1):
        tqdm.write(f"\n[{i}/{len(media_files)}] {file_path.name}")

        result = transcribe_file(
            file_path,
            output_dir=args.output,
            model_name=args.whisper_model,
            language=args.language,
            force=args.force,
        )

        if result is None:
            stats["fail"] += 1
            continue

        srt_path = result["srt_path"]
        language = result.get("language")

        if result["skipped"]:
            tqdm.write(f"  [SKIP] 字幕已存在: {srt_path.name}")
            stats["skip"] += 1
        else:
            tqdm.write(f"  [OK]   转录完成 → {srt_path.name}  (lang={language})")
            stats["ok"] += 1

        if args.no_translate:
            continue

        if not args.target_language:
            tqdm.write("  [SKIP] 未指定翻译目标语言，跳过翻译")
            continue

        if language == args.target_language:
            tqdm.write("  [SKIP] 原始语言与目标语言相同，跳过翻译")
            continue

        target_srt_path = args.output / f"{file_path.name}.{args.target_language}.srt"
        if target_srt_path.exists() and not args.force:
            tqdm.write(f"  [SKIP] 目标语言字幕已存在: {target_srt_path.name}")
            continue

        ok = translate_srt(
            srt_path,
            target_srt_path,
            args.target_language,
            args.ollama_url,
            args.ollama_model,
        )
        if ok:
            tqdm.write(f"  [OK]   翻译完成 → {target_srt_path.name}")
            stats["translated"] += 1
        else:
            tqdm.write("  [WARN] 翻译失败")

    print(f"\n{'='*50}")
    print(
        f"完成！  转录 {stats['ok']}  翻译 {stats['translated']}"
        f"  跳过 {stats['skip']}  失败 {stats['fail']}"
    )


if __name__ == "__main__":
    main()
