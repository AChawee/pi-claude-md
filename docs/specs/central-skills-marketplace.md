# Spec: pi-claude-md เป็น Skills Marketplace กลางของทีม

- สถานะ: ready-for-agent
- วันที่: 2026-10-12
- ผู้ขอ: ken1lnw

## Problem Statement

ทีมอยากมีที่เก็บ skill กลางที่ทุกคนติดตั้งได้ง่าย แต่ repo ตอนนี้ยังใช้แบบนั้นไม่ได้:

- วิธีติดตั้งคือ clone แล้ว symlink ทีละโฟลเดอร์ ซึ่งพลาดง่าย (symlink ผิดแบบแล้ว skill ไม่โหลดและไม่มี error) ใช้บน Windows ลำบาก และไม่มีวิธีอัปเดต
- ผู้ติดตั้งเลือกไม่ได้ว่าจะเอา skill ตัวไหน
- skill บางตัวพังอยู่แล้ว: `create-guide` ไม่มี `SKILL.md` (เป็นไฟล์ command เก่า 3 ชุด สองชุดเหมือนกันทุก byte และแต่ละไฟล์ใหญ่ 72–87KB) และ `install-guide` ชี้ไปโฟลเดอร์ที่ไม่มีแล้ว
- ไฟล์ `plugin.json` ตัวอย่างใช้ schema ที่ทีมคิดเอง Claude Code ไม่โหลด
- INDEX.md ไม่ตรงกับของจริง (`tyc-design-system` ตกหล่น ลิงก์ `create-guide` เสีย) เพราะต้องแก้มือ 3 จุดทุกครั้ง
- skill ที่มีประโยชน์กับทั้งทีม เช่น `ding` อยู่ในเครื่องคนเดียว ผูก path ส่วนตัวไว้ตายตัว และเก็บรายชื่อห้อง (channel UUID) ไว้ในโฟลเดอร์ skill
- repo เป็น public จึงต้องมั่นใจว่าไม่มี secret ข้อมูลส่วนตัว หรือ path ของใครหลุดเข้า repo
- ยังไม่มีกติกากลางในการเขียนโค้ดของ repo และไม่มีการ test ก่อนรายงานว่างานเสร็จ
- README มีแต่ภาษาไทย ยังสอนวิธี symlink ไม่บอกว่า repo มี skill อะไรบ้างและแต่ละตัวทำอะไร ไม่มีส่วนแก้ปัญหา ไม่บอกวิธีอัปเดตหรือถอนการติดตั้ง และคนนอกทีมที่เจอ repo public อ่านไม่ออก

## Solution

ทำ repo ให้เป็น **Claude Code plugin marketplace** โดยให้ 1 skill เป็น 1 plugin

- **ติดตั้งแบบเลือกได้:** clone repo แล้วเปิด Claude Code จากนั้นสั่ง `/install-skills` ระบบจะแสดงรายการ skill ให้ติ๊กเลือกได้หลายตัว แล้วติดตั้งให้ทีละตัว ส่วนคนที่ไม่อยาก clone ก็ใช้ `/plugin marketplace add ken1lnw/pi-claude-md` แล้วเลือกจากแท็บ Discover ได้
- **อัปเดตได้:** แต่ละ plugin มี version และเอกสารบอกวิธีเปิด auto-update ไว้
- **`ding` เข้ามาอยู่ใน repo:** ถ้าเลือก `ding` ระบบจะไม่ติดตั้งจนกว่าผู้ใช้จะกรอกไฟล์ `.env` ที่ระบบสร้างไว้ให้ในเครื่อง ไฟล์นี้อยู่นอก repo และ token ไม่ผ่านแชท
- แก้ skill ที่พัง เขียน INDEX.md ใหม่ และอัปเดต CLAUDE.md ให้บอกจุดประสงค์ของ repo และกติกาการเขียนโค้ดของทีม
- มีชุด test คำสั่งเดียวที่ต้องผ่านก่อนรายงานว่างานเสร็จ และ CI รันชุดเดียวกันทุก PR
- **README สองภาษา (ไทย/อังกฤษ):** บอกจุดประสงค์ รายการ skill พร้อมคำอธิบาย วิธีติดตั้งทีละขั้น การอัปเดต การถอนการติดตั้ง การแก้ปัญหา ความปลอดภัย และวิธี contribute

## User Stories

### ผู้ติดตั้ง (สมาชิกทีม)

1. As a team member, I want to install skills with one guided command, so that I don't need to learn symlinks or plugin internals.
2. As a team member, I want to see a list of every available skill with a one-line description before installing, so that I know what each one does.
3. As a team member, I want to pick several skills at once from a checklist, so that I install only what I need.
4. As a team member, I want skills already installed to show as installed, so that I don't install them twice.
5. As a team member, I want a summary of what was installed, skipped, and failed, so that I know the final state without checking it myself.
6. As a team member, I want to install a single skill without cloning, via `/plugin`, so that I can try it quickly.
7. As a team member on Windows, I want the same install flow as on Linux/macOS, so that the OS doesn't matter.
8. As a team member, I want to choose user scope by default (all projects), so that skills work everywhere without extra setup.
9. As a team member, I want clear instructions for turning on auto-update, so that I receive fixes without doing anything.
10. As a team member, I want a command to update manually, so that I can get a fix right away when I need it.
11. As a team member, I want to uninstall a skill cleanly, so that unused skills don't take up context.
12. As a team member, I want error messages in Thai that say what to do next, so that I can fix problems without asking a maintainer.
13. As a team member, I want running the installer again to be safe (idempotent), so that a mistake doesn't break anything.
14. As a team member, I want to verify after installing that the skill loaded (it shows up under `/`), so that I know it is ready to use.

### ผู้ใช้ `ding`

15. As a ding user, I want the installer to create a `.env` template for me in a fixed location outside the repo, so that I know exactly where to put my token.
16. As a ding user, I want to fill in the token myself in an editor rather than typing it in chat, so that it never enters the conversation log.
17. As a ding user, I want installation to stop with a clear message if `SECRET_AUTH` is missing or still the placeholder, so that I don't end up with a skill that fails on first use.
18. As a ding user, I want the `.env` file permissions set so that only I can read it, so that other users on the same machine can't see the token.
19. As a ding user, I want my saved channel list to survive plugin updates and reinstalls, so that I don't lose my room nicknames.
20. As a ding user, I want my channel list to stay on my own machine and never go into the repo, so that internal channel UUIDs aren't published.
21. As a ding user, I want ding to work on Windows without installing extra Python packages, so that setup stays simple.
22. As a ding user, I want `--dry-run` to show the final message without needing a token, so that I can check before sending for real.
23. As a ding user, I want an error that names the expected `.env` path when the token can't be read, so that I know which file to fix.
24. As a ding user, I want the token never printed to stdout or in errors, so that it can't leak through logs or screenshots.
25. As a ding user, I want all the existing safety rules kept (always ask which room, confirm the hashtag, reject ambiguous tags), so that moving the skill into the repo doesn't make it less safe.

### Contributor (ผู้เพิ่ม skill)

26. As a contributor, I want a correct plugin template to copy, so that a new skill loads the first time.
27. As a contributor, I want one command that runs every check locally, so that I know my change passes before I open a PR.
28. As a contributor, I want the check to fail if INDEX.md and the marketplace list don't match, so that the catalog never drifts.
29. As a contributor, I want the check to fail if I commit a secret, a personal home path, or an internal UUID, so that the public repo stays clean.
30. As a contributor, I want CLAUDE.md to state the repo's purpose and coding rules, so that Claude and people follow the same standard.
31. As a contributor, I want the version to live in one place per plugin, so that I bump it once per release.
32. As a contributor, I want CI to run the same check on every PR, so that review doesn't depend on someone remembering to test.
33. As a contributor, I want the PR template to ask "did you run the test command?", so that the rule is visible at review time.

### Maintainer

34. As a maintainer, I want each skill to be its own plugin, so that people install only what they use and each skill has its own version.
35. As a maintainer, I want marketplace.json to be the single list of available plugins, so that the installer, INDEX check, and `/plugin` all read the same list.
36. As a maintainer, I want `create-guide` to be a single skill that takes a language argument, so that I maintain one file instead of three copies.
37. As a maintainer, I want large skills split into a short SKILL.md plus reference files loaded on demand, so that calling a skill doesn't use more context than needed.
38. As a maintainer, I want outdated install docs removed, so that no one follows instructions that no longer work.
39. As a maintainer, I want the external skills catalog (dotnet-skills) kept as-is, so that the rule against copying other teams' files still holds.

### ผู้อ่าน README

40. As a first-time visitor, I want the first screen of the README to say what this repo is and who it's for, so that I know in a few seconds whether it's relevant to me.
41. As a first-time visitor, I want a quick start of 3–4 commands at the top, so that I can install without reading the whole page.
42. As a non-Thai reader, I want a complete English README linked from the top of the Thai one, so that I can use the repo without translating it.
43. As a Thai reader, I want the Thai README as the default page, so that most of the team reads it in their own language.
44. As a team member, I want every skill listed with what it does, when to use it, an example of what to type, whether it needs setup, and its requirements, so that I can choose before installing.
45. As a team member, I want step-by-step install instructions for both paths (`/install-skills` and `/plugin`), with what I should see at each step, so that I can tell I'm on the right track.
46. As a team member, I want a prerequisites section (Claude Code version, git, Python, OS), so that I can check my machine before I start.
47. As a ding user, I want the README to show where `ding.env` lives on each OS and what it should contain, so that I can fill it correctly the first time.
48. As a team member, I want sections for updating, auto-update, and uninstalling, so that I can manage skills after installing.
49. As a team member, I want a troubleshooting section listing common symptoms and how to fix them, so that I don't need to ask anyone.
50. As a team member, I want to know how to move from the old symlink setup to plugins, so that the same skill doesn't load twice.
51. As a security-minded reader, I want a security section saying what is stored where, what never goes into the repo, and how to report a leak, so that I can trust the repo.
52. As a contributor, I want a short "add a skill" section that links to the full guide in CLAUDE.md, so that README doesn't become a second copy of the rules.
53. As a maintainer, I want the test to fail if the skill list in either README doesn't match marketplace.json, so that the README never shows a skill that doesn't exist.

## Implementation Decisions

### โครงสร้าง marketplace

- root ของ repo เป็น marketplace ชื่อ `pi-claude-md` (ไม่ใช้ prefix `claude-`/`anthropic-` เพราะเป็นชื่อที่ถูกสงวนไว้)
- 1 skill = 1 plugin มี manifest ของตัวเอง marketplace entry ใช้ relative source
- plugin ชุดแรกมี 3 ตัว: `tyc-design-system`, `create-guide`, `ding`
- `example-skill` และ `example-plugin` ไม่อยู่ใน marketplace รวมเป็น template เดียวที่มีโครงสร้าง plugin ถูกต้อง
- skill ใน plugin จะถูก namespace เป็น `<plugin>:<skill>` เรายอมรับข้อนี้ ส่วน `name` ใน frontmatter ยังต้องเป็น kebab-case และตรงกับชื่อโฟลเดอร์
- **ที่เก็บ version:** ใส่ `version` ใน plugin manifest เท่านั้น แล้วเอา `version` ออกจาก `metadata` ใน SKILL.md (field อื่นใน `metadata` เช่น author, tags, status ยังเก็บไว้) ถ้าไม่ใส่ version ไว้ Claude Code จะใช้ commit SHA แทน และผู้ใช้จะได้อัปเดตทุก commit

### Installer (`/install-skills`)

- ชื่อคำสั่งเป็น `/install-skills` (ไม่ใช่ `/install`) เพื่อไม่ให้ชนหรือสับสนกับคำสั่งติดตั้งของ Claude Code เอง

- เป็น **project skill** อยู่ใน repo และใช้ได้เฉพาะตอนเปิด Claude Code ที่ root ของ repo ไม่อยู่ใน marketplace
- เหตุผล: `/plugin` ติดตั้งได้ทีละตัวและไม่มี multi-select เราจึงต้องทำ checklist เอง และวิธีนี้ทำงานบนทุก OS เพราะเรียกแค่ `claude plugin ...`
- ขั้นตอน:
  1. อ่านรายการ plugin จาก marketplace.json
  2. อ่านรายการที่ติดตั้งแล้วจาก `claude plugin list`
  3. ให้ผู้ใช้ติ๊กเลือกหลายตัวด้วย AskUserQuestion แบบ multiSelect (มี description ของแต่ละตัว และตัวที่ติดตั้งแล้วมีป้ายบอก)
  4. ถ้ายังไม่มี marketplace ในเครื่อง ให้ add จาก repo นี้
  5. ทำ pre-install hook ของ plugin ที่ต้องตั้งค่าก่อน (ตอนนี้มีแค่ `ding`)
  6. รัน `claude plugin install <name>@pi-claude-md --scope user` ทีละตัว
  7. สรุปผลเป็นตาราง ติดตั้งแล้ว / ข้าม / ล้มเหลว (พร้อมสาเหตุ)
- ตัวที่ล้มเหลวไม่ทำให้ตัวอื่นหยุด รันซ้ำได้ปลอดภัย
- ส่วนที่ต้องตรวจแบบแน่นอน (อ่าน marketplace, ตรวจ `.env`) อยู่ใน Python script ที่ใช้แค่ stdlib แล้ว skill เป็นตัวเรียก ส่วน skill ทำหน้าที่ถามผู้ใช้และสรุปผล

### `ding` และ `.env`

- **ที่เก็บค่า config:** `~/.config/pi-claude-md/` (หาจาก home ของผู้ใช้ ใช้ได้ทุก OS) มี 2 ไฟล์:
  - `ding.env` เก็บ `SECRET_AUTH`
  - `ding-channels.json` เก็บรายชื่อห้องที่เคยส่ง
- **ทำไมไม่ใช้ `userConfig` ของ plugin:** ค่าที่ตั้ง `sensitive` ไปไม่ถึง script ที่ Claude รันผ่าน Bash tool (ตามเอกสาร plugin ของ Claude Code)
- **ทำไมไม่ใช้ `${CLAUDE_PLUGIN_DATA}`:** โฟลเดอร์นี้ถูกลบเมื่อ uninstall และ path ขึ้นกับ id ภายในของ Claude Code
- **ขั้นตอน pre-install ของ ding:**
  1. ถ้ายังไม่มี `ding.env` ให้สร้างจาก template โดยใส่ค่า placeholder และตั้ง permission 600 (บน POSIX)
  2. บอก path ให้ผู้ใช้ไปกรอกเองใน editor แล้วตอบกลับว่าเสร็จ
  3. ตรวจว่ามี `SECRET_AUTH` ที่ไม่ว่างและไม่ใช่ placeholder **โดยไม่อ่านค่าออกมาแสดง** script บอกแค่ ok หรือเหตุผลที่ไม่ผ่าน
  4. ถ้าไม่ผ่าน จะไม่ติดตั้ง ding และขึ้นสถานะ "ข้าม — ยังไม่ได้กรอก .env" ในสรุป
- **สิ่งที่เปลี่ยนใน send.py:**
  - ลบ path ส่วนตัวที่ hardcode ไว้ แล้วอ่านจาก path config ข้างบน
  - ข้อความ error บอก path ที่คาดไว้ แต่ไม่บอกค่าในไฟล์
  - เวลาไทยใช้ fixed offset UTC+7 แทน `zoneinfo` เพราะ Windows ไม่มี tz database ถ้าไม่ลง `tzdata`
- **สิ่งที่เปลี่ยนใน SKILL.md:** อ้าง script ผ่าน `${CLAUDE_PLUGIN_ROOT}` และอ้างที่เก็บ channel ผ่าน path config แทนโฟลเดอร์ skill
- **ไม่ย้ายเข้า repo:** `channels.json` เดิม (มี UUID จริง) และ `__pycache__`
- พฤติกรรมความปลอดภัยเดิมของ ding ต้องเหมือนเดิมทุกข้อ (ถามห้องทุกครั้ง, ยืนยัน hashtag, ตรวจ tag, ไม่ retry เมื่อได้ 401, กฎ red flags)

### `create-guide`

- รวมเป็น skill เดียวที่มี `SKILL.md` ถูกต้อง รับภาษา (`th` เป็นค่าเริ่มต้น หรือ `en`) เป็น argument
- ลบไฟล์ที่ซ้ำ
- แยกเนื้อหายาว เช่น template HTML, ขั้นตอน capture ด้วย Playwright, การจัดการ auth ไปไว้ในไฟล์ reference ที่อ่านเฉพาะตอนต้องใช้ ให้ SKILL.md เหลือแค่ขั้นตอนหลัก
- ลบ `install-guide` เพราะ installer ใหม่มาแทน

### `tyc-design-system`

- ย้ายเข้าโครงสร้าง plugin เนื้อหาเดิมไม่เปลี่ยน
- เพิ่ม `metadata` ใน frontmatter ให้ครบตามกติกา

### INDEX.md

- ตาราง plugin: ชื่อ / คำอธิบาย / tags / คำสั่งติดตั้ง / ต้องตั้งค่าก่อนไหม (ding = ต้องกรอก `.env`)
- ตาราง tag
- ตาราง external skills คงไว้
- ส่วนเริ่มต้นใช้งาน 2 ทาง (`/install-skills` หรือ `/plugin`) และวิธีเปิด auto-update
- **เอาตัวเลขสถิติที่ต้องนับมือออก** เพราะเป็นต้นเหตุที่ข้อมูลไม่ตรงกับของจริง และ test ตรวจตัวเลขพวกนี้ไม่ได้
- test ตรวจว่า plugin ทุกตัวใน marketplace.json มีแถวใน INDEX.md และไม่มีแถวของ plugin ที่ไม่มีอยู่จริง

### README (ไทย + อังกฤษ)

- **ไฟล์และภาษา:** README หลักเป็นภาษาไทย (หน้าแรกบน GitHub) และมี README ภาษาอังกฤษเป็นอีกไฟล์ ทั้งสองไฟล์มีลิงก์สลับภาษาไว้บรรทัดบนสุด
  - แยกไฟล์เพื่อไม่ให้หน้าเดียวยาวสองเท่า และให้คนอ่านจบในภาษาเดียว
  - ทั้งสองไฟล์ต้องมีหัวข้อเหมือนกันและเรียงลำดับเดียวกัน
- **บทบาทของแต่ละไฟล์ (ไม่ให้เนื้อหาซ้ำกัน):**
  - README: สำหรับคนติดตั้งและคนใช้
  - INDEX.md: ค้นหาตาม tag
  - CLAUDE.md: กติกาสำหรับคนที่เขียนโค้ดเข้า repo
  - README ลิงก์ไป 2 ไฟล์นี้ ไม่ copy เนื้อหามา
- **หัวข้อตามลำดับ:**
  1. ชื่อ + จุดประสงค์ 1–2 ประโยค: skills กลางของทีม PI ติดตั้งง่าย เลือกได้ทีละตัว อัปเดตได้
  2. Quick start: คำสั่งที่น้อยที่สุดของทั้งสองทาง
  3. รายการ skill: แต่ละตัวบอก
     - ชื่อ
     - ทำอะไร
     - ใช้เมื่อไหร่
     - ตัวอย่างคำที่พิมพ์เพื่อเรียกใช้
     - ต้องตั้งค่าก่อนไหม
     - requirement เพิ่มเติม (เช่น ding ต้องมี Python 3.9+ และต้องเชื่อมต่อ `dingtalk.tycthailand.com` ได้)
  4. Prerequisites: Claude Code (ระบุเวอร์ชันขั้นต่ำที่ใช้คำสั่ง `claude plugin install` ได้), git, Python 3.9+ (เฉพาะ skill ที่มี script) และ OS ที่รองรับ
  5. วิธีติดตั้งแบบละเอียด:
     - ทาง A `/install-skills` (แนะนำ): clone → เปิด Claude Code ที่ root ของ repo → `/install-skills` → ติ๊กเลือก → (ถ้าเลือก ding) กรอก `.env` → ดูตารางสรุป
     - ทาง B `/plugin`: add marketplace → แท็บ Discover → เลือก → เลือก scope และคำสั่ง CLI แบบไม่ต้องตอบคำถาม (`claude plugin install <name>@pi-claude-md`)
     - ทุกขั้นบอกว่าควรเห็นอะไร
  6. ตั้งค่า ding:
     - path ของ `ding.env` บน Linux/macOS และ Windows
     - ตัวอย่างไฟล์ที่ใส่ค่า placeholder
     - วิธีขอ token จากผู้ดูแลระบบ
     - ห้ามวาง token ในแชทของ Claude
  7. ตรวจว่าติดตั้งสำเร็จ: พิมพ์ `/` แล้วต้องเห็นชื่อ skill แบบมี namespace (`<plugin>:<skill>`)
  8. อัปเดต: เปิด auto-update ใน `/plugin` → Marketplaces, อัปเดตเองด้วยคำสั่ง update และต้อง `/reload-plugins` หรือเปิด session ใหม่ถึงจะได้เวอร์ชันใหม่
  9. ถอนการติดตั้ง: คำสั่ง uninstall และบอกว่าไฟล์ใน `~/.config/pi-claude-md/` ไม่ถูกลบ ถ้าต้องการให้ลบเอง
  10. ย้ายจาก symlink เดิม: ลบ symlink ใน `~/.claude/skills/` ของ skill ที่ย้ายมาเป็น plugin แล้ว เพื่อไม่ให้มีสองชุด
  11. Troubleshooting (ตาราง อาการ → สาเหตุ → วิธีแก้):
      - พิมพ์ `/` แล้วไม่เห็น skill
      - ding ถูกข้ามเพราะยังไม่ได้กรอก `.env`
      - ding ได้ 401
      - `claude: command not found`
      - ติดตั้งแล้วยังได้เวอร์ชันเก่า
      - skill ขึ้นซ้ำสองชุด (มี symlink เดิมค้างอยู่)
  12. Security:
      - secret อยู่ที่ไหน
      - repo นี้ public ห้าม commit อะไรบ้าง
      - ไฟล์ที่ ding อัปโหลดเป็น public URL อายุ 7 วัน
      - ถ้าเผลอ commit secret: rotate token ทันทีและแจ้งเจ้าของ repo
  13. Skills จากภายนอก: dotnet-skills พร้อมลิงก์ไป catalog เดิม
  14. Contributing: 4 ขั้น (copy template → แก้ → เพิ่มใน marketplace.json/INDEX/README ทั้งสองภาษา → รัน test command) แล้วลิงก์ไปกติกาเต็มใน CLAUDE.md
  15. โครงสร้าง repo: ตารางสั้น ๆ ว่าโฟลเดอร์ไหนเก็บอะไร
  16. License: บอกว่ายังไม่มี LICENSE ตามกฎหมายจึงยังไม่อนุญาตให้นำไปใช้ซ้ำ จนกว่าเจ้าของจะเพิ่ม
- **ข้อกำหนดเรื่องรูปแบบ:**
  - คำสั่งทุกคำสั่งอยู่ใน code block ให้ copy ได้
  - คำสั่งที่ต่างกันตาม OS ให้แยกบล็อก
  - ใช้ emoji หัวข้อให้น้อยลงจากของเดิม
  - ไม่ใส่ข้อความโฆษณา
  - ทุกตัวอย่างใช้ placeholder ไม่ใช้ค่าจริง

### CLAUDE.md (ของ repo)

- **จุดประสงค์:** repo นี้คือ skills กลางที่ติดตั้งง่าย ทุกการเปลี่ยนแปลงต้องทำให้การติดตั้งหรือการใช้งานง่ายขึ้น หรืออย่างน้อยไม่ยากขึ้น
- **กติกาโค้ด:**
  - ไม่เขียน comment
  - โค้ดกระชับตามหลัก software engineering: ชื่อสื่อความหมาย, function เล็ก, ไม่มี abstraction ที่ไม่จำเป็น
  - ทุกครั้งต้องรัน test command และต้องผ่าน ก่อนรายงานว่าเสร็จหรือสำเร็จ ถ้าไม่ผ่านต้องแสดง output
  - ทุกการเปลี่ยนแปลงต้องคิดถึง user friendly (ภาษาไทย, ข้อความ error บอกทางแก้), performance (SKILL.md สั้น เนื้อหายาวไว้ใน reference) และ security (ไม่มี secret, path ส่วนตัว หรือ UUID ภายในใน repo public, ไม่ให้ token ผ่านแชท)
  - ใส่หลัก Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution / Design and UX Standards ไว้ในไฟล์เลย เพื่อให้ทีมได้หลักเดียวกันโดยไม่ต้องพึ่ง global CLAUDE.md ของใคร
- **อัปเดตส่วนที่ล้าสมัย:** วิธีติดตั้ง (marketplace แทน symlink), โครงสร้างโฟลเดอร์, วิธีเพิ่ม skill (copy template → เพิ่ม entry ใน marketplace.json → เพิ่มแถว INDEX → รัน test), ตาราง tags (เพิ่ม `notification`, `design-system`)
- **ไม่พึ่ง comment:** ข้อจำกัดที่ไม่ชัดในโค้ด (เช่น เพดาน 49MB เพราะ nginx) ให้สื่อผ่านชื่อค่าคงที่ หรือเขียนไว้ใน SKILL.md แทน

### อื่น ๆ

- `.gitignore` เพิ่ม `__pycache__/`, `*.env`, `.env`
- ลบ `.directory` ออกจาก repo
- PR template เพิ่มช่องให้ติ๊กว่ารัน test command แล้ว และช่องให้ติ๊กว่าอัปเดต README ทั้งสองภาษาแล้ว
- README ย่อยที่สอนโครงสร้างเก่า (ของ skills และ plugins) ให้รวมเป็นคู่มือใน template ตัวเดียว แล้วลบตัวเก่า เพื่อไม่ให้มีเอกสารสอนวิธีที่ใช้ไม่ได้แล้ว

## Testing Decisions

**test ที่ดีตรวจพฤติกรรมที่ผู้ใช้เห็น ไม่ตรวจรายละเอียดข้างใน** เช่น ตรวจว่า plugin ติดตั้งได้และ skill โหลดได้ ไม่ใช่ตรวจว่า JSON มี key ลำดับไหน

**Seams (ใช้ให้น้อยที่สุด อยู่ระดับสูงที่สุด):**

1. **Test command เดียวที่ root (seam หลัก)** ทั้ง contributor และ CI เรียกตัวนี้ ข้างในทำ:
   - **Validate:** `claude plugin validate . --strict` ตรวจ marketplace และ plugin ทุกตัวด้วย validator ของ Claude Code เอง
   - **ติดตั้งจริงแบบแยก environment:** ตั้ง Claude config dir ไปที่ temp แล้ว add marketplace จาก local path และติดตั้ง plugin ทุกตัวที่ไม่ต้องตั้งค่าก่อน จากนั้นตรวจว่า `claude plugin list` เห็นทุกตัว ส่วน ding ทดสอบผ่าน installer script โดยใช้ `.env` ปลอม
   - **Catalog sync:** marketplace.json ↔ INDEX.md ↔ README ทั้งสองภาษา ↔ โฟลเดอร์ plugin ต้องตรงกัน และ `name` ใน frontmatter ต้องตรงกับชื่อโฟลเดอร์
   - **README parity + links:** README ไทยและอังกฤษมีหัวข้อระดับ `##` จำนวนเท่ากัน และลิงก์ภายใน repo ทุกลิงก์ใน README, INDEX.md และ CLAUDE.md ชี้ไปไฟล์ที่มีอยู่จริง
   - **Secret/privacy scan:** ไฟล์ที่ track ใน git ต้องไม่มี path `/home/<user>`, UUID ที่ไม่ใช่ placeholder, ค่า `SECRET_AUTH=` ที่ไม่ใช่ placeholder หรือ IP ภายใน
2. **CLI ของ `send.py` และ installer script** (seam เดิมที่มีอยู่แล้ว) รันเป็น subprocess โดยตั้ง `HOME` เป็น temp dir:
   - ไม่มี `ding.env` → exit ≠ 0 และข้อความมี path ที่คาดไว้
   - `SECRET_AUTH` เป็น placeholder หรือว่าง → ตรวจไม่ผ่าน
   - token ถูกต้อง → ตรวจผ่าน และค่า token ไม่โผล่ใน stdout/stderr
   - `--dry-run` ใช้ได้โดยไม่ต้องมี token และไม่ยิง network
   - `--tags` ที่กำกวมถูกปฏิเสธเหมือนพฤติกรรมเดิม
   - ไฟล์ `.env` ที่ installer สร้างมี permission 600 (เฉพาะ POSIX)

**ใช้อะไรรัน:** Python stdlib (`unittest`) กับ shell script ตัวเดียว ไม่เพิ่ม dependency

**Prior art:** ใน repo ยังไม่มี test ตัวไหน `send.py` มี `--dry-run` อยู่แล้ว ซึ่งเป็น seam ที่ทดสอบได้โดยไม่ต้องยิง network

**การ test ด้วยมือก่อนปิดงาน (ทำครั้งเดียว):** ทำตาม Quick start ใน README ทีละบรรทัดบนเครื่องผู้ขอ (เพื่อพิสูจน์ว่าเอกสารใช้ได้จริง ไม่ใช่แค่โค้ดใช้ได้) เลือกครบ 3 ตัว แล้วตรวจว่าทั้ง 3 ตัวขึ้นใน `/` และ `/ding` dry-run ผ่าน

## Out of Scope

- ย้าย `restore-local-db` และ `csharp-db-pull` เข้า repo (`restore-local-db` มี IP/NAS ภายใน ต้องคิดเรื่องความปลอดภัยแยกต่างหาก)
- copy หรือแก้ external skills (dotnet-skills)
- แก้เนื้อหาหรือ design token ของ `tyc-design-system`
- แก้ logic การสร้างคู่มือของ `create-guide` (เปลี่ยนแค่โครงสร้างไฟล์และการรับ argument ภาษา)
- เพิ่ม LICENSE (เป็นการตัดสินใจทางกฎหมายของเจ้าของ repo ควรทำแยก)
- `docs/skills-manual.html` ที่ยังไม่ได้ commit
- ส่ง plugin เข้า marketplace ทางการของ Anthropic

## Further Notes

- **ยังไม่ได้ยืนยัน:**
  - การ add marketplace ด้วย local path ใน temp config dir ทำได้จริงหรือไม่ และจะใช้ env var อะไรแยก config ต้องลองตอนเริ่ม implement ถ้าไม่ได้ ให้ seam 1 เหลือแค่ validate กับ catalog sync
  - CI ต้องติดตั้ง Claude Code CLI ก่อน ยังไม่ได้ยืนยันว่า `claude plugin validate` รันได้โดยไม่ login
  - API ของ dingtalk-notify ไม่มี endpoint ให้ตรวจ token โดยไม่ส่งข้อความจริง installer จึงตรวจได้แค่รูปแบบ ถ้าผู้ใช้ใส่ token ผิด จะรู้ตอนส่งครั้งแรก (401) ซึ่ง SKILL.md มีวิธีแก้เขียนไว้แล้ว
- **ข้อกำหนด plugin ที่อ้างอิง (code.claude.com/docs/en/plugins):**
  - `userConfig.sensitive` ไปไม่ถึง Bash-run script
  - `${CLAUDE_PLUGIN_DATA}` ถูกลบเมื่อ uninstall
  - `/plugin` ติดตั้งได้ทีละตัว
  - auto-update ของ marketplace ภายนอกปิดเป็นค่าเริ่มต้น
- **ข้อมูล public:** `ding` จะทำให้ URL `dingtalk.tycthailand.com` อยู่ใน repo public ส่วน `tyc-design-system` มีชื่อระบบภายในอยู่แล้ว ผู้ขอเลือกให้ repo เป็น public แล้ว แต่ไม่มี token และ channel UUID ขึ้น repo
- issue tracker ของ to-spec ยังไม่ได้ตั้งค่า (`/setup-matt-pocock-skills`) จึงยังไม่ได้เปิด issue บน GitHub เก็บ spec นี้ไว้ใน repo ก่อน
