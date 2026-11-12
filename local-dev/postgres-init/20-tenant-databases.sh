#!/usr/bin/env bash
# Runs once, on an empty volume. Creates the tenant's two service databases in this one PostgreSQL instance:
#   erp_db       owned by erp_app (same statements as infrastructure/tenant-stack/postgres-init/10-service-databases.sh)
#   workflow_db  roles and schema in workflow-engine's layout, by infrastructure's ensure-workflow-roles.sh
#                (also usable on an existing volume: docker compose exec postgres bash /opt/erp-ops/ensure-workflow-roles.sh)
set -euo pipefail
erp_pw="$(cat /run/secrets/erp_db_password)"
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres -v erp_pw="$erp_pw" <<'SQL'
CREATE ROLE erp_app LOGIN PASSWORD :'erp_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
CREATE DATABASE erp_db OWNER erp_app;
REVOKE CONNECT, TEMPORARY ON DATABASE erp_db FROM PUBLIC;
GRANT CONNECT, TEMPORARY ON DATABASE erp_db TO erp_app;
SQL
bash /opt/erp-ops/ensure-workflow-roles.sh
