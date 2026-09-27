"""sleepdraw CLI: prompt -> art -> 16:9 -> draw -> (ship).

One variable per round: new art OR new knobs, never both.
  python3 cli.py make --prompt "lone pine..." --name pine-v1
  python3 cli.py make --prompt "..." --name pine-v2 --set WB_SKIP=6 --no-ship
  python3 cli.py make --image assets/moon-lora1-flux-pencil.jpg --name moon-v1
  python3 cli.py lora1   (print the locked recipe)
Secrets: CF_API_TOKEN/CF_ACCOUNT_ID/R2_* from env or /root/.r2-env. Never in repo.
"""
import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import yaml  # noqa: E402
from sleepdraw import art as _art, draw as _draw, ship as _ship  # noqa: E402
from sleepdraw import storyboard as _board  # noqa: E402


def _cf():
    for line in open(os.environ.get("SLEEPDRAW_ENV_FILE", "/root/.r2-env")):
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))
    return os.environ["CF_API_TOKEN"], os.environ["CF_ACCOUNT_ID"]


def _lora1():
    with open(os.path.join(HERE, "lora1.yaml")) as f:
        return yaml.safe_load(f)


def cmd_shot(a):
    data = json.load(open(a.board))
    ch = next(c for c in data["chapters"] if c["n"] == a.n)
    lora = _lora1() if a.style == "lora1" else None
    if a.style == "lora2":
        with open(os.path.join(HERE, "lora2.yaml")) as f:
            lora = yaml.safe_load(f)
    knobs = dict(lora["env"])
    for s in a.set or []:
        k, v = s.split("=", 1)
        knobs[k.strip()] = v.strip()
    prompt = a.prompt or ch["prompt"]
    if not prompt:
        sys.exit(f"chapter {a.n} has no prompt — pass --prompt or fill chapters.json "
                 f"(seed: {', '.join(ch['seed'])})")
    tok, acc = _cf()
    img = _art.generate(prompt, tok, acc, model=a.model, style=lora["art"]["style"])
    stamp = time.strftime("%H%M%S")
    slug = f"ch{a.n:02d}-{a.name or data['name']}-{stamp}"
    rundir = os.path.join(HERE, "runs", slug)
    os.makedirs(rundir, exist_ok=True)
    art_path = os.path.join(rundir, "art.jpg")
    open(art_path, "wb").write(img)
    crop = os.path.join(rundir, "art_16x9.jpg")
    _draw.crop_169(art_path, crop)
    mp4, frames, log = _draw.render(crop, os.path.join(rundir, "anim"),
                                    knobs, duration_ms=a.dur or lora["pipeline"]["duration_ms"],
                                    no_hand=not a.hand)
    recipe = {"preset": a.style, "chapter": ch["n"], "start_min": ch["start_min"],
              "chapter_text": ch["text"][:300], "prompt": prompt,
              "style": lora["art"]["style"], "model": a.model, "env": knobs,
              "no_hand": not a.hand, "duration_ms": a.dur}
    json.dump(recipe, open(os.path.join(rundir, "recipe.json"), "w"), indent=1)
    ch["render"] = mp4
    json.dump(data, open(a.board, "w"), indent=1)
    print("mp4:", mp4)
    prefix = f"powoutputs/films/{a.film}/" if a.film else "powoutputs/test/"
    if not a.no_ship:
        print("shipped:", _ship.publish(mp4, f"{data['name']}-ch{a.n:02d}", recipe, prefix))
    else:
        print("(no-ship)")


def cmd_new(a):
    import shutil
    fdir = os.path.join(HERE, "films", a.name)
    os.makedirs(fdir, exist_ok=True)
    if a.script:
        shutil.copy(a.script, os.path.join(fdir, "source.txt"))
    flow = os.path.join(fdir, "flow.md")
    if not os.path.exists(flow):
        with open(flow, "w") as fh:
            fh.write(f"# {a.name} — visual flow treatment (v1)\n\n"
                     "Source: films/%s/source.txt\n" % a.name +
                     "Law: start with beautiful landscape. One image per 5-min chunk,\n"
                     "homage to the words or contemplation tool. Mix it up, no formula.\n\n"
                     "## Shots (hour one)\n\n"
                     "| # | Min | Image | Why | Style | Status |\n"
                     "|---|---|---|---|---|---|\n"
                     "| 1 | 0 | landscape (banked?) | opener: the world | lora2 | todo |\n"
                     "\nThen: black + bed.\n")
    print("film dir:", fdir)


def cmd_status(a):
    import glob
    fdir = os.path.join(HERE, "films", a.name)
    if not os.path.isdir(fdir):
        sys.exit(f"no such film: {a.name} (cli.py new --name {a.name})")
    print(f"== {a.name} ==")
    for f in sorted(os.listdir(fdir)):
        print(" ", f)
    boards = sorted(glob.glob(os.path.join(fdir, "*.json")) +
                    glob.glob(os.path.join(HERE, "runs", f"{a.name}-*", "chapters.json")))
    for b in boards:
        try:
            data = json.load(open(b))
        except Exception:
            continue
        chs = data.get("chapters", [])
        done = sum(1 for c in chs if c.get("render"))
        print(f"  board {os.path.basename(os.path.dirname(b))}: {done}/{len(chs)} rendered")


def cmd_make(a):
    lora = _lora1()
    knobs = dict(lora["env"])
    for s in a.set or []:
        k, v = s.split("=", 1)
        knobs[k.strip()] = v.strip()
    no_hand = not a.hand
    stamp = time.strftime("%H%M%S")
    rundir = os.path.join(HERE, "runs", f"{a.name}-{stamp}")
    os.makedirs(rundir, exist_ok=True)
    if a.image:
        src = a.image if os.path.isabs(a.image) else os.path.join(HERE, a.image)
        img = open(src, "rb").read()
    else:
        tok, acc = _cf()
        img = _art.generate(a.prompt, tok, acc, model=a.model, style=a.style)
    art_path = os.path.join(rundir, "art.jpg")
    open(art_path, "wb").write(img)
    crop = os.path.join(rundir, "art_16x9.jpg")
    _draw.crop_169(art_path, crop)
    mp4, frames, log = _draw.render(crop, os.path.join(rundir, "anim"),
                                    knobs, duration_ms=a.dur, no_hand=no_hand)
    recipe = {"preset": "lora1", "prompt": a.prompt, "image": a.image,
              "style": a.style, "model": a.model, "env": knobs,
              "no_hand": no_hand, "duration_ms": a.dur}
    json.dump(recipe, open(os.path.join(rundir, "recipe.json"), "w"), indent=1)
    print("mp4:", mp4)
    for f in frames:
        print("frame:", f)
    prefix = f"powoutputs/films/{a.film}/" if a.film else "powoutputs/test/"
    if not a.no_ship:
        key = _ship.publish(mp4, a.name, recipe, prefix)
        print("shipped:", key)
    else:
        print("(no-ship)")


def main():
    p = argparse.ArgumentParser(prog="sleepdraw")
    sub = p.add_subparsers(dest="cmd", required=True)
    m = sub.add_parser("make")
    m.add_argument("--prompt", default="")
    m.add_argument("--image", default="")
    m.add_argument("--name", required=True)
    m.add_argument("--style", default="pencil")
    m.add_argument("--model", default="flux")
    m.add_argument("--dur", type=int, default=30000)
    m.add_argument("--set", action="append", help="WB_SKIP=6 (repeatable)")
    m.add_argument("--hand", action="store_true", help="keep the hand")
    m.add_argument("--film", default="", help="ship to powoutputs/films/<film>/ (default: test/)")
    m.add_argument("--no-ship", action="store_true")
    b = sub.add_parser("board")
    b.add_argument("--script", required=True)
    b.add_argument("--name", required=True)
    b.add_argument("--wpm", type=int, default=110)
    b.add_argument("--chapter-min", type=int, default=5)
    s = sub.add_parser("shot")
    s.add_argument("--board", required=True)
    s.add_argument("--n", type=int, required=True)
    s.add_argument("--prompt", default="")
    s.add_argument("--image", default="")
    s.add_argument("--name", default="")
    s.add_argument("--style", default="lora2", choices=["lora1", "lora2"])
    s.add_argument("--model", default="flux")
    s.add_argument("--dur", type=int, default=0)
    s.add_argument("--set", action="append", help="WB_SKIP=6 (repeatable)")
    s.add_argument("--hand", action="store_true")
    s.add_argument("--film", default="", help="ship to powoutputs/films/<film>/ (default: test/)")
    s.add_argument("--no-ship", action="store_true")
    n = sub.add_parser("new")
    n.add_argument("--name", required=True)
    n.add_argument("--script", default="")
    st = sub.add_parser("status")
    st.add_argument("--name", required=True)
    sub.add_parser("lora1")
    a = p.parse_args()
    if a.cmd == "lora1":
        print(open(os.path.join(HERE, "lora1.yaml")).read())
    elif a.cmd == "new":
        cmd_new(a)
    elif a.cmd == "status":
        cmd_status(a)
    elif a.cmd == "board":
        path, chapters = _board.board(a.script, a.name, a.wpm, a.chapter_min)
        print(f"{len(chapters)} chapters -> {path}")
        for c in chapters:
            print(f"  ch{c['n']:02d} @{c['start_min']}min ({c['words']}w) seed: {', '.join(c['seed'])}")
    elif a.cmd == "shot":
        cmd_shot(a)
    else:
        if not a.prompt and not a.image:
            sys.exit("need --prompt or --image")
        cmd_make(a)


if __name__ == "__main__":
    main()
