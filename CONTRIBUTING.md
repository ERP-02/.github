# Contributing to ERP-02

These defaults apply to every ERP-02 repository unless its own `AGENTS.md`/`CONTRIBUTING.md` says more. Agents also follow [AGENTS.md](AGENTS.md); architecture decisions live in the `documentation` repository.

## Before you start

1. Work from an issue in the owning repository (forms: epic, task, bug, architecture decision). One task changes one owning repository; cross-repository work is split into linked tasks with native "blocked by" relations.
2. Check the issue's dependencies: an open PR or an `In Review` status is not a completed dependency.
3. A new framework, persistence/messaging technology, provider or contract change needs an accepted decision first (ADR form). Never treat a Proposed decision as accepted.

## Branches and commits

- Branch from current `master`: `feat/<issue>-<slug>`, `fix/<issue>-<slug>`, `docs/<slug>` or `chore/<slug>`.
- Commit messages follow Conventional Commits with the issue number, e.g. `feat(procurement): withholding records on supplier invoices (#214)`.
- Never force push or rewrite a pushed branch; merge `master` into it instead. Pull requests are squash-merged and the branch is deleted.
- Never commit secrets, private keys, `.env` files, real credentials, personal or production data. Keep `.env.example` templates.

## Pull request checklist

The [pull request template](pull_request_template.md) carries the checklist. A pull request is ready for review when:

- [ ] it references its issue (`Refs #N`, or a closing keyword only when closure is intended) and stays within its scope;
- [ ] acceptance criteria are met and each is demonstrated by a test or evidence;
- [ ] the repository's checks pass, and the results are reported as PASS, FAIL or NOT VERIFIED with the commands;
- [ ] breaking changes are declared with consumers, versioning and the migration plan;
- [ ] documentation, contracts and examples are updated with the behaviour.

## Minimum review criteria

A reviewer approves only when all of these hold:

1. **Correctness:** behaviour matches the issue and the versioned contract; negative cases and failure modes are tested.
2. **Security:** authorization is enforced server-side with least privilege; tenant and company isolation hold; inputs are validated; no secrets or personal data reach logs, URLs or commits; no custom cryptography.
3. **Data:** schema changes are migrations; concurrency and idempotency are handled where retries or duplicate commands are possible; records that are history are never silently edited or deleted.
4. **Compatibility:** public APIs and events stay additive within a version, or the breaking change is approved and versioned.
5. **Operations:** errors are actionable, logs/metrics/traces cover the new failure modes, and configuration is environment-driven.
6. **Ownership:** no reads or writes into another service's database, and no silent change to another repository's model.

Required CI checks must pass and branch protections are never bypassed. A pull request that changes a shared contract is reviewed in the contract's owning repository too.

## Ownership and escalation

- The owning repository (see the repository map in [workspace/AGENTS.md](workspace/AGENTS.md)) decides within its scope.
- Disagreement on scope, contracts or architecture: record the options and a recommendation on the issue, label it `state:needs-decision`, and escalate to the organization owner. Keep the work `In Progress` and continue independent work; do not merge around the open question.
- Blocked by another repository or an external party: label `state:blocked` and link the blocking issue.

## Exceptions

An exception to these rules (for example, merging while CI is unavailable, or a temporary dependency) is allowed only when:

1. the organization owner grants it explicitly, in writing, for a stated scope and period;
2. it is recorded where reviewers see it: the pull request comment states the exception and the replacement evidence (for example the local CI-equivalent commands and their PASS results), and a lasting exception gets a decision record in `documentation`;
3. it never covers committing secrets, bypassing authorization or tenant isolation, destructive cleanup or production deployment.

The exception ends when its period ends or the condition is resolved; the normal rule then applies again.

## Labels

[labels.yml](labels.yml) defines the shared taxonomy; use one label from each relevant group:

| Group | Meaning |
| --- | --- |
| `type:*` | Kind of issue: `root`, `domain`, `epic`, `task`, `bug`, `spike`, `adr`, `security`. Issue forms set it. |
| `priority:P0`–`P3` | P0 critical/blocking, P1 high, P2 medium, P3 low. |
| `state:*` | `blocked`, `needs-refinement`, `needs-decision`. The Project board's Status field tracks progress; labels only flag obstacles. |
| `concern:*` | Cross-cutting concern: `api`, `database`, `ui-ux`, `integration`, `compliance`, `testing`. |
| `area:D00`–`D20` | Business or platform domain from the roadmap (e.g. D04 Finance, D09 HR and Payroll, D18 DevSecOps). |

Maintainers apply the taxonomy with `scripts/sync-labels.sh OWNER/REPO` (dry run) and `--apply` (creates or updates, never deletes).

## Security

Report vulnerabilities privately as described in [SECURITY.md](SECURITY.md). Behaviour is governed by the [code of conduct](CODE_OF_CONDUCT.md).
