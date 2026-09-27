"""Ship stage: R2 upload + recipe meta. Creds from env or a KEY=VAL file."""
import json
import os

R2_BUCKET = os.environ.get("R2_BUCKET", "blog-video-assets")


def load_env_file(path=None):
    """Shell `source` without export does NOT propagate to children, so load
    the vault file ourselves. Never commit this file."""
    path = path or os.environ.get("SLEEPDRAW_ENV_FILE", "/root/.r2-env")
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip().strip("'\""))
    except OSError:
        pass


def r2_upload(local, key, ctype="video/mp4"):
    load_env_file()
    import boto3
    from botocore.client import Config
    s = boto3.client(
        "s3", endpoint_url=os.environ["R2_ENDPOINT"],
        aws_access_key_id=os.environ["R2_ACCESS_KEY"],
        aws_secret_access_key=os.environ["R2_SECRET_KEY"],
        region_name="auto", config=Config(signature_version="s3v4"))
    with open(local, "rb") as f:
        s.put_object(Bucket=os.environ.get("R2_BUCKET", R2_BUCKET),
                     Key=key, Body=f, ContentType=ctype)
    return key


def publish(mp4, title, recipe, prefix="powoutputs/test/"):
    base = "".join(c if c.isalnum() else "-" for c in title.lower())[:50].strip("-")
    key = f"{prefix}{base}.mp4"
    r2_upload(mp4, key)
    meta = {"key": key, "title": "TEST " + title, "channel": "test",
            "recipe": recipe}
    mp = mp4 + ".meta.json"
    json.dump(meta, open(mp, "w"), indent=1)
    r2_upload(mp, f"{prefix}{base}.json", "application/json")
    return key
