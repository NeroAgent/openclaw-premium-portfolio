---
name: chatterbox-tts
description: "High-quality, open-source text-to-speech with voice cloning and paralinguistic tags. Use for generating speech audio from text, creating custom voices from reference clips, and adding expressive tags like [laugh], [cough]. Supports Chatterbox-Turbo (350M, English), Multilingual (23 languages), and original models. Requires Python 3.11 and PyTorch. Ideal for voice agents, narration, and creative workflows."
---

# Chatterbox TTS

## Overview

`chatterbox-tts` wraps the [Chatterbox](https://github.com/resemble-ai/chatterbox) family of state-of-the-art TTS models by Resemble AI. It provides:

- **Chatterbox-Turbo** — 350M parameter model, English only, ultra-fast (single-step decoder), paralinguistic tags (`[laugh]`, `[chuckle]`, `[cough]`)
- **Chatterbox-Multilingual** — 500M, supports 23+ languages, zero-shot voice cloning
- **Original Chatterbox** — 500M, English, CFG & exaggeration tuning for creative control

**Designed for:** Voice agents, narration, synthetic speech with natural expressiveness.

## Quick Start

```bash
# 1. Install dependencies (Python 3.11 + PyTorch)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
pip install chatterbox-tts

# 2. Generate speech with Turbo model (requires a reference audio for voice cloning)
chatterbox-tts generate "Hello, this is Nero speaking." --ref-voice your_10s_clip.wav --output hello.wav

# 3. Use paralinguistic tags
chatterbox-tts generate "Hi there! [chuckle] How are you?" --ref-voice your_clip.wav

# 4. Multilingual example (French)
chatterbox-tts generate "Bonjour!" --model multilingual --lang fr --ref-voice fr_clip.wav
```

## Capabilities

### 1. Text-to-Speech Generation

```bash
chatterbox-tts generate <text> [options]
```

**Options:**
- `--ref-voice <path>` — Path to 10-second reference audio clip (WAV/MP3) for voice cloning. Required for Turbo; optional for others (but quality improves with reference).
- `--output <path>` — Output file (default: `output.wav`)
- `--model` — `turbo` (default), `multilingual`, or `original`
- `--lang` — Language code for multilingual (e.g., `fr`, `zh`, `ja`, `es`)
- `--exaggeration <0-1>` — For original/Chatterbox only. Higher = more expressive (default: 0.5)
- `--cfg-weight <0-1>` — Controls pacing & adherence to reference (default: 0.5)
- `--device` — `cuda` or `cpu` (default auto)
- `--sample-rate` — Output sample rate (default: model's native)

**Example:**
```bash
chatterbox-tts generate "Welcome to OpenClaw!" --ref-voice ~/voices/narrator.wav --output welcome.wav --exaggeration 0.7
```

### 2. Voice Cloning

To clone a voice, provide a clean 10-second audio sample of the target speaker. The sample should:
- Be WAV or MP3 format
- Have clear speech, minimal background noise
- Ideally match the language and emotional tone of intended use

The model will mimic that voice's timbre, pitch, and cadence.

**Note:** This is zero-shot cloning — no training required. Just inference.

### 3. Paralinguistic Tags (Turbo Only)

Insert tags in the text to add expressive sounds:

- `[cough]`
- `[laugh]`
- `[chuckle]`
- `[sigh]`
- `[yawn]`
- `[sniff]`
- `[clears throat]`

These are interpreted natively by Turbo and add realism.

**Example:**
```
"Hello! [laugh] That's actually pretty funny. [cough] Sorry, I have a cold."
```

### 4. Batch Generation

Generate multiple audio files from a list:

```bash
chatterbox-tts batch --input-list prompts.txt --ref-voice voice.wav --output-dir audios/
```

`prompts.txt` format: one line per prompt.

## Installation

### Requirements

- **Python**: 3.11 (tested)
- **OS**: Linux (Debian/Ubuntu), macOS, Windows (WSL)
- **PyTorch**: Install with pip (CPU or CUDA)
- **pip packages**: `torch`, `torchaudio`, `chatterbox-tts`

### Termux Limitation

PyTorch does not provide official ARM64 builds for Android/Termux. The `chatterbox-tts` skill will **not** install on Termux. Use on a workstation, laptop, or cloud VM instead.

If you attempt to run on Termux, the skill will detect missing dependencies and report a helpful error.

### Desktop/VPS Setup

```bash
# Create virtual environment (recommended)
python3.11 -m venv ~/.venv/chatterbox
source ~/.venv/chatterbox/bin/activate

# Install PyTorch (CPU)
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu

# Install chatterbox-tts
pip install chatterbox-tts

# Verify
chatterbox-tts --help
```

### GPU Acceleration (Optional)

If you have CUDA:

```bash
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu118
```

Then use `--device cuda` for faster generation (~10x speedup).

## Usage with OpenClaw

Once installed on a capable machine, the skill provides scripts:

- `generate.py` — Single TTS generation
- `batch.py` — Batch processing
- `list_voices.py` — Show available reference voices (if any)

**Example call from OpenClaw:**
```bash
tool("chatterbox-tts", "generate", text="Hello, Sol!", ref_voice="~/voices/narrator.wav", output="hello.wav")
```

## Choosing a Voice for Nero

Since you offered to pick something for me — that's thoughtful. I don't have a built-in voice yet. Options:

1. **Record your own voice** as reference — clean 10 seconds of speech. That would make Nero sound like you (Operator). That could be a nice touch, though requires careful handling of voice data (privacy).

2. **Pick a generic narrator style** — Use a stock reference clip from a creative commons source (e.g., audiobook narrator). Could go for:
   - Warm, deep, articulate (like a radio host)
   - Crisp, technical, clear (like a engineer)
   - Friendly, conversational (like a podcast host)

3. **Try multiple and test** — Generate samples with different reference clips and decide.

I'd need you to provide a WAV file (10s, clean speech) if you want to clone your voice. Otherwise, I could suggest finding a reference from public domain narrations.

## Notes

- Watermarking: All outputs include Perth watermarks (imperceptible, detectable for provenance).
- Licensing: AGPL-3.0 — same as upstream.
- For production use, consider Resemble's hosted API (sub-200ms latency).

## Resources

### scripts/
- `generate.py` — TTS generation wrapper
- `batch.py` — Batch processing
- `install.py` — Check dependencies, guide installation
- `list_models.py` — Show available models and languages

### references/
- `models.md` — Model comparisons and capabilities
- `voice_cloning_guide.md` — How to prepare reference audio
- `tags_reference.md` — Full list of paralinguistic tags
- `troubleshooting.md` — Common issues (PyTorch, CUDA, audio formats)

---

**Next step:** Decide on a reference voice (if you want Nero to have a consistent voice). Then we'll install chatterbox-tts on a proper machine and test.

## Structuring This Skill

[TODO: Choose the structure that best fits this skill's purpose. Common patterns:

**1. Workflow-Based** (best for sequential processes)
- Works well when there are clear step-by-step procedures
- Example: DOCX skill with "Workflow Decision Tree" -> "Reading" -> "Creating" -> "Editing"
- Structure: ## Overview -> ## Workflow Decision Tree -> ## Step 1 -> ## Step 2...

**2. Task-Based** (best for tool collections)
- Works well when the skill offers different operations/capabilities
- Example: PDF skill with "Quick Start" -> "Merge PDFs" -> "Split PDFs" -> "Extract Text"
- Structure: ## Overview -> ## Quick Start -> ## Task Category 1 -> ## Task Category 2...

**3. Reference/Guidelines** (best for standards or specifications)
- Works well for brand guidelines, coding standards, or requirements
- Example: Brand styling with "Brand Guidelines" -> "Colors" -> "Typography" -> "Features"
- Structure: ## Overview -> ## Guidelines -> ## Specifications -> ## Usage...

**4. Capabilities-Based** (best for integrated systems)
- Works well when the skill provides multiple interrelated features
- Example: Product Management with "Core Capabilities" -> numbered capability list
- Structure: ## Overview -> ## Core Capabilities -> ### 1. Feature -> ### 2. Feature...

Patterns can be mixed and matched as needed. Most skills combine patterns (e.g., start with task-based, add workflow for complex operations).

Delete this entire "Structuring This Skill" section when done - it's just guidance.]

## [TODO: Replace with the first main section based on chosen structure]

[TODO: Add content here. See examples in existing skills:
- Code samples for technical skills
- Decision trees for complex workflows
- Concrete examples with realistic user requests
- References to scripts/templates/references as needed]

## Resources (optional)

Create only the resource directories this skill actually needs. Delete this section if no resources are required.

### scripts/
Executable code (Python/Bash/etc.) that can be run directly to perform specific operations.

**Examples from other skills:**
- PDF skill: `fill_fillable_fields.py`, `extract_form_field_info.py` - utilities for PDF manipulation
- DOCX skill: `document.py`, `utilities.py` - Python modules for document processing

**Appropriate for:** Python scripts, shell scripts, or any executable code that performs automation, data processing, or specific operations.

**Note:** Scripts may be executed without loading into context, but can still be read by Codex for patching or environment adjustments.

### references/
Documentation and reference material intended to be loaded into context to inform Codex's process and thinking.

**Examples from other skills:**
- Product management: `communication.md`, `context_building.md` - detailed workflow guides
- BigQuery: API reference documentation and query examples
- Finance: Schema documentation, company policies

**Appropriate for:** In-depth documentation, API references, database schemas, comprehensive guides, or any detailed information that Codex should reference while working.

### assets/
Files not intended to be loaded into context, but rather used within the output Codex produces.

**Examples from other skills:**
- Brand styling: PowerPoint template files (.pptx), logo files
- Frontend builder: HTML/React boilerplate project directories
- Typography: Font files (.ttf, .woff2)

**Appropriate for:** Templates, boilerplate code, document templates, images, icons, fonts, or any files meant to be copied or used in the final output.

---

**Not every skill requires all three types of resources.**
