# รีวิว plugin `pi-commit` 1.1.0

วันที่ 2026-10-12 · commit ที่รีวิว `2d7aed6` · รีวิวโดย Claude (Claude Code) และ Codex ตรวจซ้ำแยกกันอย่างอิสระ

## สรุป

- **ยังไม่ควร rollout ให้ทั้งทีมในสภาพปัจจุบัน** เป้าหมายดีแล้ว คือทำ commit ให้เป็นมาตรฐาน ไม่ต้องใช้ secret และไม่เรียก API หรือ DB
  แต่หลังติดตั้ง repo ที่ใช้ค่า global `core.hooksPath` (ไม่มีการตั้งค่าเฉพาะ repo ทับ) จะไม่เรียก hook ชนิดอื่นใน `.git/hooks/` อีก
  โดยไม่มีคำเตือน ทั้ง repo ทีมและ repo ส่วนตัว
- **สิ่งที่ดีอยู่แล้ว:**
  - ไม่พบการอ่านไฟล์ credential หรือการเรียกบริการเครือข่ายโดยตรงในโค้ด pi-commit ที่รีวิว
    แต่ hook ของ repo และคำสั่ง trailer ที่ผู้ใช้ตั้งไว้สามารถรันโปรแกรมอื่นได้
  - `tests/test_pi_commit.py` ผ่าน 50/50 บน git 2.43
  - บังคับ LF และรองรับ CRLF
  - setup ไม่ทับ `core.hooksPath` ของเครื่องมืออื่น
- **ข้อเสนอระยะสั้น:**
  - ปรับเป็น skill ที่ร่างข้อความเมื่อผู้ใช้สั่ง โดยตัดข้อบังคับ setup ออก
  - แก้ขั้นตอนแยก commit ให้รักษาส่วน staged และ unstaged ไว้ก่อนเผยแพร่
  - ไม่ติดตั้ง hook และไม่แก้ git config แบบ global
  - ค่อยเปิด hook หลังแก้ข้อ 1–7

| ระดับ | จำนวน |
|---|---|
| ต้องแก้ก่อน rollout | 2 |
| สำคัญ (hook ยังเชื่อถือไม่ได้) | 5 |
| เล็กน้อย | 3 |
| ยังไม่ได้ทดสอบ | Windows |

## ต้องแก้ก่อน rollout

### 1. hook ชนิดอื่นใน `.git/hooks/` ไม่ถูกเรียก

- **ที่ไหน:** `plugins/pi-commit/scripts/setup.sh:68-69`, `plugins/pi-commit/scripts/commit-msg:10-13`
- **อาการ:**
  - setup ตั้ง `core.hooksPath` แบบ global ทำให้ git หา hook จาก `~/.config/pi-claude-md/git-hooks` ที่เดียว
  - repo ที่รับค่า global นี้และไม่ได้ตั้ง `core.hooksPath` ทับเอง จะไม่เรียก hook ชนิดอื่นใน `.git/hooks/` อีก
    เช่น `pre-commit`, `pre-push` และ hook ของ git-lfs ทั้ง repo ทีมและ repo ส่วนตัว
  - `commit-msg` เดิมของ repo ยังถูกส่งต่อ แต่ส่งต่อได้เฉพาะชนิด `commit-msg` เท่านั้น
- **ผลทดสอบ:** `pre-commit` และ `pre-push` ที่ตั้งใจให้ fail ถูกข้ามหลังติดตั้ง กรณี git-lfs ยังไม่ได้ทดสอบจริง
- **แนวทางแก้:**
  - เลี่ยง global `core.hooksPath` เช่นติดตั้ง `commit-msg` ราย repo โดยเก็บ hook เดิมไว้
  - ถ้าจะใช้แบบกลาง ต้องมี shim ส่งต่อ hook ทุกชนิดไปยัง hook ของ repo ให้ได้ argument, stdin และ exit code เดิม พร้อม test ยืนยัน
  - `includeIf` ที่จำกัดเฉพาะ remote ของทีมช่วยลดจำนวน repo ที่โดน แต่ไม่ได้แก้ปัญหานี้ใน repo ทีม

### 2. การแยก commit ทำให้งานที่ยังไม่ stage ติดเข้า commit

- **ที่ไหน:** `plugins/pi-commit/skills/commit/SKILL.md:23-25`
- **อาการ:** ขั้นตอนแยก commit ใช้ `git reset -q` แล้ว `git add <ไฟล์>` ซึ่ง stage ทั้งไฟล์
  บรรทัดที่ผู้ใช้ตั้งใจไม่ stage เช่นที่เลือกด้วย `git add -p` จึงติดเข้า commit ไปด้วย
- **แนวทางแก้:**
  - ถ้าไฟล์มีทั้งส่วนที่ staged และ unstaged อย่าแยก commit อัตโนมัติ ให้ผู้ใช้ stage เอง
  - เพิ่ม test ยืนยันว่าบรรทัดที่ไม่ได้ stage ไม่ติดเข้า commit ใดเลย

## สำคัญ — hook ยังเชื่อถือไม่ได้

### 3. ชื่อผู้ commit เปลี่ยนในทุก repo ที่ใช้ชื่อ global

- **ที่ไหน:** `setup.sh:68-75`, `setup.sh:83-95`
- **อาการ:**
  - setup ตั้ง `user.name` แบบ global เป็นรหัสพนักงาน
    repo ที่ไม่ได้ตั้ง `user.name` เอง รวมถึง repo ส่วนตัวและ open source จึงได้ชื่อผู้ commit เป็น `1234` ไปด้วย
  - setup ตั้ง `commit.template` แบบ global เมื่อยังไม่มีค่าเดิม หรือค่าเดิมเป็นของ pi-commit อยู่แล้ว
  - uninstall คืนชื่อก่อนติดตั้งเสมอ แม้ผู้ใช้จะเปลี่ยนชื่อเองภายหลังแล้ว
- **แนวทางแก้:**
  - ตั้งชื่อเฉพาะ repo ทีม จะตั้งราย repo หรือใช้ `includeIf "hasconfig:remote.*.url:..."` ก็ได้ (ต้องใช้ git 2.36 ขึ้นไป)
  - ระวังว่า pattern ของ `includeIf` แยกตัวพิมพ์เล็กใหญ่ ต่างจาก hook ที่แปลง remote เป็นตัวเล็ก
    ต้องเขียน pattern ให้ครบทั้ง https, `git@github.com:` และ `ssh://` และทดสอบด้วยชุด remote เดียวกับ hook
  - uninstall ควรคืนเฉพาะค่าที่ยังเป็นของ pi-commit อยู่

### 4. setup แจ้งว่า "installed" ทั้งที่ล้มเหลว

- **ที่ไหน:** `setup.sh:63-79`, `setup.sh:83-95`
- **อาการ:**
  - setup ตรวจผลเฉพาะ `mkdir` และ `cp`
  - ถ้า `git config --global` ตัวใดเขียนไม่สำเร็จ ยังพิมพ์ `pi-commit installed` และ exit 0 ทั้งที่ค่าบางตัวเปลี่ยนไปแล้วและบางตัวยังไม่เปลี่ยน
  - การ copy hook เขียนทับไฟล์เดิมตรง ๆ ไม่ใช่การแทนที่แบบ atomic
- **แนวทางแก้:**
  - ตรวจผลทุกคำสั่งที่แก้ config หรือไฟล์
  - ตรวจค่าจริงก่อนพิมพ์ installed หรือ removed
  - ถ้าทำสำเร็จแค่บางส่วน ให้บอกตรง ๆ พร้อมวิธีกู้คืน

### 5. trailer `Emp:` ไม่น่าเชื่อถือ

- **ที่ไหน:** `plugins/pi-commit/scripts/commit-msg:66-68`
- **ทำไมสำคัญ:** เฟสถัดไปจะอ่าน commit ไปอัปเดต task จึงต้องพึ่ง trailer นี้
- **อาการ:**
  - ถ้ามี `Emp:` อยู่แล้วหลายบรรทัด จะเหลือหลายค่า เช่น `Emp: 9999` กับ `Emp: 1234`
  - config `trailer.*` ของผู้ใช้ทำให้ไม่มี `Emp:` เลย เปลี่ยน separator หรือเปลี่ยนค่าได้
  - ถ้า `git interpret-trailers` ทำงานไม่สำเร็จ commit ยังผ่านไปได้โดยไม่มี `Emp:`
- **แนวทางแก้:**
  - กำหนด trailer มาตรฐานตัวเดียว และลบค่าที่ซ้ำ
  - ควบคุมหรือปฏิเสธเฉพาะการตั้งค่าที่ทำให้ `Emp:` ผิดมาตรฐาน โดยรักษา body, `deploy!` และ trailer อื่นไว้
  - ตรวจ exit code และผลลัพธ์จริงก่อนยอมรับ commit

### 6. hook ตรวจคนละบรรทัดกับที่ git บันทึกจริง

- **ที่ไหน:** `plugins/pi-commit/scripts/commit-msg:26-27`
- **อาการ:**
  - hook ตัดบรรทัดที่ขึ้นต้นด้วย `#` ทิ้งเสมอ
  - แต่ `git commit -m` ตามค่าเริ่มต้นใช้ cleanup แบบ whitespace จึงเก็บบรรทัด `#` ไว้
    subject ที่บันทึกจริงจึงเป็นบรรทัด `#` ที่ผิด format แต่ hook ปล่อยผ่าน
  - เมื่อตั้ง `core.commentChar=';'` และใช้ `--cleanup=strip` message ที่ถูกต้องซึ่งมีบรรทัด comment แบบ `;` จะถูกปฏิเสธ
- **แนวทางแก้:** ตีความ message ให้ตรงกับ cleanup mode และ comment char ที่ git ใช้จริง
  หรือจำกัดรูปแบบที่รองรับ แล้วปฏิเสธพร้อมบอกเหตุผลเมื่อไม่ตรง

### 7. `status` ขึ้น OK ไม่ได้แปลว่า repo นี้ถูกตรวจ

- **ที่ไหน:** `setup.sh:98-107`, `skills/commit/SKILL.md:18-19`, `skills/commit/SKILL.md:36`
- **อาการ:**
  - status ดูเฉพาะค่า global
  - repo ที่ตั้ง `core.hooksPath` เอง (แบบ husky) จะข้าม pi-commit เงียบ ๆ
  - repo ที่ตั้ง `user.name` เองเป็นค่าที่ไม่ใช่รหัสพนักงาน 4 หลัก จะถูก hook ปฏิเสธทุกครั้ง
    แต่ skill สั่งให้แก้ message แล้วลองใหม่ ซึ่งแก้ไม่หายและวนไม่จบ
- **แนวทางแก้:**
  - ตรวจค่าที่มีผลจริงใน repo ปัจจุบัน ได้แก่ hooksPath และ user.name และบอกด้วยว่าค่ามาจากไหน
  - แยกวิธีกู้ตามชนิดของปัญหา ถ้าเป็นปัญหา config ให้หยุดและบอกผู้ใช้

## เล็กน้อย

8. **guard ข้ามได้** (`plugins/pi-commit/scripts/block-no-verify.sh`)
   - คำสั่งเหล่านี้ผ่าน guard ได้:
     - `git commit --no-veri` เพราะ git รับตัวย่อของ option
     - `git -c core.hookspath=...` ที่เขียนตัวเล็ก
     - `git config core.hooksPath ... && git commit`
   - guard ยัง block `--no-verify` ใน repo ที่ไม่ใช่ของทีมด้วย
   - ใช้เป็นด่านเตือนได้ แต่ไม่ควรเรียกว่าการบังคับ
9. **ช่องว่างของ format** ควรระบุให้ชัดว่านี่คือ convention ของทีมที่แคบกว่า Conventional Commits
   - `feat(api)!:` ถูกปฏิเสธ ทั้งที่เป็นเครื่องหมาย breaking change ของ Conventional Commits
   - `update code.` ที่มีจุดท้าย ผ่านการตรวจคำกว้าง ๆ
   - scope ตัวพิมพ์ใหญ่ผ่าน ทั้งที่เอกสารบอกให้ใช้ตัวเล็ก
10. **อัปเดต plugin แล้ว hook ที่ติดตั้งไว้ไม่อัปเดตตาม**
    - setup ใช้วิธี copy hook ไม่ได้ link ไว้
    - `skills/setup/SKILL.md:18-19` จบทันทีเมื่อ status เป็น OK จึงไม่ถึงขั้นที่ copy hook ตัวใหม่
    - การถอน plugin ไม่ลบ config และ hook ที่ copy ไว้

**Windows:** ยังไม่ได้ทดสอบบนเครื่อง Windows จริง ซึ่งไม่ได้แปลว่าพัง ควรทดสอบกรณีเหล่านี้:
- ใช้ Git Bash
- เปิด Claude จาก PowerShell
- path ที่มีช่องว่างหรือภาษาไทย
- commit จาก VS Code
- setup, status และ uninstall

## สำหรับเฟสถัดไป (service อ่าน commit ไปอัปเดต task)

- hook บนเครื่อง dev รับประกันไม่ได้ว่าทุก commit ใน main ถูก format หรือมี `Emp:` เพราะ:
  - merge, revert, fixup และ commit ที่มีแค่ `deploy!` ได้รับยกเว้น
  - `-n` ข้าม hook ได้
  - merge บน GitHub ไม่ผ่าน hook
  - hook อื่นของ repo แก้ message หลัง pi-commit ได้
- service ต้องรองรับ commit ที่ไม่มี `Emp:` หรือมีหลายค่า และควรมีการตรวจฝั่ง GitHub ในเฟสนั้น
- ยังไม่จำเป็นต้องเพิ่ม field `Task:` ตอนนี้ scope ยังเป็นชื่อส่วนของระบบตามเดิม

## วิธีทดสอบซ้ำ 5 ประเด็น (ข้อ 1, 2, 3, 5, 6)

สำหรับ Linux หรือ Git Bash ให้รันจาก root ของ repo ข้ออื่นมาจากการอ่าน source และการทดสอบแยกของผู้รีวิว ไม่ได้ใส่คำสั่งไว้ที่นี่

- คำสั่งรันใน child process ที่ล้าง environment ด้วย `env -i` และใช้ `HOME`, `XDG_CONFIG_HOME` และ `GIT_CONFIG_GLOBAL` ชั่วคราว จึงไม่แตะ git config จริงของเครื่อง
- ถ้าขั้นตอนใดล้มเหลว script จะหยุดทันที (`set -eu`)
- ไฟล์ทดสอบอยู่ในโฟลเดอร์ที่พิมพ์ออกมาในบรรทัดแรก (`fixture: ...`) และไม่ถูกลบอัตโนมัติ ลบเองได้เมื่อทดสอบเสร็จ

```bash
(
  set -eu
  PLUGIN="$PWD/plugins/pi-commit/scripts"
  test -f "$PLUGIN/setup.sh"
  ROOT="$(mktemp -d)"
  echo "fixture: $ROOT"
  env -i PATH="$PATH" LC_ALL=C.UTF-8 \
    HOME="$ROOT/home" XDG_CONFIG_HOME="$ROOT/home/.config" \
    GIT_CONFIG_GLOBAL="$ROOT/home/.gitconfig" GIT_CONFIG_NOSYSTEM=1 \
    PLUGIN="$PLUGIN" ROOT="$ROOT" sh -eu <<'EOF'
mkdir "$HOME" "$ROOT/team" "$ROOT/personal"
git config --global user.email demo@example.com
sh "$PLUGIN/setup.sh" install 1234 >/dev/null
cd "$ROOT/team"
git init -q
git remote add origin https://github.com/tycthailand/demo.git

echo "--- 1"
printf '#!/bin/sh\necho "pre-commit ran" >&2\nexit 1\n' > .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
if git commit -q --allow-empty -m "fix(login): แก้ปุ่มบันทึกกดไม่ได้" 2>/dev/null; then
  echo "commit ผ่าน แม้ pre-commit จะ exit 1"
else
  echo "pre-commit ถูกเรียกแล้ว"
fi
rm .git/hooks/pre-commit

echo "--- 2"
printf 'a\nb\n' > f.txt
git add f.txt
git commit -q -m "feat: เพิ่มไฟล์ตัวอย่างสำหรับทดสอบ"
printf 'A\nb\n' > f.txt
git add f.txt
printf 'A\nB-wip\n' > f.txt
echo "staged ก่อน reset:"
git diff --cached | grep '^+[^+]' || true
git reset -q
git add f.txt
echo "staged หลัง reset + add:"
git diff --cached | grep '^+[^+]' || true

echo "--- 5"
git commit -q --allow-empty -m "fix(login): แก้ปุ่มบันทึกกดไม่ได้" -m "Emp: 9999
Emp: 8888"
git log -1 --format=%B | grep '^Emp:' || true

echo "--- 6"
if git commit -q --allow-empty -m "# ไม่ใช่ subject ที่ถูกต้อง" -m "fix(login): แก้ปุ่มบันทึกกดไม่ได้" 2>/dev/null; then
  git log -1 --format=%s
else
  echo "hook ปฏิเสธ"
fi

echo "--- 3"
cd "$ROOT/personal"
git init -q
git remote add origin https://github.com/someone/personal.git
git commit -q --allow-empty -m "personal work"
git log -1 --format='author=%an'
EOF
)
```

ผลที่ได้บน git 2.43 (Linux):

```
fixture: /tmp/tmp.XXXXXXXXXX
--- 1
commit ผ่าน แม้ pre-commit จะ exit 1
--- 2
staged ก่อน reset:
+A
staged หลัง reset + add:
+A
+B-wip
--- 5
Emp: 9999
Emp: 1234
--- 6
# ไม่ใช่ subject ที่ถูกต้อง
--- 3
author=1234
```

ความหมายของแต่ละข้อ:
- **ข้อ 1:** commit ผ่านทั้งที่ `pre-commit` exit 1
- **ข้อ 2:** ก่อน reset มีเพียงบรรทัด `A` ที่ staged แต่หลังทำตามขั้นตอนของ skill แล้ว `B-wip` ติดเข้ามาด้วย
- **ข้อ 5:** มี `Emp:` สองค่า
- **ข้อ 6:** subject ที่บันทึกจริงผิด format แต่ผ่าน hook
- **ข้อ 3:** repo ส่วนตัวได้ชื่อผู้ commit เป็น `1234`
