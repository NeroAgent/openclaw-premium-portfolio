---
name: resource-check
description: "Monitor system resources on resource-constrained environments (Termux/Android). Checks RAM, storage, CPU, battery, and network status. Use before starting heavy tasks, during heartbeat checks, or when performance degrades. Provides actionable recommendations: whether to proceed, defer, or free up resources."
---

# Resource Check

## Overview

`resource-check` provides real-time visibility into system health for Termux/Android environments. It collects diagnostics on memory, storage, CPU, battery, and network, then evaluates against configurable thresholds to recommend actions.

**Designed for:** Resource-constrained mobile development where every MB of RAM and battery percentage matters.

## Quick Start

```bash
# Check all resources with recommendations
resource-check all

# Check specific areas
resource-check ram
resource-check storage
resource-check battery
resource-check network

# Get raw JSON for scripting
resource-check all --output json

# Set custom thresholds (override defaults)
resource-check all --min-ram-free 500M --min-battery 20
```

## Capabilities

### 1. RAM Assessment
- Total, used, free memory (MB)
- Swap availability (if configured)
- OOM killer proximity check
- Recommendation: `proceed`, `caution`, `stop`

**Thresholds:**
- Free RAM > 1GB: ✅ proceed
- Free RAM 500MB-1GB: ⚠️ caution (avoid parallel tasks)
- Free RAM < 500MB: ❌ stop (kill background processes first)

### 2. Storage Check
- Total and available storage (GB) on Termux home and external storage
- Inode usage (file count limits)
- Permission issues (Android storage access)
- Recommendation based on free space vs. expected task size

**Thresholds:**
- Free > 5GB: ✅ proceed
- Free 2-5GB: ⚠️ caution (clean caches)
- Free < 2GB: ❌ stop

### 3. CPU Load
- CPU count, current load average (1/5/15 min)
- Temperature (if available via Termux:API)
- Throttling detection (Android thermal)
- Recommendation: avoid heavy builds if load > core count

### 4. Battery Status
- Current percentage and charging state
- Estimated runtime remaining
- Warning if battery < 20% and not charging
- Recommendation: defer intensive tasks unless charging

### 5. Network Connectivity
- Online status (ping/API check)
- Latency measurement (optional)
- Data usage alerts (if metered)
- Offline mode detection: should skill queue commands?

## Examples

**User:** "Can I run tests now?"  
**Nero:** (runs `resource-check all`) → "RAM: 800MB free (caution), Battery: 45% (OK), Storage: 12GB free (✅). You can run tests but avoid running more than 2 at once."

**User:** "Build the APK"  
**Nero:** Pre-check → "Battery at 15% and not charging. Recommend plugging in first. Proceed anyway?" (waits for confirmation)

**Heartbeat:** Every 6 hours, `resource-check --output json` → store in memory/heartbeat-state.json with timestamp.

## Integration

- **Pre-task:** Automatically run before memory-intensive skills (coding-agent builds, video-frames processing)
- **Heartbeat:** Include in periodic checks to track resource trends
- **Failure recovery:** If a skill fails due to OOM, `resource-check` suggests cleanup actions (kill background processes, clear caches)

## Resources

### scripts/
- `check.py` — Main entry point, parses arguments, orchestrates checks
- `ram.py` — RAM/swap detection using `free`, `/proc/meminfo`
- `storage.py` — Storage and inode checks using `df`, `stat`
- `cpu.py` — CPU count, load average, temperature (Termux:API)
- `battery.py` — Battery level via Termux:API or `/sys/class/power_supply/`
- `network.py` — Connectivity test, latency, metered detection
- `recommend.py` — Threshold engine that produces human-readable advice

### references/
- `thresholds.md` — Default thresholds, how to customize, environment-specific tuning
- `termux_quirks.md` — Android storage permissions, proxt-distro considerations, Termux:API requirements

## Thresholds Reference

See `references/thresholds.md` for complete table and how to override via config file or CLI flags.

## Termux Quirks

- Storage: `/data/data/com.termux/files/home` (internal), `/storage/emulated/0` (external). Use `termux-setup-storage` to grant permissions.
- CPU info: `/proc/cpuinfo` may be limited; `nproc` counts available cores.
- Battery: Not directly accessible without Termux:API or root. May return "unknown".
- Network: `ping` may not be installed; fallback to `curl` to known URL.

---

**Note:** This skill is lightweight (<10MB RAM, <5s runtime). It uses standard Linux/Android tools, no heavy dependencies.

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
