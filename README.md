# ERP-02 shared agent and contribution rules

This public repository owns organization-wide agent rules, reusable task procedures, and GitHub issue/PR templates. Internal architecture and ADRs belong to the separate local `documentation` checkout.

- Shared rules: [AGENTS.md](AGENTS.md).
- Codex entrypoint: `AGENTS.md`; skills: `.agents/skills/<name>/SKILL.md`.
- Claude Code entrypoint: `CLAUDE.md` imports `AGENTS.md`; `.claude/skills/<name>` links to the same skill sources.
- Public source: https://github.com/ERP-02/.github/blob/master/AGENTS.md.
- Raw source: https://raw.githubusercontent.com/ERP-02/.github/master/AGENTS.md.

Sibling repositories explicitly load these rules. GitHub's shared contribution templates do not cause agents to inherit this repository's `AGENTS.md`.

Prefer a sibling checkout for local work; otherwise fetch the public source and resolve shared skill links relative to this repository, not the target service. Local unpushed changes are available only to sessions using that checkout; publish this repository before relying on new remote paths.

Keep internal service designs and private data in `documentation`. The shared rules do not install tools, grant permissions or approve architecture decisions.

## Parent workspace entrypoint

Versioned [workspace AGENTS.md](workspace/AGENTS.md) and [Claude adapter](workspace/CLAUDE.md) provide the sibling-repository map and the owner-configured single-agent Ready queue. Copy them to the parent workspace without overwriting existing files; see `documentation/standards/ready-issue-workflow.md` in the local architecture checkout for setup and live Project/dependency handling. The parent folder does not become a monorepo.

## Reusable CI workflows

`.github/workflows/` holds the reusable pull-request checks that the ERP-02 repositories call with `uses: ERP-02/.github/.github/workflows/<name>.yml@<commit>` (pin the full commit SHA; update it deliberately):

| Workflow | Runs | Inputs |
| --- | --- | --- |
| `gradle.yml` | Java 25 (Temurin) and the repository's Gradle wrapper, with Testcontainers on the runner's Docker | `working-directory`, `tasks` (default `build`), optional `playwright-directory` + `node-version-file` for backend tests that drive Chromium |
| `node.yml` | `npm ci`, then `typecheck lint test build` | `working-directory`, `node-version-file`, `scripts` |
| `docs.yml` | ERP-02/developer-tools agent-setup validator: canonical instructions, Claude adapters, skill metadata, local Markdown links | `repository-name` (defaults to the repository name) |
| `config.yml` | syntax of every tracked shell/Python script, then an optional repository script (e.g. `docker compose config` of each stack); starts no containers | `validate-script` |

The workflows request only `contents: read`, check out without persisting credentials, take no secrets and are meant for `pull_request` triggers (never `pull_request_target`), so fork pull requests receive no secrets. The agent-setup action lives in the private ERP-02/developer-tools repository, whose Actions access must allow repositories of the organization. Merge gating and the plan limitation on branch protection are described in `documentation/standards/ci-merge-gating.md`.
