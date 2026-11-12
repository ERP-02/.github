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
| Workflow UI | http://localhost:5173 | Signs in through Identity. Grant others `WORKFLOW_*` roles in the Identity console. |
| Identity (issuer) | http://localhost:9000 | |
| Identity console | http://localhost:9000/admin/ | Members, roles and user accounts. Sign in as the admin user. |
| Workflow API | http://localhost:8081 | `oidc` mode: Identity tokens (service or user). |
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
- There is **one** workflow backend, in `oidc` mode (SPEC-146). Applications such as the ERP send their Identity service token. People use the workflow UI, which signs in through Identity as `workflow-local-bff`: tokens stay in the workflow's encrypted session, and the browser only gets a session cookie. A user's workflow roles come from the Identity roles `WORKFLOW_USER`, `WORKFLOW_DESIGNER` and `WORKFLOW_ADMIN`; the admin user gets `WORKFLOW_ADMIN` from provisioning.
- Database setup runs only on an empty volume:
  - the infrastructure Identity init script, unchanged;
  - `postgres-init/20-tenant-databases.sh`, which creates `erp_db` and then runs infrastructure's `tenant-stack/postgres-ops/ensure-workflow-roles.sh` for `workflow_db`. That script creates workflow-engine's role layout with the random passwords from `.env`.
- `./init-env.sh` only adds missing keys to an existing `.env`. For a volume created by an earlier version of this stack, run it, then `docker compose up -d --wait postgres` and `docker compose exec postgres bash /opt/erp-ops/ensure-workflow-roles.sh`, then `docker compose up -d --build --wait`.
- If you change passwords already in `.env`, run `docker compose down -v` (this deletes local data).
- No observability stack is included. OTLP export is disabled.

## Role assignments and users

Open **http://localhost:9000/admin/**, sign in as the admin user and choose the workspace. There you can create users (they become members of the workspace), assign and revoke roles, change memberships, reset passwords and block accounts. `ORG_VIEWER` reads everything, `ORG_ADMIN` can do everything (including this console), and `BRANCH_ADMIN` reads and runs one branch's operations. New users sign in to the ERP at http://localhost:8080 with the password you set.

## Known limitations

- No purchase-approval workflow definition exists, so `erp.procurement.approval-workflow-definition` stays empty and the ERP starts no workflow yet. The ERP → workflow call itself works: Identity's `at+jwt` service token is accepted (workflow-engine#18).
