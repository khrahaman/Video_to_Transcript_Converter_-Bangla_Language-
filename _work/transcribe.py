import os
import sys
import time

os.environ.setdefault("HF_HOME", "D:/vid_to_audio/_work/hf_cache")

from faster_whisper import WhisperModel

AUDIO_DIR = "D:/vid_to_audio/_work/audio"
OUT_DIR = "D:/vid_to_audio/_work/transcripts"
os.makedirs(OUT_DIR, exist_ok=True)

files = sorted(f for f in os.listdir(AUDIO_DIR) if f.endswith(".wav"))

def load_model():
    try:
        m = WhisperModel("small", device="cuda", compute_type="int8_float16")
        print("Loaded model on CUDA (int8_float16)", flush=True)
        return m
    except Exception as e:
        print(f"CUDA load failed ({e}), falling back to CPU", flush=True)
        return WhisperModel("small", device="cpu", compute_type="int8")

model = load_model()

for fname in files:
    base = fname[:-4]
    out_path = os.path.join(OUT_DIR, base + ".txt")
    if os.path.exists(out_path):
        print(f"Skipping {base}, already transcribed", flush=True)
        continue
    audio_path = os.path.join(AUDIO_DIR, fname)
    print(f"Transcribing {base}...", flush=True)
    t0 = time.time()
    segments, info = model.transcribe(audio_path, beam_size=5, vad_filter=True)
    lines = []
    for seg in segments:
        lines.append(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text.strip()}")
    text = "\n".join(lines)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)
    dt = time.time() - t0
    print(f"Done {base}: lang={info.language} duration={info.duration:.1f}s took={dt:.1f}s", flush=True)

print("ALL DONE", flush=True)
