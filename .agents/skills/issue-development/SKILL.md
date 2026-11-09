---
name: issue-development
description: Implement an assigned issue or scoped user task across ERP-02 repositories, checking dependencies, acceptance criteria and authorized delivery.
---

# Issue Development

1. Read the target repository's `AGENTS.md`, shared rules and relevant local skill. Verify the actual Git remote before any GitHub read or write; do not hardcode an owner, issue number or Project.
2. Read the assigned issue and its dependencies when applicable. A direct request needs no fabricated issue. Extract the outcome, scope and acceptance criteria; identify only decisions that block implementation.
3. Consult the local documentation checkout for affected contracts and architecture decisions. Deferred ERP tenancy is not permission to design it; existing workflow contracts remain service-specific.
4. Inspect implementation, build files and available tests. Implement the smallest complete change; use a regression test for behavior defects and cover relevant authorization/error paths.
5. Run focused checks, review the diff, then finish applicable verification. Distinguish an unavailable dependency from a passing integration.
6. Follow the user's delivery mode. Do not create a branch/PR, push, close an issue or change Project status merely because this procedure was selected.
7. Report acceptance evidence as PASS, FAIL or NOT VERIFIED, with commands, changed repositories and unresolved decisions. Prepare commit/PR text only for the requested delivery.

A task that asks only for review stays read-only. Do not extend one repository's task into another repository without scope or owning-contract review.
