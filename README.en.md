[ภาษาไทย](./README.md) · **English**

# PI Claude Md

Shared skills of the PI team for [Claude Code](https://code.claude.com). Install only the ones you need, get the same version on every machine, and update them from one place.

## Quick start

**Option A — pick several at once (recommended)**

```bash
git clone https://github.com/ken1lnw/pi-claude-md.git
cd pi-claude-md
claude
```

Then type in Claude Code:

```
/install-skills
```

**Option B — install one at a time, no clone needed**

```
/plugin marketplace add ken1lnw/pi-claude-md
/plugin install tyc-design-system@pi-claude-md
```

## Available skills

| Plugin | What it does | Setup needed |
|---|---|---|
| [tyc-design-system](./plugins/tyc-design-system/skills/tyc-design-system/SKILL.md) | Applies TYC's shared design system to UI work | No |
| [create-guide](./plugins/create-guide/skills/create-guide/SKILL.md) | Builds a single-file HTML user guide | No |
| [ding](./plugins/ding/skills/ding/SKILL.md) | Sends notifications to a DingTalk group | Fill in `ding.env` |

### tyc-design-system

- **What it does:** Keeps every internal system on the same colors, buttons, tables, cards, radius/spacing scale and dark/light mode. Values are read from the real design tokens, never guessed.
- **Use it when:** building a new page, restyling an existing system, reviewing UI, or asking about the TYC theme / brand guideline.
- **Examples:** `Make the wms login page match the TYC theme` · `Reskin the receiving module to match the design system`
- **Modes:** `full` (whole system) · `partial` (named modules) · `extend` (add a new pattern to the design system)

### create-guide

- **What it does:** Builds a user guide for a module as one HTML file (images embedded as base64, ready to share) from CLAUDE.md, source code, routes and screenshots.
- **Use it when:** you need end-user documentation, or need to refresh a guide after screens changed.
- **Examples:** `/create-guide:create-guide basket-circulation` · `/create-guide:create-guide receiving th+en --capture`
- **Languages:** `th` (default) · `en` · `th+en` (with a language toggle)
- **Extra requirements (`--capture` only):** Node.js + Playwright, and a test account for the target system.

### ding

- **What it does:** Sends a markdown message, with optional images or files, to a DingTalk group through TYCTH's dingtalk-notify.
- **Use it when:** announcing a deploy, sharing a report, or notifying the team.
- **Examples:** `/ding:ding tell the team the wms deploy is done` · `send this screenshot to the DingTalk group`
- **Safety:** it asks for the target room every time and asks you to confirm the message before sending.
- **Extra requirements:** Python 3.9+, a dingtalk-notify token, and network access to `dingtalk.tycthailand.com`.

## Requirements

| What | Needed for | Check with |
|---|---|---|
| Claude Code (tested with 2.1.296) | every skill | `claude --version` |
| git | Option A | `git --version` |
| Python 3.9+ | `/install-skills` and ding | `python3 --version` (Windows: `python --version`) |

Works on Linux, macOS and Windows.

## Installation in detail

### Option A — `/install-skills` (multi-select)

1. Clone the repo and start Claude Code **at the repo root**:

   ```bash
   git clone https://github.com/ken1lnw/pi-claude-md.git
   cd pi-claude-md
   claude
   ```

2. Type `/install-skills`. You'll see the plugins that aren't installed yet, each with a description.
3. Tick the ones you want. You can pick more than one.
4. If you picked **ding**, Claude creates `ding.env` and tells you where it is. Open the file in an editor, add your token (see [Set up ding](#set-up-ding)), then tell Claude you're done.
5. Claude installs the plugins and shows a table of `installed` / `skipped` / `failed`, with reasons.
6. Run `/reload-plugins` or start a new session.

You can run `/install-skills` again at any time. Plugins that are already installed are skipped.

### Option B — `/plugin` (one at a time)

1. Add the marketplace (once per machine):

   ```
   /plugin marketplace add ken1lnw/pi-claude-md
   ```

2. Type `/plugin`, go to the **Discover** tab, pick a plugin, choose **Install**, then pick the **user** scope (available in every project).
3. For **ding**, finish [Set up ding](#set-up-ding) before using it.

From a terminal, with no prompts:

```bash
claude plugin marketplace add ken1lnw/pi-claude-md
claude plugin install tyc-design-system@pi-claude-md --scope user
claude plugin install create-guide@pi-claude-md --scope user
claude plugin install ding@pi-claude-md --scope user
```

## Set up ding

ding only reads its token from a file on your machine. That file is never part of the repo.

| OS | File |
|---|---|
| Linux / macOS | `~/.config/pi-claude-md/ding.env` |
| Windows | `%USERPROFILE%\.config\pi-claude-md\ding.env` |

1. `/install-skills` creates the file for you. To create it yourself (use `python` instead of `python3` on Windows):

   ```bash
   python3 plugins/ding/skills/ding/send.py --init-env
   ```

2. Open the file in an editor and replace `paste-token-here` with your real token:

   ```
   SECRET_AUTH=paste-token-here
   ```

3. Check the file (the token is never printed):

   ```bash
   python3 plugins/ding/skills/ding/send.py --check-env
   ```

Ask TYCTH's dingtalk-notify administrator for a token.
**Never paste the token into the Claude chat.** If you already did, ask for a new token.

## Verify the installation

Type `/` in Claude Code. You should see names in the form `<plugin>:<skill>`, such as `tyc-design-system:tyc-design-system`, `create-guide:create-guide` and `ding:ding`.

Or run this in a terminal:

```bash
claude plugin list
```

## Updating

- **Automatic (recommended):** `/plugin` → **Marketplaces** tab → `pi-claude-md` → **Enable auto-update**. Auto-update is off by default for third-party marketplaces.
- **Manual:**

  ```bash
  claude plugin marketplace update pi-claude-md
  claude plugin update ding@pi-claude-md
  ```

Sessions that are already open keep the old version until you run `/reload-plugins` or start a new session.

## Uninstalling

```bash
claude plugin uninstall ding@pi-claude-md
```

Files in `~/.config/pi-claude-md/` (ding's token and room list) are **not** deleted. Remove them yourself if you no longer need them.

## Migrating from the old symlink setup

If you symlinked skills into `~/.claude/skills/` the old way, remove the links for anything you now install as a plugin. Otherwise the skill shows up twice.

```bash
rm ~/.claude/skills/tyc-design-system ~/.claude/skills/create-guide
```

Don't add a trailing `/` and don't use `-r`. `rm -r name/` deletes the original files in the repo too.

If you used the old ding (a folder at `~/.claude/skills/ding/`):

1. Move `SECRET_AUTH` into `ding.env` as described in [Set up ding](#set-up-ding).
2. Move the room list `~/.claude/skills/ding/channels.json` to `~/.config/pi-claude-md/ding-channels.json`.
3. Delete the old `~/.claude/skills/ding/` folder.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Skill not listed under `/` | The session hasn't loaded the new plugin | `/reload-plugins` or start a new session |
| `/install-skills` not listed | Claude Code wasn't started at the repo root | `cd pi-claude-md` and run `claude` again |
| ding shows "ข้าม — ยังไม่ได้ตั้งค่า" (skipped, not set up) | `ding.env` is missing or still contains `paste-token-here` | Do [Set up ding](#set-up-ding), then run `/install-skills` again |
| ding returns `FAILED 401` | Wrong token, or stray spaces/newlines | Make `ding.env` a single line: `SECRET_AUTH=<token>` |
| `claude: command not found` | Claude Code isn't installed or isn't on PATH | Install it from [code.claude.com/docs/en/setup](https://code.claude.com/docs/en/setup) |
| `python3: command not found` (Windows) | Windows names it `python` | Use `python` instead of `python3` |
| Still on the old version after updating | The open session keeps the old version | `/reload-plugins` |
| Skill listed twice | An old symlink is still there | See [Migrating from the old symlink setup](#migrating-from-the-old-symlink-setup) |

## Security

- **Where secrets live:** only in `~/.config/pi-claude-md/` on your machine. The file is readable by you only (`600`).
- **Never commit (this repo is public):** tokens, passwords, real channel UUIDs, internal IPs or personal paths. `bash tests/run.sh` scans for these, and CI fails if it finds any.
- **Files sent with ding get a public URL that lasts 7 days.** Don't attach screenshots or files that contain secrets.
- **If you commit a secret by mistake:** get a new token right away (treat the old one as leaked, even after the commit is removed) and tell the repo owner.

## External skills

Install the .NET / Akka / Aspire set (35 skills) straight from its owner's marketplace:

```
/plugin marketplace add Aaronontheweb/dotnet-skills
```

Details: [`docs/external-skills.md`](./docs/external-skills.md)

## Adding a skill

1. Run `cp -r templates/plugin-template plugins/<name>` and rename the skill folder.
2. Write `SKILL.md` and `plugin.json`.
3. Add an entry to `.claude-plugin/marketplace.json`, and add a row to the tables in `README.md`, `README.en.md` and `INDEX.md`.
4. Make `bash tests/run.sh` pass, then open a pull request.

Full rules (no code comments, test before claiming done, security): [CLAUDE.md](./CLAUDE.md)

## Repository layout

| Path | Contents |
|---|---|
| `.claude-plugin/marketplace.json` | List of all plugins |
| `plugins/<name>/` | One plugin (manifest + skill) |
| `.claude/skills/install-skills/` | `/install-skills` |
| `scripts/install.py` | Script that `/install-skills` runs |
| `templates/plugin-template/` | Template for a new plugin |
| `tests/` | Test suite (`bash tests/run.sh`) |
| `docs/` | Other documents |
| [`INDEX.md`](./INDEX.md) | Search by tag |

## License

This repo has no LICENSE file yet. Until the owner adds one, the default legal position is that the code may not be reused outside the team.
