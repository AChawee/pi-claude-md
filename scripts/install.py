#!/usr/bin/env python3
import argparse, json, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MARKETPLACE = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
MARKETPLACE_NAME = MARKETPLACE["name"]
DEFAULT_SOURCE = "ken1lnw/pi-claude-md"
SETUP_SCRIPTS = {"ding": ROOT / "plugins/ding/skills/ding/send.py"}


def claude(*args):
    exe = shutil.which("claude")
    if not exe:
        sys.exit("ไม่พบคำสั่ง claude — ติดตั้ง Claude Code ก่อน: https://code.claude.com/docs/en/setup")
    return subprocess.run([exe, *args], capture_output=True, text=True, encoding="utf-8", timeout=300)


def output_of(r):
    return (r.stderr or r.stdout).strip() or f"exit code {r.returncode}"


def run_setup(name, flag):
    return subprocess.run([sys.executable, str(SETUP_SCRIPTS[name]), flag], capture_output=True, text=True, encoding="utf-8", timeout=30)


def installed_names():
    r = claude("plugin", "list", "--json")
    if r.returncode != 0:
        return set()
    suffix = f"@{MARKETPLACE_NAME}"
    return {p["id"].removesuffix(suffix) for p in json.loads(r.stdout) if p["id"].endswith(suffix)}


def setup_problem(name):
    if name not in SETUP_SCRIPTS:
        return None
    r = run_setup(name, "--check-env")
    return None if r.returncode == 0 else output_of(r)


def list_plugins():
    installed = installed_names()
    rows = [
        {
            "name": p["name"],
            "description": p["description"],
            "installed": p["name"] in installed,
            "needs_setup": p["name"] in SETUP_SCRIPTS,
            "setup_ok": setup_problem(p["name"]) is None,
        }
        for p in MARKETPLACE["plugins"]
    ]
    print(json.dumps(rows, ensure_ascii=False, indent=2))


def setup(name):
    if name not in SETUP_SCRIPTS:
        sys.exit(f"{name} ไม่ต้องตั้งค่าก่อนติดตั้ง")
    r = run_setup(name, "--init-env")
    print(r.stdout.strip())
    sys.exit(r.returncode)


def ensure_marketplace(source):
    r = claude("plugin", "marketplace", "list", "--json")
    if r.returncode == 0 and any(m["name"] == MARKETPLACE_NAME for m in json.loads(r.stdout)):
        r = claude("plugin", "marketplace", "update", MARKETPLACE_NAME)
        action = "อัปเดต"
    else:
        r = claude("plugin", "marketplace", "add", source)
        action = "เพิ่ม"
    if r.returncode != 0:
        sys.exit(f"{action} marketplace {MARKETPLACE_NAME} ไม่สำเร็จ: {output_of(r)}")


def install_one(name, known, installed):
    if name not in known:
        return "ล้มเหลว", "ไม่มี plugin ชื่อนี้ใน marketplace"
    if name in installed:
        return "ข้าม", "ติดตั้งอยู่แล้ว"
    if problem := setup_problem(name):
        return "ข้าม", f"ยังไม่ได้ตั้งค่า — {problem}"
    r = claude("plugin", "install", f"{name}@{MARKETPLACE_NAME}", "--scope", "user")
    if r.returncode != 0:
        return "ล้มเหลว", output_of(r).splitlines()[-1]
    return "ติดตั้งแล้ว", ""


def install(names, source):
    ensure_marketplace(source)
    known = {p["name"] for p in MARKETPLACE["plugins"]}
    installed = installed_names()
    results = [(name, *install_one(name, known, installed)) for name in names]
    print("| plugin | ผล | หมายเหตุ |\n|---|---|---|")
    for name, status, note in results:
        print(f"| {name} | {status} | {note} |")
    if any(status == "ติดตั้งแล้ว" for _, status, _ in results):
        print("\nเปิด session ใหม่ หรือรัน /reload-plugins เพื่อเริ่มใช้ skill ที่ติดตั้ง")
    sys.exit(1 if any(status == "ล้มเหลว" for _, status, _ in results) else 0)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description=f"ติดตั้ง plugin จาก marketplace {MARKETPLACE_NAME}")
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("list", help="แสดง plugin ทั้งหมดเป็น JSON")
    s = sub.add_parser("setup", help="สร้างไฟล์ตั้งค่าที่ plugin ต้องใช้ก่อนติดตั้ง")
    s.add_argument("name")
    i = sub.add_parser("install", help="ติดตั้ง plugin ที่เลือก")
    i.add_argument("names", nargs="+")
    i.add_argument("--source", default=DEFAULT_SOURCE, help="ที่มาของ marketplace (GitHub owner/repo หรือ path)")
    a = p.parse_args()
    if a.command == "list":
        list_plugins()
    elif a.command == "setup":
        setup(a.name)
    else:
        install(a.names, a.source)


if __name__ == "__main__":
    main()
