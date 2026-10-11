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

Agent conversations are session-only unless you request a view record. The browser camera saves records when you choose **Keep this moment**, import records or successfully use **Create image**. Its displayed data folder owns the collection, `history` and directly generated `images`; it is outside the installation. `OMNIVIEW_HOME` selects an owner-chosen location. Back up the entire displayed folder before a package update, and keep manually referenced images separately because they are not copied into the collection. Review exact paths before deletion.

Consider separately:

- Render Seeds and view-record files;
- generated images or videos and their metadata;
- host conversation and tool history;
- provider-side prompt, billing, or generation history;
- downloaded release archives and extracted folders;
- backups and synchronized copies;
- disposable GL4SS control and patched candidate checkouts.

Use a recoverable trash operation where practical. Provider-side deletion and cloud-history cleanup follow those services' controls.

## A returned image meets a newer edit

If a view changes or is removed while generation is in progress, the returned picture is saved as a separate **(recovered image)** moment. Its record identifies the original view and submitted revision. The newer edit remains untouched and a removed source stays removed. Open the recovered moment to inspect, compare or export it. Recovery itself makes no second provider request. A connection failure with unknown provider outcome requires inspection before another generation, not an automatic retry.

## Roll back

Restore the previously recorded complete artifact, start a fresh session, verify discovery, and repeat the prompt-only acceptance check. File restoration alone is not evidence of host discovery or healthy behavior.

For GL4SS drop-ins, use a disposable candidate. Reverse only patches known to have applied and only when no overlapping work exists; the safest rollback is to discard the candidate and return to the preserved clean checkout.

## No automatic channel

OmniView has no automatic updater, telemetry service, account, or background cleanup process. Customers must deliberately obtain releases, replace artifacts, and manage retained data.

## Image returned but collection saving failed

The workspace keeps the returned image path, complete render seed and observed host in an **unsaved draft** and explains that collection saving failed. Preserve the retained PNG. If storage is still unavailable, use **Export / handoff → Export view JSON** before leaving the page. After storage is writable again, press **Keep this moment** to register the existing image, then reopen the saved moment. No new generation is needed. If returning from an exported draft, import its JSON and save it; keep the referenced PNG at its recorded path. Collection success and provider success are different outcomes.

If you edit the notebook or choose another destination while an image is being created, the returned result does not replace your active work. A successfully saved image appears in **Your time reel**. If collection saving fails, a separate **Retained images** panel offers **Export retained image draft** and **Open retained image draft**. Export before leaving the page. Opening asks the usual discard question when your active draft has unsaved changes; save or export that work first. The retained draft includes the returned path, seed and observed host, and opening or exporting it makes no provider request.

**Import JSON**, **Keep this moment** and **Reload saved views** also preserve newer active work when their responses arrive late. Imported or saved records remain in the reel; open them after saving or exporting your current draft. A partial import reports how many moments were already saved: inspect those entries and import only the missing ones instead of repeating the whole file. A failed collection reload leaves your draft available for export.

A delayed collection reload cannot remove a result saved after that reload began. The camera retains later saved moments and asks you to reload again for other external changes. Older write replies also cannot replace a newer saved revision in the reel.
