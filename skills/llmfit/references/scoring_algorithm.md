# Scoring Algorithm

llmfit computes four primary scores:

## Quality

Quality scores are pulled from community benchmarks (Open LLM Leaderboard, HuggingFace evaluations). They reflect the model's capability on reasoning, coding, math, and knowledge tasks.

- Raw scores are normalized to 0-1.
- Some models lack benchmarks → estimated based on size/architecture.

## Speed

Speed prediction formula:

```
tokens_per_second = (hardware_factor * flops_per_token) / model_parameters
```

Where:
- `hardware_factor` = benchmark-derived constant for your CPU/GPU (e.g., 1.2e12 for modern laptop)
- `flops_per_token` = 2 * parameter_count (approx)
- `model_parameters` = in billions

Quantization affects speed: faster for lower quants (q4 vs q8) but quality trade-off.

## Fit

Fit is Boolean: ✅ fits, ❌ doesn't, ⚠️ borderline.

```
required_ram = model_size_gb * 1.5  // kv cache overhead
available_ram = system_ram_gb - 2  // reserve 2GB for OS
fit = required_ram <= available_ram
```

For GPU, similar check with `gpu_mem_gb`.

## Context

Max practical context length based on RAM:

```
max_context = available_ram / (model_size_gb / context_window) * safety_factor
```

Shorter context uses less memory; if you need long context, you may need to reduce batch size or use a smaller model.

---

The scores are rapidly computed and cached for 5 minutes to avoid repeated hardware probing.