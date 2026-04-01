# Model Database Summary

llmfit includes an embedded database of 206 models from 57 providers. Highlights:

## Popular Models

| Model | Params | Quant | Size | Provider |
|-------|--------|-------|------|----------|
| llama3.2:3b | 3B | q4_K_M | 2.0 GB | Ollama |
| llama3:8b | 8B | q4_0 | 4.7 GB | Ollama |
| mistral:7b | 7B | q4_0 | 4.1 GB | Ollama |
| qwen2.5:3b | 3B | q4_K_M | 2.0 GB | Ollama |
| gemma:2b | 2B | q4_0 | 1.4 GB | Ollama |
| phi3:mini | 3.8B | q4_0 | 2.3 GB | Ollama |

## Quantization Variants

Each model may have multiple quantizations:
- **q4_K_M** — 4-bit, medium quality (good trade-off)
- **q8_0** — 8-bit, higher quality, larger
- **q2_K** — 2-bit, very small, noticeable quality drop
- **fp16** — Full precision (huge, for GPU only)

llmfit accounts for quantization when estimating size and speed.

## Scoring

- **Quality:** Based on benchmarks (MMLU, GSM8K, HumanEval). Scores normalized 0-1.
- **Speed:** Estimated tokens/sec based on your CPU/GPU and model size/quant.
- **Fit:** Compares required RAM (model size * 1.5 for kv cache) to available RAM.
- **Context:** Max context you can support given RAM (longer context = more memory).

---

For the full list, see upstream: https://github.com/AlexsJones/llmfit/blob/main/models/src/models.rs