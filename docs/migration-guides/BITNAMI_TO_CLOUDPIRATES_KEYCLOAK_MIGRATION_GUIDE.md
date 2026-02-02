# Industry Core Hub: Keycloak Migration Guide

**Migration**: Bitnami Keycloak 25.x → CloudPirates Keycloak 26.x

> 📖 For general migration concepts and configuration mapping, see the [Generic Keycloak Migration Guide](./GENERIC_BITNAMI_TO_CLOUDPIRATES_KEYCLOAK_MIGRATION_GUIDE.md)

## Overview

### What Changed in Industry Core Hub

| Component | Change |
|-----------|--------|
| Chart dependency | Bitnami → CloudPirates |
| Keycloak version | 25.0.6 → 26.5.2 |
| Realm configuration | `keycloak.realm` → `keycloak.ichubRealm` |
| Database connection | Automatic via service alias |
| Realm import | Custom job with keycloak-config-cli |

---

## Automatic Configuration

Industry Core Hub handles several migration complexities automatically:

### 1. Database Host Resolution

**Problem**: CloudPirates requires explicit `database.host`, but the PostgreSQL service name depends on the release name.

**Solution**: The chart creates an `ExternalName` service alias:
- Template: `templates/service-postgresql-alias.yaml`
- Fixed name: `ichub-postgresql-alias`
- Points to: `<release-name>-postgresql`

**No manual `--set` required** for database configuration.

### 2. Database Secret Format

**Problem**: CloudPirates expects `db-username` and `db-password` keys.

**Solution**: Auto-generated secret:
- Template: `templates/secret-keycloak-db.yaml`
- Name: `ichub-keycloak-db`
- Keys: `db-username`, `db-password`, `db-host`, `db-url`

### 3. Realm Import

**Method**: Post-install Kubernetes job using `keycloak-config-cli`
- Template: `templates/job-realm-import.yaml`
- ConfigMap: `templates/configmap-realm-data.yaml`
- Waits for Keycloak to be ready before importing

---

## Configuration Changes

### Template References

Update any custom templates:

```yaml
# Old (Bitnami)
{{- range $user := .Values.keycloak.realm.users }}
{{ .Values.keycloak.auth.adminUser }}

# New (CloudPirates)  
{{- range $user := .Values.keycloak.ichubRealm.users }}
{{ .Values.keycloak.keycloak.adminUser }}
```

### values.yaml Key Sections

#### Admin Configuration
```yaml
keycloak:
  keycloak:
    adminUser: admin
    adminPassword: "keycloak-admin-password"
    proxyHeaders: "xforwarded"
    production: false
    httpRelativePath: /auth  # No trailing slash!
```

#### ICHub Realm Users
```yaml
keycloak:
  ichubRealm:
    name: "ICHub"
    users:
      - username: ichub-admin
        # Password from secret: ichub-test-keycloak-realm-users
```

#### Database (Automatic)
```yaml
keycloak:
  database:
    type: postgres
    name: ichub-postgres
    host: "ichub-postgresql-alias"  # Auto-resolved
    existingSecret: "ichub-keycloak-db"  # Auto-created
  postgres:
    enabled: false  # Uses main PostgreSQL
```

---

## Migration Steps for Industry Core Hub

### Step 1: Backup Current Installation (if upgrading)

```bash
# Export realm from Admin Console:
# 1. Port forward: kubectl port-forward svc/<release>-keycloak 8080:80 -n <namespace>
# 2. Navigate to http://localhost:8080/auth/admin
# 3. Go to ICHub realm → Realm Settings → Action → Partial Export
# 4. Save the JSON file

# Backup database (optional):
kubectl exec <postgresql-pod> -n <namespace> -- \
  pg_dump -U ichub_keycloak -d ichub-postgres > ichub_keycloak_backup.sql
```

### Step 2: Update Chart.yaml

The dependency has been updated:

```yaml
# Before
dependencies:
  - condition: keycloak.enabled
    name: keycloak
    repository: oci://registry-1.docker.io/bitnamicharts
    version: 23.0.0

# After
dependencies:
  - condition: keycloak.enabled
    name: keycloak
    repository: oci://registry-1.docker.io/cloudpirates
    version: 0.13.6
```

### Step 3: Update Template References

If you have custom templates, update these references:

```yaml
# Old (Bitnami)
{{- range $user := .Values.keycloak.realm.users }}
{{ .Values.keycloak.auth.adminUser }}

# New (CloudPirates)
{{- range $user := .Values.keycloak.ichubRealm.users }}
{{ .Values.keycloak.keycloak.adminUser }}
```

### Step 4: Uninstall Current Deployment (if upgrading)

```bash
# Uninstall
helm uninstall <release-name> -n <namespace>

# Delete old secrets and PVCs (optional, for clean start)
kubectl delete pvc,secrets --all -n <namespace>

# Wait for cleanup
sleep 10
```

### Step 5: Deploy New Version

```bash
# Navigate to chart directory
cd charts/industry-core-hub

# Update dependencies
helm dependency update

# Deploy (no extra flags needed - everything is automatic)
helm install ichub . -n ichub --create-namespace

# Or upgrade existing
helm upgrade ichub . -n ichub
```

> **Note**: No `--set` flags required! Database host and secrets are configured automatically.

### Step 6: Wait for Deployment

```bash
# Watch pods
kubectl get pods -n ichub -w

# Expected output (after ~2-3 minutes):
# ichub-postgresql-0                 1/1  Running
# ichub-keycloak-0                   1/1  Running
# industry-core-hub-backend-xxx      1/1  Running
# industry-core-hub-frontend-xxx     1/1  Running
# ichub-realm-import-xxx             Completed (then deleted)
```

### Step 7: Verify Migration

```bash
# Port forward to Keycloak
kubectl port-forward svc/ichub-keycloak 8080:80 -n ichub &

# Verify realm exists
curl -s http://localhost:8080/auth/realms/ICHub | jq .realm
# Expected: "ICHub"

# Get admin token
TOKEN=$(curl -s -X POST "http://localhost:8080/auth/realms/master/protocol/openid-connect/token" \
  -d "username=admin" \
  -d "password=keycloak-admin-password" \
  -d "grant_type=password" \
  -d "client_id=admin-cli" | jq -r '.access_token')

# Verify users
curl -s "http://localhost:8080/auth/admin/realms/ICHub/users" \
  -H "Authorization: Bearer $TOKEN" | jq '.[].username'
# Expected: "ichub-admin"

# Verify clients
curl -s "http://localhost:8080/auth/admin/realms/ICHub/clients" \
  -H "Authorization: Bearer $TOKEN" | jq '.[].clientId' | grep industry
# Expected: "industry-core-hub-api", "industry-core-hub-frontend"
```

### Step 8: Test Application

```bash
# Port forward frontend
kubectl port-forward svc/industry-core-hub-frontend 3000:8080 -n ichub &

# Access application
echo "Frontend: http://localhost:3000"
echo "Login with: ichub-admin / <password-from-values.yaml>"
```

---

## Files Changed

| File | Change |
|------|--------|
| `Chart.yaml` | Keycloak dependency: Bitnami → CloudPirates 0.13.6 |
| `values.yaml` | Configuration restructured for CloudPirates |
| `templates/_helpers.tpl` | Added `ichubPassword` helper for consistent password generation |
| `templates/secret-keycloak-db.yaml` | **NEW** - Auto-creates DB secret with correct keys |
| `templates/service-postgresql-alias.yaml` | **NEW** - Auto-resolves DB host dynamically |
| `templates/secret-backend-postgres.yaml` | Updated to use shared password helper |
| `templates/configmap-realm-data.yaml` | Updated references |
| `templates/job-realm-import.yaml` | Updated for CloudPirates |

---

## Deployment

Standard deployment (no extra flags needed):

```bash
# Update dependencies
helm dependency update

# Deploy
helm install ichub ./charts/industry-core-hub -n ichub

# Or upgrade existing
helm upgrade ichub ./charts/industry-core-hub -n ichub
```

### Verify Deployment

```bash
# Check pods
kubectl get pods -n ichub

# Expected:
# ichub-keycloak-0     1/1  Running
# ichub-postgresql-0   1/1  Running

# Verify Keycloak responds
kubectl port-forward svc/ichub-keycloak 8080:80 -n ichub &
curl -s http://localhost:8080/auth/realms/ICHub | jq .realm
# Should return: "ICHub"
```

---

## Troubleshooting

### Realm Import Job Stuck

**Symptom**: `ichub-realm-import-*` pod in `Init:0/1` state

**Check init container logs**:
```bash
kubectl logs <job-pod> -c wait-for-keycloak -n ichub
```

**Common causes**:
- Keycloak not ready yet (wait longer)
- Wrong URL in wait script (check `httpRelativePath`)

### Database Connection Issues

**Symptom**: Keycloak fails with connection errors

**Verify alias service**:
```bash
kubectl get svc ichub-postgresql-alias -n ichub -o yaml
# externalName should point to <release>-postgresql.<namespace>.svc.cluster.local
```

**Verify secrets**:
```bash
kubectl get secret ichub-keycloak-db -n ichub -o jsonpath='{.data}' | jq
# Should have: db-username, db-password, db-host, db-url
```

### Users Not Imported

**Check realm import job logs**:
```bash
kubectl logs job/ichub-realm-import-<timestamp> -n ichub
```

**Verify realm exists**:
```bash
curl -s http://localhost:8080/auth/realms/ICHub | jq .realm
```

---

## Rollback

If issues occur:

```bash
# Uninstall
helm uninstall ichub -n ichub

# Revert to Bitnami (git checkout Chart.yaml and values.yaml)
git checkout HEAD~1 -- charts/industry-core-hub/Chart.yaml
git checkout HEAD~1 -- charts/industry-core-hub/values.yaml

# Redeploy Bitnami version
helm dependency update
helm install ichub ./charts/industry-core-hub -n ichub
```

---

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/industry-core-hub>
