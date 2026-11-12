# Local test stack

Runs central Identity, one tenant ERP (backend with the bundled frontend), PostgreSQL and Redis on this machine for manual testing. It is not a deployment template: production uses the `infrastructure` repository (TLS, digest-pinned images, isolated networks, secret manager).

Requires Docker with Compose and the sibling `erp`, `identity-service` and `infrastructure` checkouts next to this `.github` checkout.

```bash
cd .github/local-dev
./init-env.sh                          # once: creates .env with random local secrets (never overwrites)
docker compose up -d --build --wait    # first build takes a few minutes
```

Open **http://localhost:8080** (use `localhost`, not `127.0.0.1`: it must match the configured origin). Log in with `LOCAL_ADMIN_USERNAME` / `LOCAL_ADMIN_PASSWORD` from `.env`.

| Service | Address |
| --- | --- |
| ERP + frontend | http://localhost:8080 |
| Identity (issuer) | http://localhost:9000 |
| PostgreSQL | `127.0.0.1:15432` (superuser `postgres`; `identity_db`, `erp_db`) |

The admin user is provisioned with `ORG_ADMIN` on the whole tenant.

```bash
docker compose ps
docker compose logs -f erp identity
docker compose up -d --build --wait    # after pulling new code
docker compose down                    # stop; data is kept
docker compose down -v                 # stop and DELETE the local databases
```

## Notes

- Identity and ERP share one network namespace, so `http://localhost:9000` and `http://localhost:8080` work the same for the browser and for both services. This makes the loopback-only http configuration work.
- The PostgreSQL init scripts are mounted from `infrastructure` unchanged and run only on an empty volume. If you edit passwords in `.env` later, run `docker compose down -v` (this deletes local data).
- workflow-engine and the observability stack are not included. The ERP runs with the workflow dispatcher off and OTLP export disabled.
- **Known limitation:** Identity's role catalog currently contains only `erp.company.*` and `erp.branch.*` (contract `authorization-v1` §6). The business module APIs (core, accounting, inventory, procurement, sales) therefore return 403 for every user until the catalog migration for those permissions exists.
