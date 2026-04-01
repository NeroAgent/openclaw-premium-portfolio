#!/usr/bin/env python3
"""
chatterbox-tts batch — Batch generate from a list.
"""

import argparse
import os
import sys
from pathlib import Path

def check_dependencies():
    try:
        import torch
        import chatterbox
        return True
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e.name}", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Batch TTS generation")
    parser.add_argument("--input-list", required=True, help="File containing prompts, one per line")
    parser.add_argument("--ref-voice", required=True, help="Reference voice audio")
    parser.add_argument("--output-dir", required=True, help="Directory to save outputs")
    parser.add_argument("--model", default="turbo", choices=["turbo", "multilingual", "original"])
    parser.add_argument("--lang", help="Language for multilingual")
    parser.add_argument("--prefix", default="tts", help="Filename prefix (e.g., track)")
    args = parser.parse_args()

    if not check_dependencies():
        return 1

    # Read prompts
    with open(args.input_list, 'r') as f:
        prompts = [line.strip() for line in f if line.strip()]

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Processing {len(prompts)} prompts...")

    # Lazy import to avoid loading model until needed
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox.tts import ChatterboxTTS
    import torchaudio as ta
    import torch

    device = "cuda" if torch.cuda.is_available() else "cpu"

    # Load model once
    try:
        if args.model == "turbo":
            model = ChatterboxTurboTTS.from_pretrained(device=device)
        elif args.model == "multilingual":
            model = ChatterboxMultilingualTTS.from_pretrained(device=device)
        else:
            model = ChatterboxTTS.from_pretrained(device=device)
    except Exception as e:
        print(f"[ERROR] Model load failed: {e}", file=sys.stderr)
        return 1

    # Generate each
    for i, text in enumerate(prompts):
        out_path = out_dir / f"{args.prefix}_{i:04d}.wav"
        try:
            if args.model == "multilingual" and args.lang:
                wav = model.generate(text, audio_prompt_path=args.ref_voice, language_id=args.lang)
            else:
                wav = model.generate(text, audio_prompt_path=args.ref_voice)
            ta.save(str(out_path), wav, model.sr)
            print(f"[{i+1}/{len(prompts)}] OK: {text[:50]}... -> {out_path}")
        except Exception as e:
            print(f"[{i+1}/{len(prompts)}] ERROR: {e}")

    print("[INFO] Batch complete")
    return 0

if __name__ == "__main__":
    sys.exit(main())
