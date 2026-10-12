import re, os, glob

SRC_DIR = "D:/vid_to_audio/_work/transcripts"
OUT_DIR = "D:/vid_to_audio/_work/cleaned"
os.makedirs(OUT_DIR, exist_ok=True)

seg_re = re.compile(r"^\[(\d+\.\d)-(\d+\.\d)\]\s*(.*)$")

def is_junk(text):
    # a line that is (after removing spaces/punct) just one token repeated, or a run of dots
    t = text.strip()
    if not t or t == "...":
        return True
    words = t.split()
    uniq = set(w.strip(",.") for w in words)
    if len(words) >= 3 and len(uniq) <= 2:
        return True
    # single very short garbled token repeated without spaces, e.g. "্যার্যার্যার"
    if len(words) == 1 and len(t) > 6:
        # check if it's built from a repeating short substring
        for chunklen in (2, 3, 4):
            chunk = t[:chunklen]
            if chunk and chunk * (len(t) // chunklen) == t[: (len(t) // chunklen) * chunklen] and len(t) // chunklen >= 4:
                return True
    return False

for path in sorted(glob.glob(os.path.join(SRC_DIR, "*.txt"))):
    name = os.path.splitext(os.path.basename(path))[0]
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    paragraphs = []
    buf = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("lang:"):
            continue
        m = seg_re.match(line)
        if not m:
            continue
        start, end, text = m.groups()
        text = text.replace("�", "").strip()
        if is_junk(text):
            continue
        buf.append(text)
        # break into a new paragraph roughly every ~5 segments for readability
        if len(buf) >= 5:
            paragraphs.append(" ".join(buf))
            buf = []
    if buf:
        paragraphs.append(" ".join(buf))
    out_path = os.path.join(OUT_DIR, f"{name}.txt")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(paragraphs))
    print(name, "->", len(paragraphs), "paragraphs")
