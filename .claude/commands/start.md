---
description: "Claim a ticket and set up the branch. Argument: ticket ID (optional, default = next ticket)"
argument-hint: "[P1-0xx]"
---

Ticket: $ARGUMENTS (if empty, use the result of `python scripts/board.py --next`).

1. Read `AGENTS.md`, the ticket file in `backlog/tickets/`, and the latest session log in `sessions/`.
2. Make sure `owner: agent`, status is `todo` or `in-progress`, and all `depends_on` are `done`. If not, stop and explain.
3. `git checkout main && git pull` (if there is a remote), then `git checkout -b t/<ID>-<slug>` (or check out the existing branch).
4. Set `status: in-progress`, run `python scripts/board.py`, commit `[<ID>] start`.
5. Write a short plan (3–6 steps) based on the Tasks and Done criteria sections, then start working.
