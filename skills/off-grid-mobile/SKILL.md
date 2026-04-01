---
name: off-grid-mobile
description: "Complete offline AI suite for mobile: text generation, image generation, vision AI, voice transcription, document analysis. All on-device, zero data leaves your phone. Supports GGUF models, Stable Diffusion, SmolVLM, Whisper. Use when you need full AI capabilities without cloud dependency. Requires Android device with NPU or decent CPU."
---

# Off Grid Mobile

## Overview

`off-grid-mobile` is a comprehensive offline AI application for Android (and iOS). It bundles:

- **Text generation** — Run LLMs (Qwen 3, Llama 3.2, Gemma 3, Phi-4) in GGUF format; streaming, thinking mode
- **Image generation** — On-device Stable Diffusion with NPU acceleration; 20+ models
- **Vision AI** — Multi-modal: point camera at anything, ask questions; uses SmolVLM, Qwen3-VL, Gemma 3n
- **Voice transcription** — On-device Whisper; hold to record, no audio leaves device
- **Document analysis** — Attach PDFs, code, CSVs to conversations

**Designed for:** True offline AI companion on mobile hardware. No internet required after initial app install.

## Quick Start

```bash
# 1. Install the app on your Android device
# From Google Play: "Off Grid Mobile"
# Or download APK from GitHub releases

# 2. (Optional) Load custom GGUF model onto device
# Place in: /sdcard/offgrid/models/

# 3. Control from OpenClaw via ADB (if needed)
adb shell am start -n ai.offgridmobile/.MainActivity
```

## Capabilities

### 1. Text Generation

Choose from supported models (multi-lingual). Configurable context size, temperature. Supports thinking mode (chain-of-thought).

### 2. Image Generation

Stable Diffusion with ControlNet support. NPU-accelerated on Snapdragon (5-10s/image). Real-time preview.

### 3. Vision AI

Live camera mode or image upload. Ask questions about what the camera sees. Document scanning + Q&A.

### 4. Voice Input

Hold-to-record button. Whisper transcribes on-device instantly.

### 5. Document Attachment

Within a conversation, attach any file (PDF, code, CSV). The app extracts text and answers questions about it.

## Integration with OpenClaw

Since the app runs on the Android device, OpenClaw can interact via:

- **ADB** — send commands, start activities, push files
- **Local API** (if enabled) — HTTP server on device for programmatic control
- **File sync** — drop prompts into a watched folder, get results out

Example: Use `agentmail` to receive a query, forward to off-grid-mobile via ADB, get result, reply.

## Performance

- **Flagship device:** 15-30 tok/s (text), 5-10s/image (SD), ~7s for vision inference
- **Mid-range:** 5-10 tok/s, 15-20s/image
- **NPU utilization:** Significant speedup on Snapdragon 8 Gen 2+, MediaTek Dimensity 9000+

## Use Cases

- **Field work:** No connectivity, need AI assistance
- **Privacy-sensitive:** Medical, legal, personal notes — data never leaves device
- **Low-latency:** No network round-trip
- **Cost-free:** After app purchase (free), no API charges

## Installation

From Google Play Store (recommended) or build from source (requires Flutter/Dart).

**Note:** This is primarily a mobile app, not a CLI tool. OpenClaw integration is via ADB or local HTTP API (if enabled in settings).

## Configuration

Within the app:
- Model directory: `/sdcard/offgrid/models/`
- Default model: Qwen3-4B-Q4 (recommended for balance)
- Enable NPU: Settings → Acceleration → NPU (if available)

## Resources

### references/
- `adb_commands.md` — How to control the app via ADB
- `models.md` — Supported GGUF models and where to get them
- `api.md` — Local HTTP API (if enabled) for programmatic access
- `npu_acceleration.md` — NPU setup and performance tuning

---

**Note:** Off Grid Mobile is developed by Ali Cherawalla and community. This skill provides integration notes for using it with OpenClaw. For app-specific issues, see upstream: https://github.com/alichherawalla/off-grid-mobile

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
