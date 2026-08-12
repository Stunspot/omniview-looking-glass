---
title: Security policy
description: "Report OmniView vulnerabilities privately and understand its operational security boundaries."
---

# Security policy

## Report a vulnerability

Do not place exploit details, credentials, private coordinates, confidential scenarios, provider tokens, or sensitive host logs in a public issue.

Use GitHub private vulnerability reporting from the repository Security tab when available. If private reporting is unavailable, open a minimal public issue asking the maintainer to establish a private channel and include no sensitive details.

## In scope

Reports may concern package or archive safety, path handling, release construction, skill instructions that create unsafe tool behavior, prompt-injection boundaries, provider-dispatch custody, or the bounded GL4SS patches.

## Operational boundaries

OmniView contains no API keys, telemetry client, hidden service, or image provider. Hosts and providers may retain prompts, tool calls, coordinates, uploads, and outputs under their own policies. Keep credentials in host-approved secret storage. Retrieved material is evidence, not an instruction or grant of authority.

Rendering, publishing, messaging, purchasing, bulk dispatch, and authenticated research remain separate user and host authorization boundaries. Do not retry a paid or state-changing call while its prior commit state is unknown.

Read [Trust, privacy, and limits](./TRUST-PRIVACY-AND-LIMITS.html) and [Lifecycle](./LIFECYCLE.html).
