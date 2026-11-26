# Repository bootstrap, triage and branch protection

Organization defaults for a new ERP-02 repository (workflow-engine is independent and excluded).

## New repository checklist

1. Create it private under ERP-02 with `master` as the default branch; add it to the repository map in [workspace/AGENTS.md](../workspace/AGENTS.md) and to the ownership table in the `documentation` checkout.
2. Add `AGENTS.md` (owned scope, not owned, build and test commands) and a `CLAUDE.md` that imports it; run the developer-tools agent-setup validator.
3. Add `.github/workflows/ci.yml` calling the reusable workflows of this repository, pinned to a full commit SHA, with `permissions: contents: read`, and include the `policy` job:

   ```yaml
   jobs:
     policy:
       uses: ERP-02/.github/.github/workflows/policy.yml@<commit-sha>
     docs:
       uses: ERP-02/.github/.github/workflows/docs.yml@<commit-sha>
   ```

4. Apply the label taxonomy: `scripts/sync-labels.sh ERP-02/<repo>` (dry run), then `--apply`.
5. Enable private vulnerability reporting (repository Settings → Security, or `gh api -X PUT repos/ERP-02/<repo>/private-vulnerability-reporting`) so [SECURITY.md](../SECURITY.md) works for that repository.
6. Add the repository's issues to Project 1 (ERP Platform Roadmap) and link its epics to their ROOT or domain issue.
7. Never commit secrets or `.env` files; provide `.env.example` templates and keep credentials in the deployment platform.

## Workflow policy

`scripts/check-workflows.py` enforces the rules below; `tests/run-workflow-policy-tests.sh` runs its pass and fail fixtures in `tests/workflows/`. Run it locally with `python3 scripts/check-workflows.py ../<repo>/.github/workflows` (needs PyYAML).

| Rule | Requirement |
| --- | --- |
| `pinned-action` | Every remote action and reusable workflow is pinned to a 40-hex commit SHA (add the version as a comment). |
| `permissions` | Top-level `permissions` declared, never `write-all`; each `write` scope has an inline `# reason`. |
| `no-pull-request-target` | Use `pull_request`; fork pull requests then receive no secrets. |
| `checkout-credentials` | `actions/checkout` sets `persist-credentials: false`. |
| `no-secret-in-run`, `no-secret-echo` | Secrets reach scripts only through `env:`, are never printed, and `set -x` is never used with them. |
| `no-untrusted-expression` | Titles, bodies, branch names and commit messages reach scripts only through `env:`, quoted. |
| `destructive-opt-in` | Pruning, deleting, force pushing or destroying runs only on `workflow_dispatch` behind an `if:` on an explicit input that defaults to false. |

Changing the reusable workflows or the policy is its own reviewed pull request; consumers update their pinned SHA deliberately.

## Issue triage

New issues are triaged at least weekly by the owning repository's maintainer:

1. Check the form is complete: owner repository, scope, acceptance criteria. Move an issue to the right repository if the owner is wrong; split cross-repository requests into one task per owner.
2. Label: one `type:*`, one `priority:P0`–`P3`, the relevant `area:D*` and `concern:*`, and `state:needs-refinement`, `state:needs-decision` or `state:blocked` when applicable ([CONTRIBUTING.md](../CONTRIBUTING.md#labels)).
3. Add it to Project 1 with Status `Backlog`, attach it as a sub-issue of its epic and register native "blocked by" relations.
4. Promote to `Ready` only when its blockers are completed (merged and closed as completed) and no owner decision is pending.
5. Security reports never stay public: convert to a private advisory and remove sensitive details from the public issue.

## Branch protection recommendations

Recommended for `master` once the plan allows it (currently unavailable on private repositories on GitHub Free; see `standards/ci-merge-gating.md` in the documentation checkout for the procedural gate used until then):

- require a pull request with at least one approval, dismiss stale approvals and require conversation resolution;
- require the `ci` jobs (including `policy` and `docs`) to pass on the latest commit, with the branch up to date;
- block force pushes and deletion of `master`; allow squash merges only and delete head branches automatically;
- restrict who may push to `master` to the organization owners, and do not exempt administrators.
