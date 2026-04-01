#!/usr/bin/env python3
"""
chatterbox-tts install — Check and guide installation.
"""

import argparse
import sys
import subprocess

def main():
    parser = argparse.ArgumentParser(description="Check chatterbox-tts installation and dependencies")
    args = parser.parse_args()

    print("[INFO] Checking dependencies...\n")

    # Check Python
    import platform
    py_ver = platform.python_version()
    py_ok = py_ver.startswith("3.11")
    print(f"Python: {py_ver} {'✅' if py_ok else '⚠️  (3.11 recommended)'}")

    # Check PyTorch
    try:
        import torch
        torch_ver = torch.__version__
        cuda_available = torch.cuda.is_available()
        print(f"PyTorch: {torch_ver} {'✅' if cuda_available else '✅ (CPU)'}")
    except ImportError:
        print("PyTorch: ❌ Not installed")
        print("  → Install: pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu")
        return 1

    # Check chatterbox
    try:
        import chatterbox
        print("chatterbox-tts: ✅ Installed")
    except ImportError:
        print("chatterbox-tts: ❌ Not installed")
        print("  → Install: pip install chatterbox-tts")
        return 1

    print("\n[OK] chatterbox-tts is ready to use.")
    print("\nQuick test:")
    print("  chatterbox-tts generate 'Hello world' --ref-voice reference.wav --output test.wav")
    return 0

if __name__ == "__main__":
    sys.exit(main())
