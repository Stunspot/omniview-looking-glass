# Update, remove, and clean up OmniView

The installed skill, downloaded release, optional view records, host logs, returned images, and GL4SS patch candidate are separate things. Removing one does not silently remove the others.

## Update the companion

1. Finish or preserve any Render Seed or view record you need.
2. Record the installed version and artifact.
3. Download and verify the replacement release.
4. Back up the exact existing skill folder or uploaded-skill record.
5. Replace the complete skill as one unit; do not mix versions.
6. Start a fresh host session.
7. verify discovery and run the prompt-only Point Nemo acceptance check in [Installation](INSTALLATION.md).

A copied folder is not a completed update until the fresh session discovers and invokes the intended skill.

## Remove the companion

For a local Codex or Claude Code installation, move only the complete omniview-looking-glass folder out of the host skill directory. For an uploaded Claude skill, disable or remove the exact skill through Customize and Skills. Start a fresh session and confirm the skill is no longer listed or selected.

Removing the skill does not remove saved prompts, view records, generated images, provider history, host logs, downloaded ZIPs, backups, or GL4SS files.

## Clean up data

OmniView creates no durable record by default. When a view record is requested, it is stored through the authorized host path the user chose. Review exact paths before deletion.

Consider separately:

- Render Seeds and view-record files;
- generated images or videos and their metadata;
- host conversation and tool history;
- provider-side prompt, billing, or generation history;
- downloaded release archives and extracted folders;
- backups and synchronized copies;
- disposable GL4SS control and patched candidate checkouts.

Use a recoverable trash operation where practical. Provider-side deletion and cloud-history cleanup follow those services' controls.

## Roll back

Restore the previously recorded complete artifact, start a fresh session, verify discovery, and repeat the prompt-only acceptance check. File restoration alone is not evidence of host discovery or healthy behavior.

For GL4SS drop-ins, use a disposable candidate. Reverse only patches known to have applied and only when no overlapping work exists; the safest rollback is to discard the candidate and return to the preserved clean checkout.

## No automatic channel

OmniView has no automatic updater, telemetry service, account, or background cleanup process. Customers must deliberately obtain releases, replace artifacts, and manage retained data.
