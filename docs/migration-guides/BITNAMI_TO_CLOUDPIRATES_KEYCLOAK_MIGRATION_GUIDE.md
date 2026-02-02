# Quick Migration Guide: Bitnami Keycloak 25.x → CloudPirates Keycloak 26.x

**Estimated Time**: 30-90 minutes depending on realm complexity

> ⚠️ **Important**: This migration requires downtime. Schedule a maintenance window.

## Prerequisites

- Kubernetes cluster access with `kubectl`
- Helm 3.x installed
- Maintenance window scheduled
- Access to the PR/branch with CloudPirates changes (or update Chart.yaml/values.yaml manually)
- Backup of existing Keycloak realm data

## Key Information

| Item | Value |
|------|-------|
| Keycloak pod | `<release-name>-keycloak-0` |
| Secret name | `<release-name>-keycloak` |
| Source version | Keycloak 25.0.6 (Bitnami) |
| Target version | Keycloak 26.5.2 (CloudPirates) |
| Chart source | Bitnami → CloudPirates OCI |
| Chart version | 23.0.0 → 0.13.6 |

---

## Key Differences Between Bitnami and CloudPirates Charts

### Configuration Structure Changes

| Bitnami (Old) | CloudPirates (New) | Description |
|---------------|-------------------|-------------|
| `keycloak.auth.adminUser` | `keycloak.keycloak.adminUser` | Admin user configuration nested under `keycloak` |
| `keycloak.auth.adminPassword` | `keycloak.keycloak.adminPassword` | Admin password location |
| `keycloak.proxy` | `keycloak.keycloak.proxyHeaders` | Proxy configuration (values: `xforwarded`, `forwarded`) |
| `keycloak.httpRelativePath` | `keycloak.keycloak.httpRelativePath` | HTTP relative path |
| `keycloak.production` | `keycloak.keycloak.production` | Production mode flag |
| `keycloak.realm` | `keycloak.ichubRealm` | ICHub custom realm configuration (renamed to avoid conflicts) |
| `keycloak.initContainers` | `keycloak.extraInitContainers` | Init containers configuration |
| `keycloak.ingress.hostname` | `keycloak.ingress.hosts[].host` | Ingress hostname format |
| `keycloak.ingress.tls: true` | `keycloak.ingress.tls: []` | TLS configuration (array format) |

### Image Changes

| Bitnami | CloudPirates |
|---------|-------------|
| `bitnamilegacy/keycloak:25.0.6-debian-12-r0` | `keycloak/keycloak:26.5.2` |
| Custom Bitnami entrypoint | Official Keycloak image |
| Themes at `/opt/bitnami/keycloak/themes/` | Themes at `/opt/keycloak/themes/` |

### Database Configuration

| Bitnami | CloudPirates |
|---------|-------------|
| `keycloak.postgresql.enabled` | `keycloak.postgres.enabled` |
| `keycloak.externalDatabase.*` | `keycloak.database.*` |

---

## Migration Steps

### 1. Export Current Realm Data

```bash
# Get the Keycloak admin password
KEYCLOAK_PASSWORD=$(kubectl get secret <release-name>-keycloak -o jsonpath="{.data.admin-password}" | base64 --decode)

# Port forward to Keycloak
kubectl port-forward svc/<release-name>-keycloak 8080:80 &

# Export realm using Keycloak Admin CLI (if available in pod)
# Or use the Keycloak Admin Console to export:
# 1. Navigate to http://localhost:8080/auth/admin
# 2. Login with admin credentials
# 3. Go to Realm Settings → Action → Partial Export
# 4. Select all options and export to JSON

# Save the exported realm JSON
mkdir -p ~/ichub-keycloak-backup
BACKUP_DATE=$(date +%Y%m%d_%H%M%S)
# Save your exported realm as: ~/ichub-keycloak-backup/realm_${BACKUP_DATE}.json

# Document current users (for verification after migration)
echo "Current users in realm - document this before migration"
```

**Expected**: Realm JSON export file saved

---

### 2. Backup Keycloak Database (if using dedicated PostgreSQL)

If Keycloak uses a dedicated PostgreSQL instance:

```bash
# Get the database password
KC_DB_PASSWORD=$(kubectl get secret ichub-postgres-secret -o jsonpath="{.data.ichub-keycloak-password}" | base64 --decode)

# Create backup of Keycloak database schema
kubectl exec <postgresql-pod> -- \
  env PGPASSWORD="${KC_DB_PASSWORD}" pg_dump -U ichub_keycloak -d ichub-postgres -n ichub_keycloak > ~/ichub-keycloak-backup/keycloak_db_${BACKUP_DATE}.sql

# Verify backup
ls -lh ~/ichub-keycloak-backup/keycloak_db_${BACKUP_DATE}.sql
```

---

### 3. Stop Current Deployment

```bash
# Navigate to chart directory
cd /path/to/industry-core-hub/charts/industry-core-hub

# Uninstall current deployment (or just Keycloak if using separate releases)
helm uninstall industry-core-hub

# If Keycloak had its own PVC, you may need to delete it
# kubectl delete pvc data-<release-name>-keycloak-0

# Verify pods are terminated
kubectl get pods -l app.kubernetes.io/name=keycloak
```

**Expected**: Keycloak pods terminated

---

### 4. Update Chart Configuration

Update `Chart.yaml` - change Keycloak dependency:

```yaml
dependencies:
  # ... other dependencies ...
  - condition: keycloak.enabled
    name: keycloak
    repository: oci://registry-1.docker.io/cloudpirates
    version: 0.13.6
```

Update `values.yaml` - adapt Keycloak configuration to CloudPirates format.

> 📄 **Reference**: See the updated [values.yaml](../../charts/industry-core-hub/values.yaml) for the complete Keycloak configuration structure. Key sections to review:
> - `keycloak.keycloak.*` - Admin credentials and server configuration
> - `keycloak.ichubRealm.*` - ICHub realm users and clients
> - `keycloak.ingress.*` - Ingress configuration (new format)
> - `keycloak.database.*` - Database connection settings

---

### 5. Update Template References

If you have custom templates that reference `.Values.keycloak.realm`, update them to use `.Values.keycloak.ichubRealm`:

```yaml
# Old reference
{{- range $user := .Values.keycloak.realm.users }}

# New reference
{{- range $user := .Values.keycloak.ichubRealm.users }}
```

Also update references from `.Values.keycloak.auth` to `.Values.keycloak.keycloak`:

```yaml
# Old reference
{{ .Values.keycloak.auth.adminUser }}

# New reference
{{ .Values.keycloak.keycloak.adminUser }}
```

---

### 6. Deploy CloudPirates Keycloak

```bash
# Update dependencies
helm dependency update

# Install CloudPirates chart
helm install industry-core-hub .

# Wait for Keycloak to be ready
kubectl wait --for=condition=ready pod/<release-name>-keycloak-0 --timeout=600s

# Verify Keycloak version
kubectl exec <release-name>-keycloak-0 -- /opt/keycloak/bin/kc.sh --version
```

**Expected**: Keycloak 26.5.2 running

---

### 7. Verify Migration

```bash
# Check Keycloak pod status
kubectl get pods -l app.kubernetes.io/name=keycloak

# Check Keycloak logs
kubectl logs <release-name>-keycloak-0 --tail=50

# Port forward to verify access
kubectl port-forward svc/<release-name>-keycloak 8080:80 &

# Access admin console
echo "Access Keycloak at: http://localhost:8080/auth/admin"

# Verify realm was imported
curl -s http://localhost:8080/auth/realms/ICHub/.well-known/openid-configuration | jq .issuer
```

**Expected**: Keycloak accessible, realm configured, users present

---

### 8. Test Application Integration

```bash
# Check backend can connect to Keycloak
BACKEND_POD=$(kubectl get pod -l app.kubernetes.io/name=industry-core-hub-backend -o jsonpath='{.items[0].metadata.name}')
kubectl logs $BACKEND_POD --tail=50

# Check frontend can authenticate
FRONTEND_POD=$(kubectl get pod -l app.kubernetes.io/name=industry-core-hub-frontend -o jsonpath='{.items[0].metadata.name}')
kubectl logs $FRONTEND_POD --tail=50
```

---

## Quick Rollback

If issues occur after migration:

```bash
# 1. Stop CloudPirates deployment
helm uninstall industry-core-hub

# 2. Delete Keycloak PVC if created
kubectl delete pvc data-<release-name>-keycloak-0

# 3. Restore Bitnami chart configuration
# Revert Chart.yaml and values.yaml to Bitnami configuration (git checkout or manual edit)

# 4. Deploy Bitnami
helm dependency update
helm install industry-core-hub .

# 5. Wait for Keycloak to be ready
kubectl wait --for=condition=ready pod/<release-name>-keycloak-0 --timeout=600s

# 6. Re-import realm if needed
# Use the backup realm JSON from Step 1
```

---

## Troubleshooting

### Common Issues

#### 1. Theme Not Loading

**Symptom**: Login page shows default Keycloak theme instead of Catena-X theme

**Solution**: Verify init container is copying themes to correct path:
```bash
kubectl logs <release-name>-keycloak-0 -c import-themes
```

The path changed from `/opt/bitnami/keycloak/themes/` to `/opt/keycloak/themes/`.

#### 2. Database Connection Failed

**Symptom**: Keycloak fails to start with database connection errors

**Solution**: Check database configuration:
```bash
# Verify database secret exists
kubectl get secret ichub-postgres-secret -o yaml

# Check if database user exists
kubectl exec <postgresql-pod> -- psql -U postgres -c "\\du ichub_keycloak"
```

#### 3. Realm Import Failed

**Symptom**: Users not present after migration

**Solution**: Check realm import job:
```bash
kubectl get jobs | grep realm-import
kubectl logs job/<release-name>-realm-import-<timestamp>
```

#### 4. Proxy/SSL Issues

**Symptom**: Redirect loops or SSL errors

**Solution**: The proxy configuration changed:
- Bitnami used `proxy: edge`
- CloudPirates uses `proxyHeaders: "xforwarded"`

Ensure your ingress/reverse proxy sends the correct headers.

---

## Configuration Mapping Reference

| Bitnami Path | CloudPirates Path | Notes |
|-------------|------------------|-------|
| `keycloak.auth.adminUser` | `keycloak.keycloak.adminUser` | Nested under keycloak |
| `keycloak.auth.adminPassword` | `keycloak.keycloak.adminPassword` | |
| `keycloak.auth.existingSecret` | `keycloak.keycloak.existingSecret` | |
| `keycloak.proxy` | `keycloak.keycloak.proxyHeaders` | Values: xforwarded, forwarded |
| `keycloak.production` | `keycloak.keycloak.production` | |
| `keycloak.httpRelativePath` | `keycloak.keycloak.httpRelativePath` | |
| `keycloak.realm` | `keycloak.ichubRealm` | Renamed to avoid conflicts |
| `keycloak.initContainers` | `keycloak.extraInitContainers` | |
| `keycloak.extraVolumeMounts[].mountPath` | `/opt/keycloak/...` | Path prefix changed |
| `keycloak.ingress.hostname` | `keycloak.ingress.hosts[].host` | Array format |
| `keycloak.ingress.tls: true/false` | `keycloak.ingress.tls: []` | Array of TLS configs |
| `keycloak.postgresql.*` | `keycloak.postgres.*` | Subchart name changed |
| `keycloak.externalDatabase.*` | `keycloak.database.*` | Renamed |

---

## NOTICE

This work is licensed under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/legalcode).

- SPDX-License-Identifier: CC-BY-4.0
- SPDX-FileCopyrightText: 2025 Contributors to the Eclipse Foundation
- Source URL: <https://github.com/eclipse-tractusx/industry-core-hub>
