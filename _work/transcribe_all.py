import os, time, glob, re
from faster_whisper import WhisperModel, BatchedInferencePipeline

AUDIO_DIR = "D:/vid_to_audio/_work/audio"
OUT_DIR = "D:/vid_to_audio/_work/transcripts"
os.makedirs(OUT_DIR, exist_ok=True)

def collapse_repeats(text, max_repeat=3):
    words = text.split()
    out = []
    run_word = None
    run_len = 0
    for w in words:
        if w == run_word:
            run_len += 1
            if run_len <= max_repeat:
                out.append(w)
        else:
            run_word = w
            run_len = 1
            out.append(w)
    return " ".join(out)

print("loading model...")
t0 = time.time()
model = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
batched_model = BatchedInferencePipeline(model=model)
print(f"model loaded in {time.time()-t0:.1f}s", flush=True)

files = sorted(glob.glob(os.path.join(AUDIO_DIR, "*.wav")))
for path in files:
    name = os.path.splitext(os.path.basename(path))[0]
    out_path = os.path.join(OUT_DIR, f"{name}.txt")
    if os.path.exists(out_path):
        print(f"skip {name} (already done)", flush=True)
        continue
    print(f"transcribing {name} ...", flush=True)
    t0 = time.time()
    segments, info = batched_model.transcribe(
        path,
        batch_size=8,
        beam_size=5,
        language="bn",
        vad_filter=True,
        condition_on_previous_text=False,
    )
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(f"lang: {info.language} {info.language_probability}\n")
        for seg in segments:
            text = collapse_repeats(seg.text.strip())
            f.write(f"[{seg.start:.1f}-{seg.end:.1f}] {text}\n")
    elapsed = time.time() - t0
    print(f"done {name} in {elapsed:.1f}s", flush=True)

print("ALL DONE", flush=True)
