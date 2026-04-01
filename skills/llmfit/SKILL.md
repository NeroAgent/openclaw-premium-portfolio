---
name: llmfit
description: "Find the right LLM model for your hardware. Use to detect system capabilities (RAM, CPU, GPU), match models that will run on your device, and get recommendations for optimal performance. Supports 206 models across 57 providers. Ideal for selecting models for Ollama, HuggingFace, or local inference on resource-constrained environments like Termux/Android."
---

# llmfit

## Overview

`llmfit` is a hardware-aware LLM model selector. It analyzes your system (RAM, CPU cores, GPU) and scores 200+ models across four dimensions:

- **Quality** — model's capability (based on benchmarks)
- **Speed** — expected tokens/sec on your hardware
- **Fit** — whether model fits in memory (RAM/GPU)
- **Context** — max context window you can support

**Designed for:** Choosing the right model size before downloading gigabytes. Avoid wasted downloads and runtime OOMs.

## Quick Start

```bash
# 1. Install llmfit binary
cargo install llmfit   # or use prebuilt from install.sh

# 2. Run hardware scan (interactive TUI by default)
llmfit

# 3. Or use CLI mode for scripting
llmfit --format json | jq '.models[] | select(.fit=="✅")'
```

## Modes

### Interactive TUI (default)

```bash
llmfit
```

Shows a full-screen interface with sortable columns, filtering, and model details. Use arrow keys, Enter to select.

### CLI Mode

```bash
llmfit --format json               # Full data as JSON
llmfit --format table              # ASCII table
llmfit --provider ollama           # Filter to Ollama-compatible models
llmfit --min-quality 0.7           # Filter by quality threshold
llmfit --sort speed                # Sort by expected speed
```

**Example:** Find the fastest model that fits in 4GB RAM:
```bash
llmfit --format json | jq '[.models[] | select(.fit=="✅" and .ram_required<4)] | sort_by(.speed) | reverse | first'
```

## Output Columns

| Column | Meaning |
|--------|---------|
| Model | Model name (e.g., `llama3.2:3b`) |
| Provider | Source (ollama, huggingface, etc.) |
| Quality | 0-1 score from benchmarks |
| Speed | Est. tokens/sec on your hardware |
| Fit | ✅ fits, ⚠️ borderline, ❌ too big |
| RAM | Required RAM (GB) |
| Context | Max context length (tokens) |
| Quant | Quantization method (q4_K_M, q8_0, etc.) |

## Integration with Ollama

llmfit can directly suggest which models to `ollama pull`:

```bash
# Get top 5 recommended models for your system
llmfit --provider ollama --format json | jq -r '.models[:5] | .[].name' | while read model; do
  echo "Consider: ollama pull $model"
done
```

## Use Cases

- **Before downloading a model:** Check if it will run on your phone/laptop
- **Optimizing for speed:** Find fastest acceptable-quality model
- **Memory constraints:** Filter to models that fit in available RAM
- **Comparing providers:** See if HuggingFace or Ollama has better quantization
- **Multi-GPU setups:** llmfit detects multiple GPUs and splits accordingly

## Installation

On Termux/Android (ARM64):
```bash
# Cargo (requires Rust)
cargo install llmfit

# Or download prebuilt (if available)
curl -fsSL https://llmfit.axjns.dev/install.sh | sh
```

On Linux/macOS:
```bash
brew tap AlexsJones/llmfit && brew install llmfit
```

## Configuration

Environment variables:
- `LLMFIT_CACHE_TTL` — cache hardware detection (default 300s)
- `LLMFIT_MODEL_DB_PATH` — path to custom model database

## Technical Details

- Hardware detection: `/proc/cpuinfo`, `/proc/meminfo`, `nvidia-smi`, `lspci`
- Model database: embedded JSON with 206 entries, updated with each release
- Speed estimation: based on known benchmarks scaled by your CPU/GPU specs

## Limitations

- Does not actually download models; only advises.
- Speed estimates are approximate; real-world depends on many factors.
- Model database may lag behind newest releases.

## Resources

### scripts/
- `scan.py` — Hardware detection
- `score.py` — Compute fit/speed/quality scores
- `list.py` — Output models in various formats
- `tui.py` — Interactive TUI

### references/
- `models_db.md` — List of 206 models and their specs
- `scoring_algorithm.md` — How quality, speed, fit are calculated
- `providers.md` — Differences between Ollama, HuggingFace, etc.

---

**Note:** llmfit is developed by Alex Jones. This skill wraps its CLI. For more details, see https://github.com/AlexsJones/llmfit

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
