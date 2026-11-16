---
id: P1-080
title: "Approve candidate sources batch (owner decisions delegated)"
milestone: M2
type: research
owner: agent
review: human
status: done
priority: medium
depends_on: []
estimate: 1
outputs:
  - references/registry.yaml
---

## Context

The owner reviewed a summary of the 62 `candidate` sources (P1-072, P1-074, P1-075, P1-076, P1-078, plus older Unit 5-6 and Tier 6 candidates) and said to follow the recommendations in it. This ticket applies those decisions. It is an owner decision delegated to an agent in the chat; `review: human` so the owner can check the diff.

## Tasks

1. Approve every `candidate` except `zookeeper-wiki-zab1-0`; set `verified_on` to 2026-11-16 where empty (all were reopened by a verifier that day).
2. Reject `zookeeper-wiki-zab1-0` (user-editable wiki; `dissecting-zab-yahoo-2010` covers Zab).
3. Fix validator prerequisites for approval: NO-AUTHOR/NO-DATE markers, an attribution line for `k8s-docs-deployments`, a `free_companion` for the paywalled `alex-xu-sdi-vol1-vol2`.

## Done criteria

- [x] No `candidate` entries remain; 61 `approved`, 1 `rejected` among the batch
- [x] Owner checked the diff (confirmed in chat, 2026-11-16)
- [x] `python scripts/validate.py` passes

## Notes

- Owner decisions applied: B1 reject Zab wiki; B2 approve Mattern with the unstable-URL note; B3 approve Qiao as `rewrite-only` (stricter licence); B4 approve Django docs as `all-rights-reserved`; B5 approve Honeycomb (not as the only observability source); C approve the four Tier 6 entries as `map-only`.
- B6 (the `capacity-headroom` trigger quotes 70-80% with no source) had no recommendation and is still open: the owner must rewrite the trigger or accept it.
- `alex-xu-sdi-vol1-vol2` is paywalled, so `free_companion: [system-design-primer]` was added to satisfy the validator.
- `verified_on` for the 45 sources added this session is 2026-11-16, the day the verifier subagents reopened them; the older candidates keep their own dates.
- Next: P1-079 (map approved sources into `concepts.yaml`) is now unblocked.
