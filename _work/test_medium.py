import os
os.environ.setdefault("HF_HOME", "D:/vid_to_audio/_work/hf_cache")
from faster_whisper import WhisperModel

import time
t0 = time.time()
try:
    model = WhisperModel("large-v3", device="cuda", compute_type="int8")
    print("using CUDA int8")
except Exception as e:
    print("cuda int8 failed:", e)
    model = WhisperModel("large-v3", device="cpu", compute_type="int8")
    print("using CPU int8")
segments, info = model.transcribe(
    "D:/vid_to_audio/_work/audio/20260928_100728.wav",
    beam_size=5,
    language="bn",
    vad_filter=False,
    condition_on_previous_text=False,
)
with open("D:/vid_to_audio/_work/test_large_out.txt", "w", encoding="utf-8") as fh:
    fh.write(f"lang: {info.language} {info.language_probability}\n")
    for seg in segments:
        fh.write(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text.strip()}\n")
print(f"done in {time.time()-t0:.1f}s")
