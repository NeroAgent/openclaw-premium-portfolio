# Paralinguistic Tags Reference

Chatterbox-Turbo natively supports expressive tags inserted into the text:

| Tag | Effect |
|-----|--------|
| `[laugh]` | Insert a hearty laugh |
| `[chuckle]` | A lighter, shorter laugh |
| `[cough]` | A polite cough |
| `[sigh]` | A sigh (disappointed or relieved) |
| `[yawn]` | A yawn |
| `[sniff]` | Sniffing (crying or cold) |
| `[clears throat]` | Throat clearing |
| `[groan]` | A groan of pain or frustration |
| `[gasp]` | A sharp intake of breath |
| `[pause]` | A brief pause (silence) |

**Usage:**
```
"Hello there! [chuckle] It's good to see you. [cough] Sorry, I've got a bit of a cold."
```

The model will produce the corresponding non-lexical sounds inline with the speech.

**Note:** These tags are only supported by Turbo and Multilingual models. For the original model, use exaggeration/CFG to add expressivity instead.

**Positioning:** Place tags where you want the sound to occur. They occupy time in the audio output like a word; adjust pacing accordingly.

---

More tags may be added in future versions. Check the official documentation for updates.