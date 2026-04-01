# Providers Comparison

| Provider | Format | Quant Options | Hosting | Notes |
|----------|--------|---------------|---------|-------|
| Ollama | GGUF | Many (q2-q8) | Local | Easiest for CLI use |
| HuggingFace | GGUF/Safetensors | Many | Download | Requires manual inference |
| LocalAI | GGML | Similar to Ollama | Server | REST API |
| LM Studio | GGUF | Several | Desktop GUI | macOS/Windows |
| text-generation-webui | GGUF/Safetensors | Many | Web UI | Python-based |

llmfit normalizes model names across providers when possible (e.g., `llama3.2:3b` exists on both Ollama and HuggingFace but may have different quant names).

---

**Choosing a provider:** For OpenClaw on Termux, Ollama is best supported (single binary, REST API). HuggingFace gives more control but requires more setup.