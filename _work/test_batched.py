import time
from faster_whisper import WhisperModel, BatchedInferencePipeline

t0 = time.time()
model = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
batched_model = BatchedInferencePipeline(model=model)
print(f"model loaded in {time.time()-t0:.1f}s")

t0 = time.time()
segments, info = batched_model.transcribe(
    "D:/vid_to_audio/_work/audio/20260928_100728.wav",
    batch_size=8,
    beam_size=5,
    language="bn",
    vad_filter=True,
    condition_on_previous_text=False,
)
segments = list(segments)
print(f"transcribed clip in {time.time()-t0:.1f}s")
print("lang:", info.language, info.language_probability)
with open("D:/vid_to_audio/_work/batched_transcript.txt", "w", encoding="utf-8") as f:
    for seg in segments:
        f.write(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text}\n")
print("wrote transcript")
