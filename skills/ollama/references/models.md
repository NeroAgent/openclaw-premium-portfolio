# Recommended Models for Mobile/Resource-Constrained

## Small Models (<4GB)

| Model | Size | RAM Needed | Quality | Use Case |
|-------|------|------------|---------|----------|
| `gemma:2b` | 1.4 GB | ~4 GB | Good for simple tasks | Quick answers, light coding |
| `llama3.2:3b` | 2.0 GB | ~6 GB | Solid for its size | General purpose, coding help |
| `qwen2.5:3b` | 2.0 GB | ~6 GB | Competitive with Llama | Multilingual, coding |
| `phi3:mini` | 2.3 GB | ~5 GB | Strong reasoning | Q&A, logic |
| `mistral:7b` | 4.1 GB | ~10 GB | Higher quality | Serious coding, complex tasks |

## Medium Models (4-8GB)

| Model | Size | RAM Needed | Quality |
|-------|------|------------|---------|
| `llama3:8b` | 4.7 GB | ~12 GB | Very good |
| `qwen2.5:7b` | 4.5 GB | ~11 GB | Very good |
| `codellama:7b` | 3.8 GB | ~10 GB | Specialized for code |

## Large Models (>8GB) — Desktop Only

- `llama3:70b` (40GB) — needs 80GB RAM
- `mixtral:8x7b` (26GB) — needs 60GB RAM

**Tip:** Use `ollama show <model>` to see parameter count and size before pulling.

---

## Choosing a Model

- **For Termux/Android:** Stick to 2B-3B models. They fit in ~6GB RAM and run acceptably fast (~5 tokens/sec on good CPU).
- **For laptop/desktop:** 7B-8B models offer better quality with still-reasonable disk usage.
- **For coding:** `codellama` variants or `llama3.2:3b-instruct` fine-tuned for code.
- **For multilingual:** `qwen2.5` supports many languages.

## Converting Other Formats

Ollama uses GGUF format (quantized). If you have a model in another format, use `ollama create` with a Modelfile to convert.

---

For the full model zoo, see https://ollama.com/library