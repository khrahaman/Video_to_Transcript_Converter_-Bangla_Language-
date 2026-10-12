import os, sys, time
os.environ.setdefault("HF_HOME", "D:/vid_to_audio/_work/hf_cache")

nvidia_base = os.path.join(os.path.dirname(sys.executable), "..", "Lib", "site-packages", "nvidia")
nvidia_base = os.path.abspath(nvidia_base)
for pkg in os.listdir(nvidia_base):
    bin_dir = os.path.join(nvidia_base, pkg, "bin")
    if os.path.isdir(bin_dir):
        os.add_dll_directory(bin_dir)
        os.environ["PATH"] = bin_dir + os.pathsep + os.environ["PATH"]

from faster_whisper import WhisperModel

t0 = time.time()
model = WhisperModel("large-v3-turbo", device="cpu", compute_type="int8")
print(f"model loaded in {time.time()-t0:.1f}s")

t0 = time.time()
segments, info = model.transcribe(
    "D:/vid_to_audio/_work/audio/20260928_100728.wav",
    beam_size=1,
    language="bn",
    vad_filter=False,
    condition_on_previous_text=False,
)
with open("D:/vid_to_audio/_work/test_gpu_out.txt", "w", encoding="utf-8") as fh:
    fh.write(f"lang: {info.language} {info.language_probability}\n")
    for seg in segments:
        fh.write(f"[{seg.start:.1f}-{seg.end:.1f}] {seg.text.strip()}\n")
print(f"transcribed 161s clip in {time.time()-t0:.1f}s")
