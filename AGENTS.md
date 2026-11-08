# ERP-02 organization agent rules

## Before coding
- Read the target repository's README.md and AGENTS.md, the assigned issue, and relevant accepted ADRs from `ERP-02/documentation`.
- Work on a dedicated branch linked to an issue; do not push directly to main.
- Do not alter another repository's owned data model or public contracts without an issue and review in that repository.
- Never commit secrets, tokens, passwords, `.env` files, or production data.

## Architecture
- Java 25 LTS, Spring Boot 4.x for new Java services; Gradle Kotlin DSL is proposed pending ADR acceptance.
- ERP backend is a modular monolith initially. Workflow engine stays independent.
- React + TypeScript + Vite is proposed for the authenticated ERP SPA.
- Prefer explicit contracts, tenant scoping, idempotency, structured logging, and migrations.
- Each service owns its schema; no cross-service direct database access.

## Completion checklist
- Tests pass and relevant negative/authorization cases are covered.
- API/schema changes are documented and backwards compatibility assessed.
- Database changes include reversible or forward-safe migrations.
- PR references the issue and explains impact, verification and rollback.
- No new cross-repo dependency without an approved ADR or contract review.
