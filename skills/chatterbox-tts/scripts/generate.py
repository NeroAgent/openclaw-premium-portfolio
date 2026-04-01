#!/usr/bin/env python3
"""
chatterbox-tts generate — Generate speech from text.
"""

import argparse
import os
import sys
import subprocess
import json

def check_dependencies():
    """Check if torch and chatterbox are available."""
    try:
        import torch
        import chatterbox
        return True
    except ImportError as e:
        print(f"[ERROR] Missing dependency: {e.name}", file=sys.stderr)
        print("Install with: pip install torch torchaudio chatterbox-tts", file=sys.stderr)
        return False

def main():
    parser = argparse.ArgumentParser(description="Generate TTS audio with Chatterbox")
    parser.add_argument("text", help="Text to synthesize")
    parser.add_argument("--ref-voice", required=True, help="Path to reference voice audio (10s WAV/MP3)")
    parser.add_argument("--output", default="output.wav", help="Output file path")
    parser.add_argument("--model", choices=["turbo", "multilingual", "original"], default="turbo",
                        help="Model to use (default: turbo)")
    parser.add_argument("--lang", help="Language code for multilingual (e.g., fr, zh, es)")
    parser.add_argument("--exaggeration", type=float, default=0.5,
                        help="Exaggeration level 0-1 (for original model)")
    parser.add_argument("--cfg-weight", type=float, default=0.5,
                        help="CFG weight 0-1 (affects pacing)")
    parser.add_argument("--device", choices=["cuda", "cpu"], default=None,
                        help="Device (default: auto)")
    parser.add_argument("--sample-rate", type=int, default=24000,
                        help="Output sample rate (default: 24000)")
    args = parser.parse_args()

    if not check_dependencies():
        return 1

    # Import here after check
    from chatterbox.tts_turbo import ChatterboxTurboTTS
    from chatterbox.mtl_tts import ChatterboxMultilingualTTS
    from chatterbox.tts import ChatterboxTTS
    import torchaudio as ta

    # Determine device
    device = args.device or ("cuda" if torch.cuda.is_available() else "cpu")

    # Load model
    try:
        if args.model == "turbo":
            model = ChatterboxTurboTTS.from_pretrained(device=device)
        elif args.model == "multilingual":
            model = ChatterboxMultilingualTTS.from_pretrained(device=device)
        else:
            model = ChatterboxTTS.from_pretrained(device=device)
    except Exception as e:
        print(f"[ERROR] Failed to load model: {e}", file=sys.stderr)
        return 1

    # Generate
    try:
        if args.model == "multilingual" and args.lang:
            wav = model.generate(args.text, audio_prompt_path=args.ref_voice, language_id=args.lang)
        else:
            wav = model.generate(args.text, audio_prompt_path=args.ref_voice)
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}", file=sys.stderr)
        return 1

    # Save
    try:
        ta.save(args.output, wav, model.sr)
        print(f"[OK] Saved to {args.output}")
        return 0
    except Exception as e:
        print(f"[ERROR] Save failed: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main())
