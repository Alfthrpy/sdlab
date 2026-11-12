---
description: Close a ticket session — validate, review, log, board, PR
argument-hint: "P1-0xx"
---

Ticket: $ARGUMENTS

1. `python scripts/validate.py` must pass. Fix it if it fails.
2. Tick the Done criteria in the ticket file that are actually met. Do not tick ones that are not.
3. Review:
   - `review: agent` → call the matching reviewer subagent (`source-verifier` for research, `content-reviewer` for content/curriculum). Give it the list of changed files and the done-criteria. Fix serious findings, then repeat until it passes.
   - `review: human` → prepare a decision summary in the ticket's Notes section so the owner can decide in < 15 minutes.
4. Write the log `sessions/<YYYY-MM-DD>-<ID>.md` from `templates/session-log.md`.
5. Set the status: `done` (agent review passed), `review` (waiting for human), or leave `in-progress` (not finished). Run `python scripts/board.py`.
6. Commit, push, open PR `[<ID>] <title>` with summary, outputs, checklist, and review result.
7. If `review: agent`, CI is green, and the reviewer says pass → merge the PR.
8. Report to the owner in 3–5 lines.
