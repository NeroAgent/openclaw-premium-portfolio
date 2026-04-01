# Troubleshooting

## Common Issues

### "No module named 'torch'"

**Cause:** PyTorch not installed or wrong environment.

**Fix:**
```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
# or for CUDA:
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### "CUDA out of memory"

**Cause:** GPU doesn't have enough VRAM for the model.

**Fix:**
- Use CPU: `--device cpu`
- Reduce model size: use Turbo (350M) instead of Multilingual (500M)
- Close other GPU applications

### "Could not find a version that satisfies the requirement torch"

**Cause:** Running on an unsupported platform (e.g., ARM Android/Termux) or Python version mismatch.

**Fix:** PyTorch does not provide ARM64 builds for Android/Termux. You need to run chatterbox on a machine with x86_64 CPU (Intel/AMD) or ARM64 macOS. Consider using a VPS or your laptop.

If on Termux, this skill will not work. Use a cloud TTS API instead (ElevenLabs, OpenAI, Google).

### "Audio file not read" or "Soundfile runtime"

**Cause:** Missing `soundfile` or `libsndfile`.

**Fix:**
```bash
apt-get install libsndfile1  # Debian/Ubuntu
# or on macOS: brew install libsndfile
pip install soundfile
```

### "Model weights not found"

**Cause:** Chatterbox downloads models on first use; network issues or permission errors.

**Fix:**
- Ensure internet connectivity on first run
- Set `HF_HOME` to a writable directory if you have permission issues
- Check disk space (~1GB for model cache)

### Bad audio quality / robotic voice

**Possible reasons:**
- Reference audio is low quality (noisy, short, mismatched language)
- Text contains unusual characters or non-matching language
- Model cfg_weight/exaggeration settings not tuned

**Fix:**
- Use a clean 10s reference, same language as text
- Try default settings first (`exaggeration=0.5`, `cfg_weight=0.5` for original model)
- For Turbo, ensure reference matches target voice characteristics

### Watermark extraction fails

**Cause:** Output was modified or the watermarker expects specific sample rate.

**Fix:** The watermark is robust but not indestructible. Re-encode may weaken it. Use original file for detection.

---

## Getting Help

- Upstream Issues: https://github.com/resemble-ai/chatterbox/issues
- Discord: https://discord.gg/rJq9cRJBJ6

When reporting issues, include:
- OS and Python version
- Model you're using (Turbo/Multilingual/Original)
- Error messages and stack traces
- Sample command line