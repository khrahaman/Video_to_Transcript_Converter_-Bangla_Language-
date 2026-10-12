import time
from faster_whisper import WhisperModel

t0 = time.time()
model = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
print(f"model loaded in {time.time()-t0:.1f}s")

t0 = time.time()
segments, info = model.transcribe(
    "D:/vid_to_audio/_work/audio/20260928_100728.wav",
    beam_size=5,
    language="bn",
    vad_filter=False,
    condition_on_previous_text=False,
)
segments = list(segments)
print(f"transcribed clip in {time.time()-t0:.1f}s")
with open("D:/vid_to_audio/_work/baseline_transcript.txt", "w", encoding="utf-8") as f:
    f.write(f"lang: {info.language} {info.language_probability}\n")
    for seg in segments:
        f.write(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text.strip()}\n")
print("wrote transcript")
