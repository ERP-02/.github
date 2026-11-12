# Local test stack

Runs the whole system for one tenant on this machine for manual testing. Central Identity runs once. The tenant gets its own ERP (backend with the bundled frontend), workflow-engine, PostgreSQL (separate `erp_db` and `workflow_db`) and Redis. This is not a deployment template: production uses the `infrastructure` repository (TLS, digest-pinned images, isolated networks, secret manager).

Requires Docker with Compose and the sibling `erp`, `identity-service`, `workflow-engine` and `infrastructure` checkouts next to this `.github` checkout. No sibling repository is modified.

```bash
cd .github/local-dev
./init-env.sh                          # once: creates .env with random local secrets (never overwrites)
docker compose up -d --build --wait    # first build takes several minutes
```

| What | Address | Notes |
| --- | --- | --- |
| ERP + frontend | http://localhost:8080 | Use `localhost`, not `127.0.0.1`. Log in with `LOCAL_ADMIN_USERNAME` / `LOCAL_ADMIN_PASSWORD` from `.env`. |
| Workflow UI | http://localhost:5173 | Enter tenant `00000000-0000-4000-8000-000000000001` to see this tenant's data. |
| Identity (issuer) | http://localhost:9000 | |
| Workflow API (ERP-facing) | http://localhost:8081 | `oidc` mode: needs a token from Identity. |
| PostgreSQL | `127.0.0.1:15432` | Superuser `postgres`; `identity_db`, `erp_db`, `workflow_db`. |

The admin user is provisioned with `ORG_ADMIN` on the whole tenant.

```bash
docker compose ps
docker compose logs -f erp identity workflow
docker compose up -d --build --wait    # after pulling new code
docker compose down                    # stop; data is kept
docker compose down -v                 # stop and DELETE all local databases
```

## How it fits together

- Identity, ERP and the ERP-facing workflow instance share one network namespace. `http://localhost:9000`, `:8080` and `:8081` therefore mean the same thing to the browser and to every service, which is what makes the loopback-only http configuration work.
- There are two workflow backends on the same `workflow_db`:
  - `workflow` runs in `oidc` mode and validates tokens. The ERP outbox dispatcher calls it with the ERP's service token.
  - `workflow-ui-backend` runs in workflow-engine's `header` development mode, which has **no authentication**. It serves only the workflow UI, because that UI sends `X-Tenant-Id`/`X-Roles` headers instead of tokens. Both see the same data.
- Database setup runs only on an empty volume:
  - the infrastructure Identity init script, unchanged;
  - `postgres-init/20-tenant-databases.sh`, which creates `erp_db` and then runs infrastructure's `tenant-stack/postgres-ops/ensure-workflow-roles.sh` for `workflow_db`. That script creates workflow-engine's role layout with the random passwords from `.env`.
- `./init-env.sh` only adds missing keys to an existing `.env`. For a volume created by an earlier version of this stack, run it, then `docker compose up -d --wait postgres` and `docker compose exec postgres bash /opt/erp-ops/ensure-workflow-roles.sh`, then `docker compose up -d --build --wait`.
- If you change passwords already in `.env`, run `docker compose down -v` (this deletes local data).
- No observability stack is included. OTLP export is disabled.

## Role assignments

Open **http://localhost:9000/admin**, sign in as the admin user, choose the workspace and assign roles there. To try other users, add them as members first. Users themselves are still created by provisioning: add one to the `provisioning` config in `compose.yaml`, then `docker compose up -d identity`. `ORG_VIEWER` reads everything, `ORG_ADMIN` can do everything, and `BRANCH_ADMIN` reads and runs one branch's operations.

## Known limitations

- No purchase-approval workflow definition exists, so `erp.procurement.approval-workflow-definition` stays empty and the ERP starts no workflow yet. The ERP → workflow call itself works: Identity's `at+jwt` service token is accepted (workflow-engine#18).
