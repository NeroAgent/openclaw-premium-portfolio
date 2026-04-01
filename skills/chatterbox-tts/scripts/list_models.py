#!/usr/bin/env python3
"""
chatterbox-tts list-models — Show available models and languages.
"""

import argparse
import sys

def main():
    parser = argparse.ArgumentParser(description="List available Chatterbox models")
    args = parser.parse_args()

    models = [
        {
            "name": "turbo",
            "size": "350M",
            "languages": ["English"],
            "features": ["Paralinguistic tags", "One-step decoder", "Low VRAM"],
            "best_for": "Voice agents, production, low-latency"
        },
        {
            "name": "multilingual",
            "size": "500M",
            "languages": ["Arabic", "Danish", "German", "Greek", "English", "Spanish", "Finnish", "French", "Hebrew", "Hindi", "Italian", "Japanese", "Korean", "Malay", "Dutch", "Norwegian", "Polish", "Portuguese", "Russian", "Swedish", "Swahili", "Turkish", "Chinese"],
            "features": ["Zero-shot cloning", "23+ languages"],
            "best_for": "Global applications, localization"
        },
        {
            "name": "original",
            "size": "500M",
            "languages": ["English"],
            "features": ["CFG tuning", "Exaggeration control"],
            "best_for": "Creative control, expressive speech"
        }
    ]

    print("=== Chatterbox Models ===\n")
    for m in models:
        print(f"{m['name']} ({m['size']})")
        print(f"  Languages: {', '.join(m['languages'])}")
        print(f"  Features: {', '.join(m['features'])}")
        print(f"  Best for: {m['best_for']}")
        print()

    print("For more info: https://github.com/resemble-ai/chatterbox")

if __name__ == "__main__":
    main()
