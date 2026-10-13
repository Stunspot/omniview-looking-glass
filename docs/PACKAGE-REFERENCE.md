# Package Reference

Current complete bundle: **0.3.1**, including the portable companion, local camera and direct-image workflow.

The publicv0.1.1/v0.1.0 releases remain historical. The source repository is canonical; the current supplied complete bundle is the delivery artifact whose manifest and checksums describe its exact bytes. Camera orchestration was tested with a mocked provider; that does not establish a paid live provider result.

## Delivery artifacts

| Artifact | Assembled-kit path | Purpose |
|---|---|---|
| Orientation | `README.md` and `customer-kit/START-HERE.md` | Choose the GL4SS or companion path. |
| Codex skill | `codex/omniview-looking-glass/` | Folder install with Codex-facing metadata. |
| Claude skill | `claude/omniview-looking-glass.zip` | ZIP with one top-level skill folder. |
| GL4SS proposal | `gl4ss-dropins/` | Ordered planner and renderer patches plus verifier. |
| Documentation | `docs/` and `customer-kit/` | Install, use, verify, recover, trust, and provenance. |
| License notices | `LICENSE.md`, `TRADEMARKS.md`, and `LICENSES/` | OmniView split license, marks, and GL4SS AGPL custody. |
| Inventory | `release-manifest.json` | Machine-readable file inventory and build contract. |
| Checksums | `SHA256SUMS.txt` | Sorted SHA-256 digest for each delivered file except the checksum file itself. |

## Portable skill topology

The Codex folder and expanded Claude ZIP carry the complete skill, including the following core files and the `workspace/` directory. Compare the current manifest rather than an older twelve-file inventory:

    omniview-looking-glass/
      SKILL.md
      NOTICE.md
      LICENSE.md
      package-manifest.yaml
      assets/
        render-seed.template.md
        view-record.template.md
      evals/
        eval-manifest.yaml
        omniview-cases.yaml
      workspace/
        host.py
        README.md
        Open.cmd
        Open.command
        OmniView.app/
        Setup Windows Launcher.ps1
        Launch OmniView.ps1
        native/
        domain.json
        index.html
        app.js
        style.css
        assets/
      references/
        comparison-and-traversal.md
        grounding-and-precision.md
        render-language.md
        wormhole-optics.md

Host metadata such as `agents/openai.yaml` is included as declared by each current artifact. The workspace and all of its web assets must travel together; a SKILL.md-only copy cannot launch the camera.

## Canonical source paths

| Material | Repository source |
|---|---|
| Codex-oriented skill | `plugins/omniview-looking-glass/skills/omniview-looking-glass/` |
| Claude/generic skill | `dist/claude-code/omniview-looking-glass/` |
| GL4SS patches | `dropins/` |
| Customer documentation | `README.md`, `customer-kit/`, and `docs/` |
| Behavioral evidence | `verification/behavioral/final-v0.1.0/` |
| TestForge decision | `verification/testforge/verification-manifest.json` |

Development corpus, raw trial material, ignored candidate checkouts, and private harness paths are not customer runtime dependencies and are not included in the delivery kit.

## Verify a release

Run `python VERIFY.py` from the complete kit before opening it. The checker verifies closure, bytes, portable parity and static native bindings. To check the outer ZIP and executable modes too, pass `--archive path/to/the-complete.zip`.

Read `release-manifest.json` for version, topology, source custody, and included paths. Recompute SHA-256 digests and compare them with `SHA256SUMS.txt`.

A matching digest establishes file-byte identity with that manifest. It does not establish host discovery, invocation, source truth, provider behavior, or visual quality.

## Compatibility and maintenance

The companion uses the portable `SKILL.md` convention and host-specific installation paths documented in [Installation](INSTALLATION.md). Requalify a host whenever its skill packaging, discovery, tool, permission, or invocation contract changes.

The GL4SS patches target one exact commit. Any upstream change to the touched planner, template, compiler, schema, or public contract requires a fresh patch review and candidate verification.

Any change to runtime prompt bytes invalidates the behavioral fingerprint until the suite and reviews are rerun. Any change to customer documentation invalidates its documentation manifest and accessibility review until they are regenerated.

Use [Troubleshooting](TROUBLESHOOTING.md) to prepare a reproducible defect report. Custody and release decisions remain with Collaborative Dynamics; no automatic update or telemetry channel is included.
