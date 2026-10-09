# Installation

These instructions target the complete **0.3.0** bundle, including the local camera and its direct image workflow. Use the complete supplied kit; its manifest and checksums identify the exact delivery. Artifact paths in this guide are relative to that kit.

The [public v0.1.1 release](https://github.com/Stunspot/omniview-looking-glass/releases/tag/v0.1.1) remains a historical portable-skill handoff. It does not include the current camera. Do not mix its files into a0.3.0 installation. See [Package reference](PACKAGE-REFERENCE.md) for the current topology.

## Open the local camera

Keep the complete `codex/omniview-looking-glass/` folder intact. Its `workspace` directory contains `Open.cmd` for Windows, `Open.command` for macOS and `host.py` for Linux. Install Python3.10 or newer; no extra packages are required. Windows users open `Open.cmd`; macOS users first run `chmod +x Open.command` in that directory, then open it; Linux users run `python3 host.py` there. macOS execution has not been observed in this project's evidence.

The launcher opens or reconnects the exact local camera. Start with Place and Time. With `OPENAI_API_KEY` configured in the launching environment, **Create image** requests one OpenAI image and may incur a charge; the quick path does no historical source research. **Plan with my agent instead** needs no provider request. Read the included `OPEN-WORKSPACE.md` or `codex/omniview-looking-glass/workspace/README.md` for configuration, source-grounded handoff and saved work.

## Before you install

1. Choose one host artifact.
2. Confirm that the skill folder contains `SKILL.md` directly.
3. Compare the artifact against `SHA256SUMS.txt` in the assembled kit.
4. Preserve any existing skill with the same name before replacing it.

On Windows PowerShell, inspect a file hash with:

    Get-FileHash -Algorithm SHA256 -LiteralPath path\to\file

The GL4SS drop-in patches are a separate maintainer handoff. Do not install them as an agent skill.

## Install for Codex

Artifact:

    codex/omniview-looking-glass/

Codex local skills live under:

    $CODEX_HOME/skills/

When `CODEX_HOME` is not customized, the default is:

    ~/.codex/skills/

Place the complete `omniview-looking-glass` directory there. The resulting topology is:

    $CODEX_HOME/
      skills/
        omniview-looking-glass/
          SKILL.md
          NOTICE.md
          LICENSE.md
          package-manifest.yaml
          agents/
          assets/
          evals/
          references/
          workspace/

Start a new Codex task. Restart the host if it does not refresh skill discovery automatically.

### Check Codex discovery

Ask:

> Use omniview-looking-glass to open a prompt-only view onto Uruk around 3200 BC at first light.

A useful discovery check must demonstrate that the installed skill was selected. A plausible historical answer by itself is not discovery evidence.

This release has no qualified Codex selection receipt yet. Treat discovery as awaiting fresh-host qualification unless the host exposes an observable selection record.

The package includes Codex-facing metadata that permits implicit selection. Qualify explicit selection before testing implicit selection.

## Install for Claude

Artifact:

    claude/omniview-looking-glass.zip

The ZIP contains exactly one top-level `omniview-looking-glass` folder with `SKILL.md` directly beneath it.

### Claude skill upload

Anthropic's current skill-upload flow requires Code execution and file creation:

1. Open **Customize > Skills**.
2. Select **+**, then **Create skill**.
3. Select **Upload a skill**.
4. Choose `omniview-looking-glass.zip`.
5. Confirm that OmniView appears in the skill list and is enabled.

See Anthropic's [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude) and [How to create custom skills](https://support.claude.com/en/articles/12512198-how-to-create-custom-skills) for the current host flow and ZIP requirements.

### Claude Code project skill

For a project-local Claude Code installation, extract or copy the skill folder so the project contains:

    .claude/
      skills/
        omniview-looking-glass/
          SKILL.md
          NOTICE.md
          LICENSE.md
          package-manifest.yaml
          assets/
          evals/
          references/

Claude's current documentation identifies `.claude/skills/<name>/SKILL.md` as the project skill location. Start a new Claude Code session, then invoke the skill explicitly before testing automatic selection.

### Check Claude discovery

Ask:

> Use OmniView to open a prompt-only view onto Uruk around 3200 BC at first light.

For Claude Code, you may also inspect the available custom commands or skills and invoke the installed name explicitly if the host exposes it that way.

## First-value acceptance check

Use this exact request:

> Open a prompt-only view at Point Nemo in AD 1500 at 23:30 local time. The year is all I know.

The response should:

- use a declared virtual aperture over open water;
- compose ocean, atmosphere, depth, surface action, and broad night luminance;
- avoid inventing land, a vessel, a famous event, a lunar phase, or exact weather;
- report `prompt-only` and zero dispatches.

This is a behavioral acceptance check. It does not prove installation unless the host also shows that the installed skill supplied the behavior.

## Update or remove

Before updating, move the existing `omniview-looking-glass` folder or ZIP record to a clearly named backup. Install the replacement as a complete unit; do not mix files from different versions.

To remove a local installation, move the complete skill folder out of the host's skill directory and start a new session. In Claude's uploaded-skill interface, disable or remove the skill through **Customize > Skills**.

If discovery or behavior is unclear, stop before replacing more files and use [Troubleshooting](TROUBLESHOOTING.md). For complete update, removal, rollback, and data-cleanup boundaries, read [Lifecycle](LIFECYCLE.md).
