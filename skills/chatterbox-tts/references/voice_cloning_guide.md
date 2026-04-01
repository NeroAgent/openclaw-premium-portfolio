# Voice Cloning Guide

## Preparing a Reference Voice

To generate speech with a specific voice, you need a **reference audio clip**:

- **Length:** 10-30 seconds (10s is ideal)
- **Format:** WAV or MP3 (WAV preferred for quality)
- **Sample rate:** 16kHz or higher (model resamples internally)
- **Content:** Clear, articulate speech. Minimal background noise, no music.
- **Single speaker:** No overlapping voices or interruptions.
- **Emotional tone:** Should match intended use (cheerful for assistant, calm for narration, etc.)

**Recording tips:**
- Use a decent microphone (not phone speaker)
- Speak naturally, at normal pace
- Avoid mouth sounds, pops, breaths
- Record in a quiet room

### Splitting a longer audio

If you only have a longer recording, use `ffmpeg` to extract a 10s segment:

```bash
ffmpeg -i input.mp3 -ss 00:00:15 -t 10 -c copy reference.wav
```

## How It Works

Chatterbox uses **zero-shot voice cloning**:
- The reference audio is encoded into a voice embedding
- The TTS model conditions on that embedding to produce speech in that voice
- No fine-tuning or training needed

Quality depends on reference clarity. With a good reference, the output will closely match voice characteristics.

## Privacy & Ethics

- Only use reference audio you own or have permission to use.
- Voice cloning can be misused; respect others' voice rights.
- The model includes Perth watermarks to detect generated audio.

---

For technical details, see the upstream docs: https://github.com/resemble-ai/chatterbox