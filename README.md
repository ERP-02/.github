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
