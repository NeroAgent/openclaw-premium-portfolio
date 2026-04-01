# Supported Models

Off Grid Mobile uses GGUF format models (all CPU-compatible, some NPU-accelerated).

## Text Models (LLMs)

| Model | Size | Recommended RAM | Quality |
|-------|------|----------------|---------|
| Qwen3-4B-Q4 | 2.6 GB | 4 GB | Excellent |
| Llama 3.2 3B Instruct | 2.0 GB | 4 GB | Very Good |
| Gemma 3 4B IT | 2.5 GB | 4 GB | Very Good |
| Phi-4 Mini | 1.8 GB | 3 GB | Good |
| Mistral 7B v0.3 Q4 | 4.1 GB | 8 GB | Very Good |

Place in `/sdcard/offgrid/models/text/`.

## Vision Models (Multimodal)

| Model | Size | Context | Notes |
|-------|------|---------|-------|
| SmolVLM-1.7B | 1.1 GB | 4096 | Fast, decent |
| Qwen3-VL-2B | 1.5 GB | 4096 | Multilingual |
| Gemma 3 4B IT (vision) | 2.5 GB | 8192 | Higher quality |

Place in `/sdcard/offgrid/models/vision/`.

## Image Generation

Stable Diffusion 1.5 based, with ControlNet support. Models (`.safetensors`) in `/sdcard/offgrid/models/image/`.

Examples:
- `sd1.5_epoch10.ckpt`
- `deliberate_v3.safetensors`
- `realisticVision_v51.safetensors`

## Where to Get GGUF Models

- HuggingFace: https://huggingface.co/models?library=gguf
-llama.cpp: https://huggingface.co/ggml-org/ggml-model-mgr

Download the `.gguf` file and push to device.

## NPU Acceleration

On Snapdragon 8 Gen 2+ and MediaTek Dimensity 9000+, the app can offload layers to NPU for faster inference. Enable in Settings → Acceleration → NPU. Not all models support NPU; Qwen3 and Gemma 3 have good NPU support.

---

For updated model compatibility, see the official Off Grid Mobile docs: https://offgridmobile.io/docs/models