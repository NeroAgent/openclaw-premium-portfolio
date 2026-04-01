# Models Comparison

## Chatterbox-Turbo (350M)

**Size:** 350 million parameters  
**Languages:** English only  
**Inference speed:** Fast (1-step decoder)  
**VRAM:** ~1.5GB (FP16)  
**Key features:**
- Paralinguistic tags native
- Low latency (~200ms on GPU, ~1s on CPU)
- Built for voice agents

**Best for:** Real-time applications, production voice agents, fast iteration.

**Limitations:** English only.

## Chatterbox-Multilingual (500M)

**Size:** 500M  
**Languages:** 23+ (see list in main README)  
**Inference speed:** Moderate (multi-step decoder)  
**VRAM:** ~2GB  
**Key features:**
- Zero-shot voice cloning across languages
- Language ID parameter (`--lang fr`, `--lang zh`, etc.)
- Good cross-lingual consistency

**Best for:** Global apps, multilingual content, localization workflows.

**Limitations:** Slower than Turbo; quality may vary by language.

## Original Chatterbox (500M)

**Size:** 500M  
**Languages:** English  
**Inference speed:** Moderate  
**VRAM:** ~2GB  
**Key features:**
- CFG weight tuning (controls adherence to reference)
- Exaggeration tuning (expressiveness)
- Mature model with active community

**Best for:** Creative projects, exaggerated expressive speech, when you need fine control.

**Limitations:** English only; no paralinguistic tags.

---

### Quick Decision Guide

| Need | Choose |
|------|--------|
| Fastest, English, agent use | Turbo |
| Multiple languages | Multilingual |
| Maximum expressiveness control | Original |
| Paralinguistic tags | Turbo |
| Lowest VRAM | Turbo |
| Best quality overall (subjective) | Compare demos; many prefer Turbo |

---

**Demos:** https://resemble-ai.github.io/chatterbox_turbo_demopage/  
**Comparison:** https://podonos.com/resembleai/chatterbox-turbo-vs-elevenlabs-turbo