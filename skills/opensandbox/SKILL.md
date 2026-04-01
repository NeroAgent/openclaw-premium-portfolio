---
name: opensandbox
description: "Secure sandbox for executing code in isolated environments (Docker/Kubernetes). Use when running untrusted code, building Android apps, testing dependencies, or needing reproducible environments. Wraps OpenSandbox SDK to create disposable containers with filesystem, network, and resource limits. Integrates with coding-agent for safe build and test workflows."
---

# OpenSandbox

## Overview

`opensandbox` provides isolated, disposable execution environments using Docker or Kubernetes. It's designed for:

- Running untrusted code safely
- Building Android apps in a controlled environment
- Testing across multiple language runtimes
- CI/CD sandboxing
- Reproducible development environments

**Important:** This skill requires a working Docker daemon or Kubernetes cluster. On Termux/Android, Docker is typically not available; use this skill on a workstation or CI server.

## Quick Start

```bash
# 1. Install OpenSandbox server (once)
opensandbox install-server

# 2. Start the sandbox server (local Docker)
opensandbox start-server

# 3. Create a sandbox and run a command
opensandbox run "echo 'Hello from sandbox'"

# 4. Run a code interpreter session
opensandbox python "print(2+2)"
```

## Capabilities

### 1. Server Management

```bash
opensandbox install-server   # Install opensandbox-server via pip/uv
opensandbox start-server     # Start local Docker-backed server
opensandbox stop-server      # Stop server
opensandbox server-status    # Check health
```

The server listens on `http://localhost:8080` by default.

### 2. Sandbox Execution

```bash
# Run a shell command in a sandbox
opensandbox run "ls -la"

# Run with specific image
opensandbox run --image python:3.11 "python -c 'import sys; print(sys.version)'"

# Mount local directory
opensandbox run --mount .:/workspace "make test"
```

### 3. Code Interpreter

Execute code in various languages with stateful sessions:

```bash
opensandbox python "import numpy; print(numpy.__version__)"
opensandbox node "console.log(process.version)"
opensandbox bash "echo $HOME"
```

Sessions are ephemeral; filesystem changes are discarded after exit (unless using persistent volumes).

### 4. File Operations

```bash
# Upload a file to sandbox
opensandbox upload local.txt /tmp/remote.txt

# Download from sandbox
opensandbox download /tmp/output.txt .

# Execute with mounted workspace (current dir)
opensandbox run --workspace "npm test"
```

## Use Cases

- **Android builds:** Use a sandbox with Android SDK installed to build APKs without polluting host.
- **Dependency testing:** Try a new npm/apt package without installing globally.
- **Security:** Run user-provided code snippets safely.
- **Reproducibility:** Ensure everyone uses the same environment.

## Installation

On the host system (requires Python 3.10+ and Docker):

```bash
# Install server
uv pip install opensandbox-server

# Or via pip
pip install opensandbox-server
```

The skill's `install-server` script automates this if possible.

**Check server:**
```bash
opensandbox start-server
# Should print "Server started on http://localhost:8080"
```

## Configuration

Environment variables:

- `OPENSANDBOX_SERVER_URL` — override server URL (default: http://localhost:8080)
- `OPENSANDBOX_DEFAULT_IMAGE` — default sandbox image (e.g., `python:3.11`)
- `OPENSANDBOX_TIMEOUT` — max execution seconds (default: 600)

## Examples

**Build an Android app:**
```bash
opensandbox run --image ner0/opensandbox-android:latest \
  "--mount $PWD:/app" \
  "./gradlew assembleDebug"
```

**Run tests in clean environment:**
```bash
opensandbox run --image node:20 -- "npm ci && npm test"
```

**Python quick check:**
```bash
opensandbox python "import pandas; print(pandas.__version__)"
```

## Notes

- OpenSandbox is a powerful tool but requires infrastructure.
- On Termux, consider using `proot-distro` for lightweight sandboxing instead.
- For long-running sessions, increase timeout.
- Network access inside sandbox is controlled by egress rules (configurable on server).

## Resources

### scripts/
- `install_server.py` — Install opensandbox-server
- `start_server.py` / `stop_server.py` / `status.py` — Server control
- `run.py` — Generic sandbox execution
- `language.py` — Code interpreter for specific languages
- `file_transfer.py` — Upload/download

### references/
- `architecture.md` — Server + runtime architecture
- `sdk.md` — Using OpenSandbox SDK directly
- `security.md` — Isolation guarantees and limitations

---

**Note:** OpenSandbox is developed by Alibaba and the open source community. This skill wraps its CLI and HTTP API. For advanced usage, consult the upstream docs: https://opensandbox.ai

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
