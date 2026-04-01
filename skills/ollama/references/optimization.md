# Optimization Tips

## Memory

- Use smaller quantizations (q4_K_M vs q8_0). Smaller = faster, less memory, slight quality drop.
- Set `OLLAMA_MAX_LOADED_MODELS=1` to keep only one model in RAM at a time.
- Use `OLLAMA_NUM_PARALLEL=1` to reduce memory pressure.

## Speed

- Increase `OLLAMA_NUM_THREADS` to number of CPU cores (or 4 for mobile).
- Use `--raw` mode if you don't need chat template processing.
- Cache model embeddings if computing repeatedly.

## Disk Space

Remove unused models with `ollama rm` to free space.

## GPU

If you have CUDA, Ollama auto-uses it. Set `OLLAMA_GPU_LAYERS` to control how many layers offload to GPU (default: all).

On Apple Silicon, Metal is auto-enabled.

## Environment Variables

| Variable | Default | Purpose |
|----------|---------|---------|
| OLLAMA_HOST | 127.0.0.1:11434 | Bind address |
| OLLAMA_MAX_LOADED_MODELS | 1 | Max models in memory |
| OLLAMA_NUM_PARALLEL | 1 | Max concurrent requests |
| OLLAMA_NUM_THREADS | CPU count | Threads for inference |
| OLLAMA_GPU_LAYERS | all | Number of layers on GPU (if available) |
| OLLAMA_MODELS | ~/.ollama/models | Model storage directory |

Set these in your shell profile before using the skill.

## Monitoring

Check RAM usage while generating:
```bash
free -h
```

If you see swap activity, reduce model size or concurrency.

---

For more, see Ollama docs: https://github.com/ollama/ollama/blob/main/docs/faq.md