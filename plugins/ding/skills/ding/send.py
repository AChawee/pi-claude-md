#!/usr/bin/env python3
import argparse, datetime, json, mimetypes, os, re, sys, time, urllib.error, urllib.request, uuid
from pathlib import Path

BASE = "https://dingtalk.tycthailand.com"
CONFIG_DIR = Path.home() / ".config" / "pi-claude-md"
ENV_FILE = CONFIG_DIR / "ding.env"
TOKEN_KEY = "SECRET_AUTH"
TOKEN_PLACEHOLDER = "paste-token-here"
BANGKOK = datetime.timezone(datetime.timedelta(hours=7))
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp", ".tiff", ".ico"}
DOC_EXTS = {".xlsx", ".xls", ".doc", ".docx", ".pdf", ".ppt", ".pptx", ".txt", ".csv", ".md", ".html"}
NGINX_SAFE_DOC_BYTES = 49 * 1024**2
MAX_BYTES = {"images": 10 * 1024**2, "docs": NGINX_SAFE_DOC_BYTES}
FILE_TTL_DAYS = 7
STORAGE_PURGE_HOUR = 3
MAX_ATTEMPTS_ON_502 = 4


def init_env():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not ENV_FILE.exists():
        ENV_FILE.write_text(f"{TOKEN_KEY}={TOKEN_PLACEHOLDER}\n", encoding="utf-8")
    os.chmod(ENV_FILE, 0o600)
    print(f"ไฟล์ .env อยู่ที่: {ENV_FILE}")
    print(f"เปิดไฟล์นี้ด้วย editor แล้วแทน {TOKEN_PLACEHOLDER} ด้วย token จริง (ห้ามวาง token ในแชท)")


def load_token():
    try:
        lines = ENV_FILE.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        return None, f"ยังไม่มีไฟล์ {ENV_FILE} — รัน: python3 send.py --init-env"
    except OSError as e:
        return None, f"อ่าน {ENV_FILE} ไม่ได้: {e.strerror}"
    values = [v.strip().strip("'\"") for k, _, v in (line.partition("=") for line in lines) if k.strip() == TOKEN_KEY]
    if not values:
        return None, f"ไม่พบ {TOKEN_KEY} ใน {ENV_FILE}"
    if values[-1] in ("", TOKEN_PLACEHOLDER):
        return None, f"ยังไม่ได้ใส่ token จริงใน {ENV_FILE} — แทน {TOKEN_PLACEHOLDER} ด้วย token"
    return values[-1], None


def read_token():
    token, problem = load_token()
    if problem:
        sys.exit(problem)
    return token


def check_env():
    read_token()
    print(f"OK: พบ {TOKEN_KEY} ใน {ENV_FILE}")


def kind_of(path):
    return "images" if path.suffix.lower() in IMAGE_EXTS else "docs"


def check_files(paths):
    errors = []
    for path in paths:
        ext = path.suffix.lower()
        if not path.is_file():
            errors.append(f"ไม่พบไฟล์: {path}")
        elif ext not in IMAGE_EXTS | DOC_EXTS:
            errors.append(f"{path.name}: นามสกุล '{ext or '(ไม่มี)'}' อัปโหลดไม่ได้")
        elif re.search(r'[\\#?%"\r\n]', path.name):
            errors.append(f"{path.name}: ชื่อไฟล์มี \\ # ? % \" หรือขึ้นบรรทัดใหม่ — API ตอบ 400 ให้เปลี่ยนชื่อก่อน")
        elif path.stat().st_size > MAX_BYTES[kind := kind_of(path)]:
            errors.append(f"{path.name}: {path.stat().st_size / 1024**2:.1f} MB เกินเพดาน {kind} ({MAX_BYTES[kind] // 1024**2} MB)")
    return errors


def check_tags(tags, msg):
    errors = []
    for t in tags:
        for m in re.finditer(re.escape(t), msg):
            before, after = msg[m.start() - 1 : m.start()], msg[m.end() : m.end() + 1]
            if before != "@" or after.isdigit():
                ctx = msg[max(0, m.start() - 15) : m.end() + 15].replace("\n", " ")
                errors.append(f"รหัส {t} ไปโดนข้อความอื่นด้วย: …{ctx}…")
    return errors


def error_text(status, headers, body):
    if "application/json" not in headers.get("content-type", ""):
        return f"HTTP {status} (ถูกปฏิเสธที่ nginx — ไม่ได้ส่ง header / method ผิด / body เกิน 1 MB)"
    try:
        data = json.loads(body)
    except ValueError:
        return body[:200] or f"HTTP {status}"
    d = data.get("detail", data) if isinstance(data, dict) else data
    if isinstance(d, list) and all(isinstance(e, dict) and "loc" in e and "msg" in e for e in d):
        return "; ".join(f"{'.'.join(map(str, e['loc']))}: {e['msg']}" for e in d)
    return str(d)


def unreachable(e):
    reason = getattr(e, "reason", e)
    sys.exit(f"เชื่อมต่อ {BASE} ไม่ได้ ({reason}) — ตรวจว่าต่อเครือข่ายบริษัท/VPN แล้วลองใหม่ (ยังไม่ได้ส่งข้อความ)")


def post(payload, token):
    req = urllib.request.Request(
        f"{BASE}/api/notify/",
        data=json.dumps(payload).encode(),
        headers={"X-Authentication": token, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.status, error_text(e.status, e.headers, e.read().decode("utf-8", "replace"))
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        unreachable(e)


def upload(path, token):
    kind = kind_of(path)
    boundary = "----ding" + uuid.uuid4().hex
    ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    body = (
        f'--{boundary}\r\nContent-Disposition: form-data; name="kind"\r\n\r\n{kind}\r\n'
        f'--{boundary}\r\nContent-Disposition: form-data; name="file"; filename="{path.name}"\r\n'
        f"Content-Type: {ctype}\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(
        f"{BASE}/api/upload/",
        data=body,
        headers={"X-Authentication": token, "Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return kind, json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        sys.exit(f"FAILED upload {path.name} {e.status}: {error_text(e.status, e.headers, e.read().decode('utf-8', 'replace'))}")
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        unreachable(e)


def parse_args():
    p = argparse.ArgumentParser(description="ส่งข้อความ markdown เข้ากลุ่ม DingTalk ผ่าน dingtalk-notify")
    setup = p.add_mutually_exclusive_group()
    setup.add_argument("--init-env", action="store_true", help=f"สร้าง {ENV_FILE} (ถ้ายังไม่มี) แล้วจบ")
    setup.add_argument("--check-env", action="store_true", help=f"ตรวจว่า {ENV_FILE} มี token แล้ว โดยไม่แสดงค่า")
    p.add_argument("--channel")
    p.add_argument("--hashtag")
    p.add_argument("--message-file")
    p.add_argument("--tags", default="all", help='"all" หรือรหัสพนักงานคั่นด้วย comma')
    p.add_argument("--file", action="append", default=[], help="แนบไฟล์ (ใส่ซ้ำได้) — รูปฝังในข้อความ เอกสารเป็นลิงก์")
    p.add_argument("--dry-run", action="store_true", help="พิมพ์ข้อความฉบับที่จะส่งจริง โดยไม่อัปโหลดและไม่ส่ง")
    a = p.parse_args()
    if not (a.init_env or a.check_env):
        missing = [f"--{n.replace('_', '-')}" for n in ("channel", "hashtag", "message_file") if not getattr(a, n)]
        if missing:
            p.error("ต้องระบุ " + ", ".join(missing))
    return a


def parse_tags(raw):
    if raw == "all":
        return "all"
    tags = [t.strip() for t in raw.split(",") if t.strip()]
    if not tags:
        sys.exit('--tags ว่าง: ข้อความจะเข้ากลุ่มแต่ไม่มีใครได้แจ้งเตือน — ใช้ "all" หรือใส่รหัสพนักงาน')
    return tags


def attachment_expiry():
    now = datetime.datetime.now(BANGKOK)
    return (now + datetime.timedelta(days=FILE_TTL_DAYS, hours=-STORAGE_PURGE_HOUR)).date()


def send(payload, token):
    for attempt in range(MAX_ATTEMPTS_ON_502):
        status, body = post(payload, token)
        if status != 502 or attempt == MAX_ATTEMPTS_ON_502 - 1:
            return status, body
        time.sleep(2**attempt)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    a = parse_args()
    if a.init_env:
        return init_env()
    if a.check_env:
        return check_env()

    msg = Path(a.message_file).read_text(encoding="utf-8")
    tags = parse_tags(a.tags)
    paths = [Path(fp) for fp in a.file]
    errors = check_files(paths) + (check_tags(tags, msg) if tags != "all" else [])
    if errors:
        sys.exit("ยังไม่ได้อัปโหลด/ส่งอะไร:\n" + "\n".join(f"  - {e}" for e in errors))

    token = None if a.dry_run else read_token()
    for path in paths:
        if a.dry_run:
            kind, name, link = kind_of(path), path.name, f"<url ของ {path.name}>"
        else:
            kind, info = upload(path, token)
            name = info.get("filename", path.name)
            link = info.get("view_url") or info.get("url")
            if not link:
                sys.exit(f"อัปโหลด {path.name} แล้วแต่ API ไม่คืนลิงก์ — ยังไม่ได้ส่งข้อความ ลองใหม่อีกครั้ง")
            print(f"uploaded {path.name} -> {link}")
        msg += f"\n\n![{name}]({link})" if kind == "images" else f"\n\n- [{name}]({link})"

    if paths:
        msg += f"\n\n> ไฟล์แนบเปิดได้ถึง {attachment_expiry():%Y-%m-%d}"

    if tags != "all" and not a.dry_run and (errors := check_tags(tags, msg)):
        sys.exit("อัปโหลดแล้วแต่ยังไม่ส่ง — ลิงก์ไฟล์มีเลขตรงกับรหัสพนักงาน:\n" + "\n".join(f"  - {e}" for e in errors))

    payload = {"channel_id": a.channel, "hashtag": a.hashtag, "markdown_msg": msg, "tags": tags}

    if a.dry_run:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        print("\n----- markdown_msg -----\n" + msg)
        print("\nDRY RUN: ยังไม่ได้อัปโหลดและไม่ได้ส่ง")
        return

    status, body = send(payload, token)
    print("OK: ส่งเข้ากลุ่มแล้ว" if status == 200 else f"FAILED {status}: {body}")
    sys.exit(0 if status == 200 else 1)


if __name__ == "__main__":
    main()
