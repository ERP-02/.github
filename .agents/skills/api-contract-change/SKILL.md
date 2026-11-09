---
name: api-contract-change
description: Assess and implement requested public API or event contract changes, identifying ERP-02 owners, consumers, compatibility and verification.
---

# API and Event Contract Change

1. Resolve the owning repository and the actual contract source: OpenAPI, event schema, public library types or documented protocol. Read applicable local documentation and ADR constraints.
2. Identify callers and existing behavior for fields, validation, errors, pagination, authorization and retries. Separate known consumers from assumptions.
3. Preserve compatibility where possible. For a necessary break, document the version/migration path and obtain the required decision before implementation; do not silently change consumers in sibling repositories.
4. Preserve existing tenant context where defined. Do not invent ERP tenant headers, claims or identifiers while its tenancy ADR is deferred.
5. Update the canonical contract and regenerate clients only with established tooling. Avoid hand-editing generated code.
6. Verify positive, invalid-input and relevant authorization/error cases against the contract. Check idempotency when the operation can be retried. Report consumer checks that could not run.
7. Summarize the before/after behavior, affected consumers, compatibility and rollout order. Editing a contract does not authorize publication or release.
