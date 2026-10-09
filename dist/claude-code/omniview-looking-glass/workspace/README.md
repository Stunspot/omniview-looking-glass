# Open OmniView

Take an impossible camera somewhere in place and time. OmniView gives curiosity a viewfinder, a time reel, and a way to look at two moments together. The workspace can create a quick image directly with a configured OpenAI API key. Your agent remains the route for source-grounded research and authored scene composition. The workspace also lets you revisit, compare, and hand off the results.

## Start the workspace

Install Python 3.10 or newer from python.org. No extra packages are required. Keep the workspace folder intact. On Windows, open `Open.cmd`. On macOS, run `chmod +x Open.command` once in Terminal, then open `Open.command`. On Linux, run `python3 host.py`.

Open starts this product or reconnects its exact existing instance, confirms its identity, and opens your browser. It uses an available loopback port. Use the same launcher after a reboot. No desktop shortcut is installed; you may create one pointing to the launcher.

## Frame your first moment

Enter **Place** and **Time**, optionally choose **Light**, then press **Create image**. This sends one image request to OpenAI, saves the returned PNG in your local collection, and shows it in the viewfinder. Your OpenAI API account may be charged. The quick image is a visual interpretation; the workspace does not research historical sources. For a source-grounded image, use **Plan with my agent instead** and ask your agent to research and render the view. The viewfinder follows your destination as you type. The century buttons move a numeric year by 100 years, preserving the BCE/CE boundary; dates and written periods remain editable directly. **Deal me a destination** fills a starting idea without researching it or generating an image. A place and time are enough for the quick image or an agent planning draft. Select **Camera notebook** to open its notebook: **Aperture** holds the location and temporal precision; **Witness** holds the viewpoint and scene; **Grounding** separates source-backed conditions, visual inference, and unresolved choices; **Render handoff** holds the complete seed and actual returned result.

**Return to viewfinder** closes the notebook and keeps edits in the current draft. **Keep this moment** writes the record and reports its revision. Leaving an edited draft asks whether to discard its unsaved changes. **Try the planning example** opens an unsaved planning scaffold whose historical conditions remain unresearched.

Open saved views from **Your time reel** or the **Turn the reel** ribbon. Search uses the title, place, time, and scene. The ribbon uses equal, ordinal spacing, not elapsed-time distances. Explicit years, BC/BCE/CE/AD years, and ISO dates such as `2000-06-15` are ordered; ambiguous periods keep their archive positions. A year alone does not determine season, weather, or exact solar geometry.

## Configure one-click rendering

Set `OPENAI_API_KEY` in the environment that launches the local host, then restart OmniView. The key stays in the host process; it is not entered in the browser or saved with a view. The default image model is `gpt-image-2.5-flare`, and `OMNIVIEW_IMAGE_MODEL` can select another model that supports the same Image API parameters. The workspace sends the place, time, optional light and scene, or an authored complete render seed to OpenAI when you press **Create image**. Each press requests one image and can incur an API charge. Do not press again while the outcome of a prior request is unknown; reload the collection first.

If no key is configured, the camera says so before you render. **Plan with my agent instead** frames the place and time without a provider request. The agent can research the world and use an exposed host image tool. A direct quick render does not provide source evidence, even when its image looks convincing.

## Bring back the image

**Create image** in the viewfinder renders the current place and time or its authored render seed and saves the result automatically. **Copy aperture brief** copies the current fields for your agent; copying does not dispatch a render. **Behind the looking glass** opens the sources and uncertainty drawer; **Inside the camera** opens viewpoint and continuity details.

After grounding the scene, enter **Complete render seed** in **Render handoff**. **Copy render seed** copies it for your agent's image tool; if the clipboard is unavailable, it downloads the seed. **Export / handoff → Download agent handoff** includes the view, evidence, uncertainty, and seed.

After an actual image return, set **Observed render state** to `host-rendered`, record **Observed host / model**, and enter **Returned image reference (HTTPS URL or local path)**. Save the view. HTTPS image references display when reachable. Local images display after saving when the reference is an existing absolute file path to a PNG, JPEG, GIF, or WebP no larger than 30 MiB. Manually registered files remain at their original paths; the workspace does not copy them. Directly generated images are stored in the collection’s `images` folder. Back up that folder with the records.

A missing or unsuitable image shows an unavailable message and retains the reference. Correct the file or URL in **Render handoff**, then save. Prompt-only, render-failed, and source-unavailable states stay explicit. Registering a result does not authenticate its historical accuracy: the image remains a reconstruction.

## Compare two moments

Open a view and select **Pin as reference**, then open another saved moment and select **Compare**. Within Compare, use **Compare to** to select another saved moment without leaving the comparison. The reference is a snapshot held for this browser-tab session. You can update it, unpin it, or **Swap reference & current**; changing the working view does not rewrite the pinned snapshot.

Compare shows actual returned images when available, with scene text otherwise. **What holds between these views?** checks recorded spatial anchor, camera, support, light, and invariant values, identifying changes and missing information. Matching text records an intended invariant; it does not prove pixel alignment or source validity.

## Continue through time

**Journey** shows the planned stops entered under **Grounding → Ordered traversal stops — one per line**. These plans are separate from the saved moments in **Turn the reel**. Select **Frame this stop**, or use **Turn time**, to start a new unsaved view and review its date.

The new view carries the place, spatial anchor, local light, viewpoint support, camera, comparison invariant, and planned route. A selected planned stop updates temporal precision from its date; Turn time leaves the new date for you to enter. Numeric years and ISO dates in the future are labeled as declared future scenarios. Review Temporal precision in Aperture, especially for dates written as periods or with an era label. The new view starts without the previous scene, habitation, source notes, inference, scenario, render seed, host, or image reference. Ground it independently and save it to add it to the collection. The workspace dispatches only when you press **Create image**, one image at a time. Agree any multi-image run with your agent.

## Choose a working environment

**Chronoscope** is a brass, leather, and clockwork optical instrument. **Pocket Universe** is a bright, chunky instant camera with printed-photo collection cards. **Midnight Cinema** places the view in a velvet picture palace with a projection console beneath its screen. Choose one under **Choose your camera**. All three expose the same records and capabilities; the preference stays in this browser. Their camera artwork is decorative interface material and is never presented as a generated destination. Old environment preferences fall back to Chronoscope.

## Save, recover, and move your work

**Export / handoff → Export view JSON** preserves the current view, including unsaved changes and unknown fields. Under **Collection tools**, **Export collection** includes saved records only. **Import JSON** accepts a record or a `records` bundle, up to 500 records and a 2 MB file. Imported records receive new identities and retain their original JSON.

Saving uses atomic replacement and revisions. If another editor or agent changed a record, your stale save is rejected and your draft remains available. Export that draft, then use **Archive & exchange → Reload saved views**, inspect the newer record, and reapply the intended changes. Earlier revisions live in `history` beside the records.

If a saved view changes or is removed while an image request is in progress, the completed image is retained as a separate **(recovered image)** moment. Its record identifies the source view and submitted revision. The newer view remains untouched; a removed source stays removed. Open the recovered moment to keep, compare or export that result. This recovery makes no second provider request.

Records stay outside the installation: Windows `%LOCALAPPDATA%\Collaborative Dynamics\omniview-looking-glass`; macOS `~/Library/Application Support/Collaborative Dynamics/omniview-looking-glass`; Linux `~/.local/share/Collaborative Dynamics/omniview-looking-glass`. `OMNIVIEW_HOME` selects an absolute owner-chosen location. The path displayed in **Collection tools** is authoritative. Back up the entire data folder, including directly generated images, and keep manually referenced local images separately. Records survive restart, relocation, and reinstall.

If the archive cannot load, use **Try again**. If startup fails, inspect `workspace.log` in the data folder. Stop this workspace's Python process when finished; the launcher will restart it. macOS launchers are included but have not been exercised on a macOS host.

## Agent and API reference

Agents can read `records/*.json`, retain unknown fields, and use the revision-aware local API with `X-Workspace-Token` from `instance.json`: GET `/api/state`; POST `/api/record` with `{ "record": {…}, "revision": N }`. Do not edit record JSON while the server is writing. GET `/api/image/<record-id>` serves an eligible local image from that authenticated saved record; it does not accept arbitrary paths.

`python host.py --no-browser` starts or reconnects and prints the launch receipt. `--data-home PATH` selects an external test store. `--serve --port 0` runs the host directly. It binds only `127.0.0.1`. The workspace calls the OpenAI Images API only when **Create image** is pressed with `OPENAI_API_KEY` configured. It has no bundled model, stores no API key, and makes no background provider calls.

## Image returned but collection saving failed

The workspace keeps the returned image path, complete render seed and observed host in an **unsaved draft** and explains that collection saving failed. Preserve the retained PNG. If storage is still unavailable, use **Export / handoff → Export view JSON** before leaving the page. After storage is writable again, press **Keep this moment** to register the existing image, then reopen the saved moment. No new generation is needed. If returning from an exported draft, import its JSON and save it; keep the referenced PNG at its recorded path. Collection success and provider success are different outcomes.

If you edit the notebook or choose another destination while an image is being created, the returned result does not replace your active work. A successfully saved image appears in **Your time reel**. If collection saving fails, a separate **Retained images** panel offers **Export retained image draft** and **Open retained image draft**. Export before leaving the page. Opening asks the usual discard question when your active draft has unsaved changes; save or export that work first. The retained draft includes the returned path, seed and observed host, and opening or exporting it makes no provider request.

**Import JSON**, **Keep this moment** and **Reload saved views** also preserve newer active work when their responses arrive late. Imported or saved records remain in the reel; open them after saving or exporting your current draft. A partial import reports how many moments were already saved: inspect those entries and import only the missing ones instead of repeating the whole file. A failed collection reload leaves your draft available for export.

A delayed collection reload cannot remove a result saved after that reload began. The camera retains later saved moments and asks you to reload again for other external changes. Older write replies also cannot replace a newer saved revision in the reel.
