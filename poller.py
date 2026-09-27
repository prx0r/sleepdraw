"""Render poller: R2 job queue -> sleepdraw pipeline -> test channel.

Edge review page writes powoutputs/jobs/<id>.json {queued}; this loop claims,
renders (lora1 30s default, lora2 2min), ships to powoutputs/test/, marks done.
One poller per box (claim = rewrite status; single consumer, no races).
Run: nohup python3 poller.py > runs/poller.log 2>&1 &
"""
import json
import os
import sys
import time
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
BOX = os.uname().nodename

from sleepdraw import art as _art, draw as _draw, ship as _ship  # noqa: E402
import yaml  # noqa: E402


def _cf():
    for line in open(os.environ.get("SLEEPDRAW_ENV_FILE", "/root/.r2-env")):
        line = line.strip()
        if line and "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip().strip("'\""))
    return os.environ["CF_API_TOKEN"], os.environ["CF_ACCOUNT_ID"]


def _r2():
    _cf()
    import boto3
    from botocore.client import Config
    return boto3.client(
        "s3", endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
        region_name="auto", config=Config(signature_version="s3v4"))


def _bucket():
    return os.environ.get("R2_BUCKET", "blog-video-assets")


def _preset(style):
    with open(os.path.join(HERE, "lora1.yaml" if style == "lora1" else "lora2.yaml")) as f:
        return yaml.safe_load(f)


def _get(s, key):
    return json.loads(s.get_object(Bucket=_bucket(), Key=key)["Body"].read() or b"{}")


def _put(s, key, obj):
    s.put_object(Bucket=_bucket(), Key=key, Body=json.dumps(obj, indent=1).encode(),
                 ContentType="application/json")


def run_job(s, key, job):
    lora = _preset(job.get("style", "lora2"))
    knobs = dict(lora["env"])
    for kv in job.get("set", []) or []:
        if "=" in kv:
            k, v = kv.split("=", 1)
            knobs[k.strip()] = v.strip()
    dur = job.get("dur", lora["pipeline"]["duration_ms"])
    tok, acc = _cf()
    img = _art.generate(job["prompt"], tok, acc, model=job.get("model", "flux"),
                        style=lora["art"]["style"])
    rd = os.path.join(HERE, "runs", f"job-{job['id']}")
    os.makedirs(rd, exist_ok=True)
    ap = os.path.join(rd, "art.jpg")
    open(ap, "wb").write(img)
    crop = os.path.join(rd, "art_16x9.jpg")
    _draw.crop_169(ap, crop)
    mp4, frames, log = _draw.render(crop, os.path.join(rd, "anim"), knobs,
                                    duration_ms=dur, no_hand=True)
    recipe = {"preset": job.get("style", "lora2"), "job": job["id"],
              "prompt": job["prompt"], "style": lora["art"]["style"],
              "model": job.get("model", "flux"), "env": knobs,
              "no_hand": True, "duration_ms": dur, "box": BOX}
    json.dump(recipe, open(os.path.join(rd, "recipe.json"), "w"), indent=1)
    return _ship.publish(mp4, f"job-{job['id']}", recipe)


def poll_once():
    s = _r2()
    r = s.list_objects_v2(Bucket=_bucket(), Prefix="powoutputs/jobs/")
    for o in r.get("Contents", []):
        key = o["Key"]
        if not key.endswith(".json"):
            continue
        job = _get(s, key)
        if job.get("status") != "queued":
            continue
        job["status"], job["box"] = "claimed", BOX
        _put(s, key, job)
        print(f"[{time.strftime('%H:%M:%S')}] claimed {job.get('id')}: "
              f"{job.get('prompt', '')[:60]}", flush=True)
        try:
            out = run_job(s, key, job)
            job["status"], job["result"] = "done", out
        except Exception as e:  # noqa: BLE001
            job["status"], job["error"] = "error", str(e)[:500]
            traceback.print_exc()
        _put(s, key, job)
        print(f"[{time.strftime('%H:%M:%S')}] {job['id']} -> {job['status']}",
              flush=True)


if __name__ == "__main__":
    print(f"poller up on {BOX}, prefix powoutputs/jobs/", flush=True)
    while True:
        try:
            poll_once()
        except Exception:  # noqa: BLE001
            traceback.print_exc()
        time.sleep(15)
