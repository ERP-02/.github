# ERP-02 — Organization Agent Rules

Shared instructions for Codex and Claude Code. Repository instructions add local details; explicit user instructions take precedence over these defaults within the active session's permissions.

## Load the right context
- Load each instruction source once per task; references between organization and documentation rules are a reading graph, not a recursive checklist. Resolve paths from the target repository root, not a nested shell directory.
- In a target repository, read its root `AGENTS.md` and the relevant nested `AGENTS.md`; Claude adapters import those same files. Read the assigned issue when one exists; a direct user request is also valid scope.
- This file is public at https://github.com/ERP-02/.github/blob/master/AGENTS.md (raw: https://raw.githubusercontent.com/ERP-02/.github/master/AGENTS.md). Prefer the sibling `../.github/AGENTS.md` when available, including locally prepared changes. Otherwise retrieve the public file; a link alone does not load instructions.
- Architecture and internal standards require a local `ERP-02/documentation` checkout. Resolve `ERP_DOCUMENTATION_DIR` if set, otherwise `../documentation` from the target repository root. If missing, obtain it with `gh repo clone ERP-02/documentation ../documentation` from that root; use the explicit override path instead when configured. Never overwrite an existing directory or reset/pull a dirty checkout.
- Read `AGENTS.md` and `standards/agent-conventions.md` in that checkout, then only the ADRs/specifications relevant to the task. Read applicable Deferred constraints as well as Accepted decisions. Proposed decisions are context, not approval.
- If retrieval is blocked, report the source and exact blocker, continue independent work, and leave architecture-dependent implementation unresolved. Do not guess missing decisions. Record the local commit or remote ref used when it matters to cross-repository work.

## Architecture and ownership
- Preserve working repository conventions. Java 25 / Spring Boot 4.x, Gradle Kotlin DSL, React / TypeScript / Vite and the modular-monolith ERP with package modules are accepted (ADR-0001, ADR-0002, ADR-0009, 2026-11-11). Changing a framework or adding a persistence or messaging technology needs a new ADR. Business module scope and accounting rules are in ADR-0015. Skills do not approve technology choices.
- ERP tenancy/identity are Accepted in `architecture/adr/ADR-0013-dedicated-tenant-central-identity.md` in the resolved documentation checkout (owner decision, 2026-11-10). Read it for affected work: cloud only; dedicated ERP/workflow applications, PostgreSQL and Redis per tenant; separate ERP/workflow databases; fixed deployment tenant; tenant-local Company/Branch rows; central scoped roles/permissions; BFF + OIDC/PKCE; service OAuth2/JWT/TLS; ERP transactional outbox. Accepted ADR-0014 adds the owner's Identity decisions: self-built Identity on standard OAuth2/OIDC libraries, 10 min access / 7 day refresh tokens, revalidation under 5 min, revocation and Identity-outage tolerance of at most 5 min, fail closed; backup/recovery implementation is Deferred. Implement the versioned `contracts/` in the documentation checkout. No dynamic tenant datasource routing, shared cross-tenant business tables or on-prem delivery. Preserve existing workflow contracts; workflow-engine changes require a separately authorized scope.
- Each repository owns its code, schema and public contracts. Do not read or write another service's database directly or silently change another repository's model.
- Contract changes need identified consumers, compatibility assessment and review in the owning repository. Avoid cross-repository dependencies without an accepted decision or explicit review.
- Use environment-driven configuration, least privilege, migrations and idempotency where the actual operation requires them.

## Work and verification
- Inspect the existing implementation and available commands before selecting tools. Keep changes within scope and preserve unrelated work.
- For a behavior defect, add a regression check when practical. Use focused checks while editing and the repository's applicable checks before handoff. Documentation-only changes need link/instruction checks, not an invented application test suite.
- Report verification as PASS, FAIL or NOT VERIFIED with commands and relevant limitations. Configuration files alone do not prove a running integration.
- Never commit secrets, private keys, real credentials, `.env` files or production data. Preserve safe `.env.example` templates.
- Do not delete persistent data, rewrite shared history or run destructive cleanup without explicit scope.

## Delivery
- When the owner invokes the configured multi-repository Ready queue, follow the parent workspace entrypoint (versioned in `workspace/AGENTS.md`) and `standards/ready-issue-workflow.md` in the documentation checkout. That explicit workflow authorizes sequential issue branches, commits, push/PR delivery and its stated Project transitions. Merging, issue closure and Done are authorized only when the owner's invocation explicitly grants them, following the workflow's owner-authorized completion section (verified checks, no bypassed protections, Deferred scope never closed). Deployment is never authorized by it. Other tasks retain the authorization rules below.
- Default to an issue branch and PR delivery when that workflow is requested. Explicit instructions to use the current branch, commit only, skip PRs, or work without an issue override that default; do not ask again.
- Commit only when authorized. Push, PR creation, merge, issue closure and Project status changes require authorization for those actions; a skill does not grant it.
- Use `Refs #N` when the issue should remain open. Use closing keywords only when automatic closure is intended and authorized.
- Summarize the result, verification and remaining decisions. Never turn a Proposed or Deferred ADR into Accepted without the user's explicit decision.

## Shared task procedures
Read these only for the matching task, from this checkout or the corresponding public URL. In sibling repositories these are referenced procedures, not automatically installed slash commands.
- Issue implementation: [.agents/skills/issue-development/SKILL.md](.agents/skills/issue-development/SKILL.md).
- Public API or event changes: [.agents/skills/api-contract-change/SKILL.md](.agents/skills/api-contract-change/SKILL.md).
- Read-only review: [.agents/skills/code-review/SKILL.md](.agents/skills/code-review/SKILL.md).
