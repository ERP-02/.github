---
name: code-review
description: Review a specified ERP-02 diff, commit or repository area without editing, prioritizing actionable correctness and compatibility defects.
---

# Code Review

1. Establish the requested target and base. Read target `AGENTS.md` files and only architecture/contract sources relevant to the change.
2. Trace changed behavior through callers and tests. Look for reproducible defects in correctness, authorization, data integrity, API compatibility and operation.
3. Run read-only checks or existing tests when helpful and permitted. Do not edit files, reformat, commit or mutate GitHub during a review-only request.
4. Report findings by severity with a file/line, concrete trigger, impact and suggested correction. Distinguish confirmed defects from unresolved questions; omit speculative concerns and unrelated style changes.
5. State the inspected scope and verification gaps. If no actionable defects are found, say so without claiming untested behavior is verified.
