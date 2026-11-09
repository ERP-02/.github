# ERP-02 multi-repository workspace

This file describes the parent workspace, not a Git repository. All paths below are relative to the parent containing the sibling checkouts, even when this template is read from `.github/workspace/`. Run one agent and one issue at a time; do not spawn subagents or parallel implementation workers.

## Repository map

| Checkout | Purpose / ownership |
| --- | --- |
| `.github` | Shared agent policy, contribution templates and workspace instruction templates. |
| `documentation` | Authoritative architecture decisions, cross-repository contracts, standards and implementation register. |
| `erp` | ERP backend/frontend, canonical business records and business rules; enforces centrally supplied access grants. |
| `identity-service` | Authentication, user identities, tenant memberships, roles, permissions and scoped assignments. |
| `infrastructure` | Runtime/deployment templates, networks, secrets integration, observability and recovery operations. |
| `integration-hub` | External connectors, mapping, webhook delivery and reconciliation; no ownership of ERP business records. |
| `reporting-engine` | Derived reports/projections; no writes to source-service databases. |
| `shared-libraries` | Small versioned contracts/utilities; no shared business entities or database coupling. |
| `developer-tools` | Optional local bootstrap, lint and validation tools; no production business behavior. |
| `workflow-engine` | Existing independent workflow engine. Excluded from this queue: do not change its files, configuration, Git branch/history, issues, PRs or Project fields. Read existing public/local contracts only when required by an ERP integration task. |

## Load instructions and authority

1. Read `.github/AGENTS.md` for shared policy, then the target repository's `AGENTS.md`, `CLAUDE.md`, applicable nested rules and matching canonical skill. Do not load every repository or all specifications up front.
2. Architecture comes from `documentation/AGENTS.md`, `documentation/standards/agent-conventions.md`, Accepted ADR-0013 and the original final decision it links. Earlier Superseded proposals do not override the accepted architecture.
3. Read `documentation/standards/ready-issue-workflow.md` for the live Ready queue procedure. Verify actual Git remotes and discover Project fields/options before mutations.
4. Preserve user changes and secrets. Inspect existing build/test configuration; do not invent tooling, provider products, contract details or unapproved architecture.

## Meaning of “Ready durumundaki issue'ları yap”

The owner configured this workspace for a single-agent GitHub issue queue. When asked to work on Ready issues, use **ERP-02 Project 1 — ERP Platform Roadmap**, not a global issue search or a status label. Select only open issue items whose built-in Project Status is exactly `Ready`; exclude ROOT/EPIC summaries, PR items and workflow-engine.

The configured delivery is one new issue branch and one PR per issue in its owning repository, based on current `master` after checking local changes. Commit the scoped implementation, push the branch and create a `master`-targeted PR with `Refs #N`. This is the owner's standing delivery preference for the invoked queue; later explicit user directions override it.

Project transitions for queue work are `Ready` → `In Progress` → `In Review`. Use `In Review` only after required checks and a concrete PR exist. No automatic PR merge, issue closure, `Done`, production deployment, credential provisioning or destructive cleanup is authorized by the Ready request.

Before starting and after handing off an issue, inspect dependencies and refresh eligibility. An open PR or an `In Review` status does not satisfy an implementation dependency. Require reviewed/merged changes, relevant check evidence and any explicit owner decision required by that dependency. A closed issue alone is also insufficient if it was cancelled or lacks completion evidence.

Promote an open `Backlog` TASK to `Ready` only when its native blocked-by relations and body/register requirements are satisfied. This queue request authorizes those evidence-based promotions; never mark every task Ready to bypass dependencies. Do not retag unrelated work or touch workflow-engine items.

If several issues are genuinely Ready, select one deterministically: highest configured Priority, then oldest creation time, then repository/number. Finish or hand off that issue before starting another. Continue with another eligible Ready issue without requesting permission for routine implementation steps.

If the issue needs a new owner decision, prepare the concrete options/recommendation and record the blocker. Keep it `In Progress` while incomplete (or `In Review` when the issue's proposal deliverable is genuinely finished and awaiting review); do not accept its proposal yourself or unblock dependent implementation. Continue independent Ready work if available.

If no Ready issue remains, refresh dependency eligibility once, report the exact pending reviews/decisions and stop. Do not start Backlog work merely to keep the agent busy. Report each issue's outcome, check results, Project status, source/target branch and PR link.

## Workspace-local entrypoints

The installed root `CLAUDE.md` imports this root `AGENTS.md`. Versioned sources live in `.github/workspace/`; the parent workspace itself is not committed as a monorepo. Repository-local Claude adapters remain in place. Do not add global Claude settings, broad tool permissions, model pins or enforcement hooks as part of this setup.
