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
    if not a.no_ship:
        key = _ship.publish(mp4, a.name, recipe)
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
    m.add_argument("--no-ship", action="store_true")
    sub.add_parser("lora1")
    a = p.parse_args()
    if a.cmd == "lora1":
        print(open(os.path.join(HERE, "lora1.yaml")).read())
    else:
        if not a.prompt and not a.image:
            sys.exit("need --prompt or --image")
        cmd_make(a)


if __name__ == "__main__":
    main()
