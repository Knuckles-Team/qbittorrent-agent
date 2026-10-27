---
name: qbittorrent-agent-development
domain: development
skill_type: skill
description: >-
  Develop, verify, document, and release changes to qbittorrent-agent, including
  its qBittorrent WebUI connector, packaged skills, documentation, and CI.
license: MIT
tags: [qbittorrent-agent, development, connector, specs, gates]
metadata:
  version: '0.1.0'
---

# qbittorrent-agent development

`qbittorrent-agent` is the qBittorrent WebUI connector. It owns qBittorrent API
calls, mappings, and connector tools. Connector contracts and transports belong
to `agent-connector-sdk`; served operations and registry belong to `arbora`;
the in-run harness belongs to `agent-utilities`.

## Step 0: route the feature

Route the feature before any code.

1. Read the [ecosystem boundaries standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/ecosystem-boundaries.md).
2. Split the feature into parts with its routing procedure.
3. If a part is not owned by this repository, write its requirement in the owning repository and link it by ID. Continue here only with the qBittorrent connector work.
4. Follow `specs/README.md` and the ecosystem [spec standard](https://github.com/Knuckles-Team/pipelines/blob/main/reference/spec-standard.md).

## Rapid delivery: the 5-minute contract

Specs are already designed. Deliver implementation in small, continuously landed slices.

**Extend first**
- Before any code change, find its owner with `git grep -n "<term>" -- specs`. Cite the owning ID in the commit `Spec:` trailer.
- Extend an owning spec before adding spec text. Create a spec only when no current spec owns the capability.
- Audits, reviews, and carry-overs stay in the owning spec; they do not get separate spec directories.
- Search for and reuse an existing module or connector helper before adding another implementation.

**Time and size**
- One agent delivers one PR in five minutes or less. If a task needs more work, split it into another small PR and hand it off.
- Read only what is needed to identify the owner, the relevant code path, and the required gate. Trust supplied exact-main evidence for the other parts of the task.
- Split work when it crosses repository boundaries or has independent entry points; put each requirement in its owning repository.

**Spec receipts and verification**
- End every implementation commit with `Spec: <ID>[, <ID>...]`. For work that does not deliver a requirement, use `Spec: none (ci|deps|refactor|fix-forward)`.
- Bind a test to each delivered requirement in the same PR using `@pytest.mark.spec("<ID>")` for Python tests. Use a focused static or build check for documentation and workflow wiring.
- `specs/status.json` is generated. Never edit it by hand; use the repository's spec hooks when its inputs change.
- A requirement is delivered only when its acceptance is met. Record a concrete blocker and stop when required behavior belongs to another repository.

**Package and release**
- Skills under `qbittorrent_agent/skills/` are package data (`skills/**`) and are included in the source distribution. Keep shipped skill content there.
- Documentation, workflow, and skill-content changes do not require a Python version bump or PyPI/Docker release by themselves. A release is needed only when a runtime package change is intended for consumers; follow `.bumpversion.cfg` and rebuild `uv.lock` only when dependencies change.
- The Pages workflow publishes documentation and the spec dashboard from `main`; a PR or workflow reference alone does not prove that the dashboard has been published.

**Before every push**
- Work in a real Git worktree based on current `origin/main`. Never edit a shared checkout, use `git stash`, stage everything, or force-push.
- Inspect `git status --short` and the complete diff. Stage only reviewed paths by name.
- Run `pre-commit run --all-files` and the focused tests or checks for the changed paths. Fix reported issues before committing.
- Never hide a failing check with `noqa`, type ignores, skips, xfails, or gate bypasses.

**Landing**
- Open a PR with the requirement IDs, behavior, and checks recorded in the description.
- Merge only under the repository's authorized landing process and required CI checks. After merge, verify the generated status and deployed Pages build separately.
