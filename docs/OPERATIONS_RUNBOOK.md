# MediCopilot Operations & Disaster Recovery Runbook

## Overview
This runbook outlines operational procedures, incident response playbooks, disaster recovery steps, and compliance maintenance for **MediCopilot Healthcare AI Platform**.

---

## 1. Incident Response Playbook

### High API Latency / Timeout Surge
1. Check Prometheus Grafana Dashboard for `medicopilot_http_request_duration_seconds`.
2. Verify Redis cache hit ratio (`REDIS_CACHE_TTL`).
3. Scale API replicas via HPA:
   ```bash
   kubectl scale deployment medicopilot-api --replicas=10 -n medicopilot
   ```

### Prompt Injection / Security Threat Surge
1. Review audit logs for detected threat category:
   ```bash
   kubectl logs -l app=medicopilot-api -n medicopilot | grep "prompt_injection"
   ```
2. Rate-limit offender IP / Token subject via Redis manager.

---

## 2. Disaster Recovery & Backup Procedures

### PostgreSQL Database Backup
```bash
pg_dump -h localhost -U postgres medicopilot > medicopilot_backup_$(date +%F).sql
```

### PostgreSQL Point-In-Time Restore
```bash
psql -h localhost -U postgres medicopilot < medicopilot_backup_2026-07-28.sql
```

---

## 3. Deployment & Zero-Downtime Upgrades

```bash
kubectl apply -f k8s/deployment.yaml
kubectl rollout status deployment/medicopilot-api
```
