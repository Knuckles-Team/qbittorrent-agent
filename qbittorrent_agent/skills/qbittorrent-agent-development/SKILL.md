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

## Steps

1. Find the owning requirement with `git grep -n "<term>" -- specs`.
   Verify a row matches before editing behavior.
2. Make the change within this connector's boundary under `qbittorrent_agent/`.
   Verify skills stay under `qbittorrent_agent/skills/`.
3. Run `uv run pytest -q` for the touched area.
   Verify the tests pass.
4. Run `pre-commit run --all-files`.
   Verify every hook reports Passed.
5. Stage reviewed paths with `git add -- <path>` and check `git diff --cached --name-status`.
   Verify only intended files are listed and the `Spec:` trailer names a declared id.

## Failure recovery

| Failure | Cause | Recovery |
|---------|-------|----------|
| Spec-trailer hook rejects the id | The id is not declared in this repository's `specs/` | Cite a row found with `git grep -n "<term>" -- specs`, or use the established receipt shown above for central rows |
| A hook fails | Formatting, spelling or a gate was violated | Read the hook output, fix the named file, and rerun `pre-commit run --all-files` |
| Skill file missing from the wheel | It sits outside `qbittorrent_agent/skills/` | Move it under `qbittorrent_agent/skills/`, which the `skills/**` package-data rule includes |
