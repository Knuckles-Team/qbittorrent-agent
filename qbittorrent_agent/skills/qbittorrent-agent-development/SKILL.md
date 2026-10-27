---
name: qbittorrent-agent-development
domain: development
skill_type: skill
description: >-
  Develop and verify changes to qbittorrent-agent, its qBittorrent connector,
  documentation, and packaged skills.
license: MIT
tags: [qbittorrent-agent, development, connector]
metadata:
  version: '0.1.0'
---

# qbittorrent-agent development

## Rapid delivery: the 5-minute contract

Find the owning requirement before changing behavior and keep the change within
this repository's connector boundary. Use the existing package layout: skills in
`qbittorrent_agent/skills/` are included by the `skills/**` package-data rule.

The spec-trailer hook accepts only IDs declared in this repository's `specs/`.
For the central consumer criteria `PIPE-CONNSPEC-R156.3` and
`PIPE-CONNSPEC-R156.4`, use the established receipt:

`Spec: none (PIPE-CONNSPEC-R156.3/.4 are pipelines-owned; consumer specs do not define those central rows)`
