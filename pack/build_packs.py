#!/usr/bin/env python3
"""build_packs.py — assemble one slim vid-pack per uploadable.

Reads: voice masters (sleepdraw runs), cluster spec files (damn art/).
Writes: packs/<slug>/{meta.json,prompts.md,cue.yaml,segments.txt,build.sh,README.md}
        + packs/<slug>.zip
Audio is REFERENCED (path+sha256+duration), never copied.
"""
import hashlib
import json
import os
import re
import subprocess
import zipfile

VOICE = "/root/sleepdraw/runs/studio/voice"
ART = "/root/damn/projects/folk-and-fable/art"
OUT = "/root/sleepdraw/runs/studio/packs"

# slug, title, [audio files], cluster spec, [(tale, spec-section-anchor or None)]
UPLOADABLES = [
    ("grimm-01", "Grimm's Fairy Tales I", ["ff-grimm-part-1-080501-14-master.mp3"],
     "cluster-grimm.spec.md", ["Twelve Brothers", "Rapunzel", "Hansel and Gretel"]),
    ("grimm-02", "Grimm's Fairy Tales II", ["ff-07-grimm-part-2-full-074116-50-master.mp3"],
     "cluster-grimm.spec.md", ["Briar-Rose", "Snow White"]),
    ("grimm-03", "Grimm's Fairy Tales III", ["ff-grimm-part-3-094850-16-master.mp3"],
     "cluster-grimm.spec.md", []),
    ("grimm-04", "Grimm's Fairy Tales IV", ["ff-grimm-part-4-103914-17-master.mp3"],
     "cluster-grimm.spec.md", []),
    ("andersen-01", "Andersen's Fairy Tales I", ["ff-andersen-part-1-214621-02-master.mp3"],
     "cluster-andersen-perrault.spec.md", ["Little Mermaid"]),
    ("andersen-02", "Andersen's Fairy Tales II", ["ff-andersen-part-2-223656-03-master.mp3"],
     "cluster-andersen-perrault.spec.md", ["Snow Queen", "Puss in Boots", "Cinderella"]),
    ("kwaidan-01", "Kwaidan I", ["ff-kwaidan-part-1-124026-20-master.mp3"],
     "cluster-japan.spec.md", ["Mujina", "Rokuro-Kubi"]),
    ("kwaidan-02", "Kwaidan II + Yuki-Onna", ["ff-kwaidan-part-2-133420-21-master.mp3",
     "ff-yuki-onna-211130-01-master.mp3"], "cluster-japan.spec.md",
     ["Jiu-Roku-Zakura", "Yuki-Onna"]),
    ("russian-tales", "Russian Fairy Tales", ["ff-russian-fairy-tales--184910-28-master.mp3",
     "ff-russian-fairy-tales--193900-29-master.mp3", "ff-russian-fairy-tales--202448-30-master.mp3"],
     "cluster-russian.spec.md", ["Vasilisa + Baba Yaga", "Firebird", "Snegurochka"]),
    ("russian-stories", "Russian Story Book", ["ff-russian-story-book-p-211334-31-master.mp3",
     "ff-russian-story-book-p-215609-32-master.mp3"], "cluster-russian.spec.md", []),
    ("nights-01", "Thousand Nights", ["ff-thousand-nights-part-021320-38-master.mp3"],
     "cluster-nights.spec.md", ["Ali Baba"]),
    ("nights-02", "Nights Continued", ["ff-nights-continued-143901-23-master.mp3"],
     "cluster-nights.spec.md", []),
    ("nights-03", "Arabian Nights + Sinbad", ["ff-arabian-nights-enter-232424-04-master.mp3",
     "ff-sinbad-burton-223909-33-master.mp3"], "cluster-nights.spec.md",
     ["Aladdin", "Sinbad"]),
    ("celtic-01", "Celtic Folk + Fairy Faith", ["ff-celtic-folk-fairy-ta-014611-07-master.mp3",
     "ff-fairy-faith-celtic-051515-11-master.mp3"], "cluster-celtic-norse.spec.md",
     ["The Changeling", "Tam Lin"]),
    ("celtic-02", "English Fairy + Household", ["ff-english-fairy-tales--041448-10-master.mp3",
     "ff-household-spirits-112736-18-master.mp3"], "cluster-celtic-norse.spec.md", []),
    ("celtic-03", "West England + Changelings", ["ff-west-england-romance-044716-42-master.mp3",
     "ff-changelings-witnesse-023142-08-master.mp3"], "cluster-celtic-norse.spec.md", []),
    ("norse-01", "Eddas", ["ff-poetic-edda-153614-24-master.mp3",
     "ff-prose-edda-180729-27-master.mp3", "ff-prose-edda-part-2-171958-26-master.mp3"],
     "cluster-celtic-norse.spec.md", ["Ragnarok", "Master-Builder"]),
    ("african-01", "Anansi + West African", ["ff-jamaica-anansi-120650-19-master.mp3",
     "ff-west-african-part-1-034816-40-master.mp3", "ff-west-african-part-2-041841-41-master.mp3"],
     "cluster-african.spec.md", ["Anansi", "Why the Sky is Far Away"]),
    ("african-02", "South African Folk Tales", ["ff-south-african-folk-t-004233-36-master.mp3"],
     "cluster-african.spec.md", []),
    ("shorts-01", "Yuki-Onna (pilot)", ["01-yuki-135401-01-master.mp3"],
     "yuki-tableau.spec.md", ["Yuki-Onna"]),
    ("shorts-02", "Mermaid + Baba Yaga", ["ff-02-little-mermaid-073006-45-master.mp3",
     "ff-03-baba-yaga-073355-46-master.mp3"],
     ["cluster-andersen-perrault.spec.md", "cluster-russian.spec.md"],
     ["Little Mermaid", "Vasilisa + Baba Yaga"]),
    ("shorts-03", "Punchkin + Deccan + Aesop", ["ff-04-punchkin-073737-47-master.mp3",
     "ff-05-deccan-sun-moon-w-073915-48-master.mp3", "ff-06-aesop-fables-074013-49-master.mp3"],
     "cluster-african.spec.md", ["Punchkin", "Deccan Sun-Moon-Wind"]),
]

BUILD_SH = r"""#!/usr/bin/env bash
# build.sh — pack assembler. Proven recipe (yuki-practice-full, 1080p24).
# usage: build.sh
# reads segments.txt: title|audio|still|duration_s  (still rendered at factory)
# writes <slug>-full.mp4
set -euo pipefail
SLUG="$(basename "$PWD")"
FPS=24
segs=()
i=0
while IFS='|' read -r title audio still dur; do
  [[ "$title" =~ ^#.*$ || -z "$title" ]] && continue
  i=$((i+1))
  FRAMES=$(python3 -c "print(int(float('$dur')*$FPS))")
  FADEOUT_ST=$(python3 -c "print(float('$dur')-3)")
  LAST=""
  # outro law on final segment handled after loop; per-tale: 3s black both ends
  ffmpeg -y -v error -loop 1 -framerate $FPS -i "$still" \
    -vf "scale=1080:1080:in_range=full:out_range=limited,pad=1920:1080:(ow-iw)/2:(oh-ih)/2:color=black,zoompan=z='1+0.12*on/$FRAMES':x='(iw-iw/zoom)*on/$FRAMES':y='(ih-ih/zoom)/2':d=$FRAMES:s=1920x1080:fps=$FPS,fade=t=in:st=0:d=3,fade=t=out:st=$FADEOUT_ST:d=3,format=yuv420p" \
    -frames:v $FRAMES -c:v libx264 -crf 18 -preset veryfast "seg_$i.mp4"
  ffmpeg -y -v error -i "$audio" -af "loudnorm=I=-14:TP=-1.5:LRA=11,afade=t=in:st=0:d=3,afade=t=out:st=$FADEOUT_ST:d=3" \
    -c:a aac -b:a 192k -ar 48000 -ac 2 "seg_$i.m4a"
  ffmpeg -y -v error -i "seg_$i.mp4" -i "seg_$i.m4a" -map 0:v -map 1:a -c copy \
    -movflags +faststart "seg_$i-full.mp4"
  segs+=("seg_$i-full.mp4")
  rm -f "seg_$i.mp4" "seg_$i.m4a"
done < segments.txt
printf "file '%s'\n" "${segs[@]}" > concat.txt
ffmpeg -y -v error -f concat -safe 0 -i concat.txt -c copy -movflags +faststart "$SLUG-full.mp4"
rm -f seg_*-full.mp4 concat.txt
echo "DONE: $SLUG-full.mp4"
"""


def duration(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                        "format=duration", "-of", "csv=p=0", path],
                       capture_output=True, text=True, timeout=60)
    return float(r.stdout.strip())


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(4 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def extract_prompt(cluster_files, tale):
    """Slice a tale's section out of cluster spec(s). None if not found.
    Single-tableau specs (no ### tale headings, <10KB) embed whole."""
    if not cluster_files:
        return None
    if isinstance(cluster_files, str):
        cluster_files = [cluster_files]
    for cf in cluster_files:
        p = os.path.join(ART, cf)
        if not os.path.exists(p):
            continue
        text = open(p).read()
        heads = [(m.start(), m.group(0)) for m in re.finditer(r"^### .+$", text, re.M)]
        if not heads and len(text) < 10240:
            return f"(whole file: {cf})\n\n" + text.strip()
        want = tale.lower().split(" ")[0]
        for idx, (pos, head) in enumerate(heads):
            if want in head.lower():
                end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
                nxt = re.search(r"^## ", text[pos + 10:], re.M)
                if nxt and pos + 10 + nxt.start() < end:
                    end = pos + 10 + nxt.start()
                return head + "\n" + text[pos + len(head):end].strip()
    return None
    # sections headed "### <tale>" (case-insensitive, prefix match)
    heads = [(m.start(), m.group(0)) for m in re.finditer(r"^### .+$", text, re.M)]
    want = tale.lower().split(" ")[0].rstrip("s-")
    for idx, (pos, head) in enumerate(heads):
        if want in head.lower() or head.lower().split(" ", 1)[-1][:6] in tale.lower():
            end = heads[idx + 1][0] if idx + 1 < len(heads) else len(text)
            # stop at next ## section too
            nxt = re.search(r"^## ", text[pos + 10:], re.M)
            if nxt and pos + 10 + nxt.start() < end:
                end = pos + 10 + nxt.start()
            return head + "\n" + text[pos + len(head):end].strip()
    return None


def main():
    os.makedirs(OUT, exist_ok=True)
    report = []
    for slug, title, audios, cluster, tales in UPLOADABLES:
        d = os.path.join(OUT, slug)
        os.makedirs(d, exist_ok=True)
        audio_meta, total = [], 0.0
        missing_audio = []
        for a in audios:
            p = os.path.join(VOICE, a)
            if os.path.exists(p):
                dur = duration(p)
                audio_meta.append({"file": a, "path": p,
                                   "sha256": sha256(p), "duration_s": round(dur, 2)})
                total += dur
            else:
                missing_audio.append(a)
        prompts, specced, pending = [], [], []
        for tale in tales:
            sec = extract_prompt(cluster, tale)
            if sec:
                prompts.append("---\n\n" + sec)
                specced.append(tale)
            else:
                pending.append(tale)
        prompts_md = (f"# {title} — tableau prompts (copy-paste into vision model)\n"
                      f"\nHouse: folk-and-fable, lora3, 16:9, black canvas, gold engine-drawn.\n"
                      + ("\n".join(prompts) if prompts else "\n(no tale prompts specced yet — see cluster file)\n"))
        if pending:
            prompts_md += ("\n---\n\n## Prompts still needed (next spec batch)\n" +
                           "".join(f"- [ ] {t}\n" for t in pending))
        meta = {"slug": slug, "title": title,
                "audio": audio_meta, "missing_audio": missing_audio,
                "total_s": round(total, 2), "total_h": round(total / 3600, 2),
                "cluster_spec": cluster, "tales_specced": specced,
                "tales_pending": pending,
                "ready_for_factory": bool(audio_meta) and not missing_audio
                and not pending and bool(specced),
                "thumbnail_rule": "strongest tale's final frame (verdict on dash)"}
        cue = (f"# cue sheet — {slug}\n"
               f"uploadable: {slug}\nbed: rain-tent (continuous, never drops)\n"
               f"transitions: fade to black 3s + black hold 2s between tales "
               f"(bed continues); outro law 15s fade + 5s black at end\n"
               f"chapters: one per tale (starts fill in when read text staged)\ntales:\n")
        for k, tale in enumerate(tales):
            cue += f"  - title: \"{tale}\"\n    start: TBD\n    still: stills/{k+1:02d}-{slug}.jpg\n"
        seg = "".join(f"# {t}\n# audio: TBD (per-tale master or full-book split)\n"
                      f"# still: stills/{k+1:02d}-{slug}.jpg\n# duration_s: TBD\n\n"
                      for k, t in enumerate(tales))
        readme = (f"# pack {slug} — {title}\n\nTotal audio: {meta['total_h']}h. "
                  f"Factory-ready: {meta['ready_for_factory']}.\n\n"
                  + ("Missing audio: " + ", ".join(missing_audio) + "\n" if missing_audio else "")
                  + ("Prompts needed: " + ", ".join(pending) + "\n" if pending else "")
                  + ("\nNext: render stills into stills/, fill segments.txt, run ./build.sh\n"
                       if meta["ready_for_factory"] else
                       "\nBlocked: stage read text for starts + spec pending prompts.\n"))
        open(os.path.join(d, "meta.json"), "w").write(json.dumps(meta, indent=1))
        open(os.path.join(d, "prompts.md"), "w").write(prompts_md)
        open(os.path.join(d, "cue.yaml"), "w").write(cue)
        open(os.path.join(d, "segments.txt"), "w").write(seg)
        bp = os.path.join(d, "build.sh")
        open(bp, "w").write(BUILD_SH)
        os.chmod(bp, 0o755)
        open(os.path.join(d, "README.md"), "w").write(readme)
        zp = os.path.join(OUT, slug + ".zip")
        if os.path.exists(zp):
            os.remove(zp)
        with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
            for f in ("meta.json", "prompts.md", "cue.yaml", "segments.txt",
                      "build.sh", "README.md"):
                z.write(os.path.join(d, f), f)
        report.append((slug, meta["total_h"], meta["ready_for_factory"],
                       len(specced), len(pending),
                       os.path.getsize(zp) // 1024))
    print(f"{'slug':<14}{'hrs':>6}  factory  specced/pending  zipKB")
    for slug, h, ready, s, p, kb in report:
        print(f"{slug:<14}{h:>6.2f}  {'YES' if ready else 'no ':<7}  {s}/{p:<13}{kb}")
    print(f"\n{len(report)} packs in {OUT}")


if __name__ == "__main__":
    main()
