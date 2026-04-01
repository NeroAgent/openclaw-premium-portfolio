---
name: ollama
description: "Run and manage local LLMs via Ollama. Use to serve open-source models (Llama, Qwen, Mistral, etc.), generate completions, create embeddings, and manage model lifecycles. Integrates with OpenClaw for on-device AI inference without cloud dependencies. Works offline and fully controllable. Requires 'ollama' binary in PATH."
---

# Ollama

## Overview

`ollama` wraps the [Ollama](https://github.com/ollama/ollama) binary for local large language model serving. It allows OpenClaw to:

- **Run LLMs locally** — no API costs, no internet required after download
- **Switch models on demand** — Llama 3, Qwen, Mistral, Gemma, CodeLlama, etc.
- **Generate text** — completions, chat, structured output
- **Create embeddings** — for RAG and semantic search
- **Manage models** — pull, list, delete, copy

**Designed for:** Resource-constrained environments (Termux/Android) where cloud APIs are expensive or unavailable. Ideal for coding agents that need a local brain.

## Quick Start

```bash
# 1. Install ollama binary (if not present)
# On Termux (ARM64): download from https://github.com/ollama/ollama/releases
# Or build from source (requires Go 1.21+)
# Place binary in ~/.local/bin or /usr/local/bin

# 2. Start the ollama daemon (runs in background)
ollama serve &

# 3. Pull a model (first time only)
ollama pull llama3.2:3b  # small, mobile-friendly

# 4. Generate a completion
ollama generate llama3.2:3b "What is OpenClaw?"

# 5. Or use chat mode (interactive)
ollama chat llama3.2:3b
```

**From OpenClaw tools:**
```bash
tool("ollama", "generate", model="llama3.2:3b", prompt="Explain Rust in 3 sentences")
tool("ollama", "list-models")
tool("ollama", "pull", model="qwen2.5:3b")
```

## Capabilities

### 1. Model Management

```bash
ollama list-models              # Show downloaded models
ollama pull <model>             # Download a model (e.g., llama3.2:3b)
ollama rm <model>               # Remove a model to free space
ollama show <model>             # Show model details (parameters, size)
```

**Common models for mobile:**
- `llama3.2:3b` — 3B params, ~2GB, decent quality
- `qwen2.5:3b` — Alibaba's 3B, multilingual
- `gemma:2b` — Google's 2B, lightweight
- `mistral:7b` — 7B, higher quality but ~4GB

### 2. Text Generation

```bash
ollama generate <model> "<prompt>"
```

Options:
- `--system "<system prompt>"` — Set system message
- `--template "<mustache template>"` — Customize prompt format
- `--format json` — Force JSON output (if model supports)
- `--raw` — Raw mode (no chat formatting)
- `--stream` — Stream output token-by-token

**Example:**
```bash
ollama generate llama3.2:3b --system "You are a helpful assistant." "What's the capital of France?"
```

### 3. Chat Mode

Interactive REPL:
```bash
ollama chat llama3.2:3b
```

Sessions can be saved and resumed.

### 4. Embeddings

Generate vector embeddings for RAG:
```bash
ollama embed <model> "text to embed"
```

Useful for semantic search over documents.

### 5. API Server

`ollama serve` starts the REST API on `http://localhost:11434`. OpenClaw skills can call it directly via HTTP if needed, bypassing the CLI wrapper.

## Integration with OpenClaw

The `ollama` skill provides:

- `list_models.py` — enumerate available models
- `pull.py` — download a model
- `generate.py` — single completion
- `chat.py` — interactive chat (for manual use)
- `embed.py` — embeddings
- `serve.py` — start/stop daemon

**Example tool call:**
```bash
tool("ollama", "generate", model="llama3.2:3b", prompt="Summarize this code: ...", system="You are a senior engineer.")
```

## Resource Considerations

- **Disk space:** Models range from 2GB (2B params) to 20GB+ (70B). Choose mobile-friendly sizes.
- **RAM:** Model size * 2 (approx). A 3B model needs ~6GB during inference. On Termux with limited RAM, use 2-3B models only.
- **CPU/GPU:** Ollama uses CPU by default. If you have GPU (CUDA, Metal, ROCm), it will auto-detect and accelerate.
- **Performance:** 3B models: ~10 tokens/sec on mid-range phone CPU. 7B: ~4 tokens/sec.

**Tip:** Use `lean-ctx` to compress prompts before sending to ollama, saving memory and tokens.

## Use Cases

- **Local coding assistant** — no cloud latency, no API keys
- **Offline work** — travel, remote areas
- **Privacy** — data never leaves device
- **Cost control** — no per-token charges

## Installation on Termux/Android

1. Download prebuilt ARM64 binary:
   ```bash
   wget https://github.com/ollama/ollama/releases/download/v0.19.0-rc2/ollama-linux-arm64
   chmod +x ollama-linux-arm64
   mv ollama-linux-arm64 ~/.local/bin/ollama
   ```

2. Start daemon:
   ```bash
   ollama serve &
   ```

3. Pull a model:
   ```bash
   ollama pull llama3.2:3b
   ```

**Note:** The binary is single-threaded by default; you can adjust `OLLAMA_NUM_PARALLEL` env var.

## Troubleshooting

**"binary not found"**
- Ensure ~/.local/bin or /usr/local/bin is in PATH
- Or set `OLLAMA_BIN` environment variable to full path

**"Cannot allocate memory"**
- Model too large for available RAM. Use smaller model (2B or 3B).
- Close other apps to free memory.
- Consider using swap (but performance will suffer).

**"GPU not detected"**
- Termux doesn't expose GPU to userland. Ollama will use CPU only.
- On a laptop with NVIDIA, ensure CUDA drivers installed.

**Slow inference**
- Expected on mobile CPU. Reduce model size.
- Batch multiple prompts if possible.

## Resources

### scripts/
- `list_models.py` — List downloaded models with sizes
- `pull.py` — Download a model with progress
- `generate.py` — Generate text completion
- `embed.py` — Generate embeddings
- `serve.py` — Start/stop/check daemon status
- `rm.py` — Remove a model

### references/
- `models.md` — Recommended models for mobile and desktop
- `api.md` — HTTP API reference (for direct integration)
- `optimization.md` — Tips for speed and memory optimization

---

**Note:** Ollama is developed by the Ollama team. This skill wraps the CLI; refer to upstream docs for advanced features (modelfiles, adapters, etc.).

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
