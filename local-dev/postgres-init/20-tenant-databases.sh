#!/usr/bin/env bash
# Runs once, on an empty volume. Creates the tenant's two service databases in this one PostgreSQL instance:
#   erp_db       owned by erp_app (same statements as infrastructure/tenant-stack/postgres-init/10-service-databases.sh)
#   workflow_db  set up by workflow-engine's own, unchanged init script (its roles workflow_owner, workflow_app, ...)
# The infrastructure tenant script is not used here: it creates a single workflow_app role, which conflicts with the
# role model workflow-engine's script and Flyway migrations expect.
set -euo pipefail
erp_pw="$(cat /run/secrets/erp_db_password)"
psql -v ON_ERROR_STOP=1 --username postgres --dbname postgres -v erp_pw="$erp_pw" <<'SQL'
CREATE ROLE erp_app LOGIN PASSWORD :'erp_pw' NOSUPERUSER NOCREATEDB NOCREATEROLE NOREPLICATION;
CREATE DATABASE erp_db OWNER erp_app;
REVOKE CONNECT, TEMPORARY ON DATABASE erp_db FROM PUBLIC;
GRANT CONNECT, TEMPORARY ON DATABASE erp_db TO erp_app;
CREATE DATABASE workflow_db;
SQL
psql -v ON_ERROR_STOP=1 --username postgres --dbname workflow_db -f /opt/workflow-init/01-roles-and-schema.sql
