"""Storyboard: narration script -> 5-minute chapters, one image each.

Pacing law (sleep niche): a picture every ~5 min for the first hour, each
relevant to what's being said as it comes into focus; then black + bed.
Slow narration ≈ 110 wpm → ~550 words per 5-min chapter.

Input script format: plain text, sentences. Optional [MM:SS] markers force
chapter breaks (illustration must land on its words — markers win).
Output: runs/<name>/chapters.json [{n, start_min, words, text, prompt}] with
prompt slots filled by keyword seed (human/agent refines in Studio).

Usage:
  python3 cli.py board --script essay.txt --name mariner-night
  python3 cli.py shot --board runs/mariner-night-<ts>/chapters.json --n 3 --prompt "..." [--style lora2]
"""
import json
import os
import re
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

WPM = 110
CHAPTER_MIN = 5
WORDS_PER_CHAPTER = WPM * CHAPTER_MIN

STOP = set("""a an the and or of to in on at for with as by is are was were be been
being it its this that these those i you he she we they them his her our your
their my me him us so but not no from into over after such very can will just
than then there here when where what which who whom how all any both each few
more most other some only own same too s t d ll m re ve don doesn isn aren wasn
weren hadn hasn haven couldn wouldn shouldn mustn needn ought shan""".split())


def _sentences(text):
    text = re.sub(r"\[(.*?)\]", r" MARK[\1]MARK ", text)
    parts = re.split(r"(?<=[.!?])\s+|\s*MARK\[?(.*?)\]?MARK\s*", text)
    out = []
    for p in parts:
        p = (p or "").strip()
        if not p:
            continue
        m = re.fullmatch(r"\[?(\d+):(\d+)\]?", p)
        if m:
            out.append(("break", int(m.group(1)) + int(m.group(2)) / 60))
        else:
            out.append(("text", p))
    return out


def _keywords(text, k=6):
    words = re.findall(r"[a-z]{4,}", text.lower())
    freq: dict = {}
    for w in words:
        if w not in STOP:
            freq[w] = freq.get(w, 0) + 1
    return [w for w, _ in sorted(freq.items(), key=lambda x: -x[1])[:k]]


def board(script_path, name, wpm=WPM, chapter_min=CHAPTER_MIN):
    with open(script_path) as f:
        text = f.read()
    wpc = wpm * chapter_min
    chapters, cur, cur_words, start_min = [], [], 0, 0.0
    n = 1

    def flush(end_min=None):
        nonlocal n, start_min
        if not cur:
            return
        joined = " ".join(cur)
        chapters.append({"n": n, "start_min": round(start_min, 1),
                         "words": cur_words, "text": joined,
                         "seed": _keywords(joined),
                         "prompt": ""})
        n += 1

    for kind, val in _sentences(text):
        if kind == "break":
            flush()
            cur, cur_words, start_min = [], 0, float(val)
            continue
        w = len(val.split())
        if cur_words + w > wpc and cur:
            flush()
            start_min = round(start_min + cur_words / wpm, 1)
            cur, cur_words = [], 0
        cur.append(val)
        cur_words += w
    flush()
    rundir = os.path.join(HERE, "runs", f"{name}-{time.strftime('%H%M%S')}")
    os.makedirs(rundir, exist_ok=True)
    path = os.path.join(rundir, "chapters.json")
    json.dump({"name": name, "wpm": wpm, "chapter_min": chapter_min,
               "chapters": chapters}, open(path, "w"), indent=1)
    return path, chapters
