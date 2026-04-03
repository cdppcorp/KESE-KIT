# AI Data Pipeline Security Check

> Source: 인공지능(AI) 보안 안내서 (KISA)
> Checklist refs: 2.1, 2.2, 2.3, 6.1

---

## 1. Data Transfer Encryption Check (2.1.1)

```bash
# Check if data transfer uses encrypted protocols
# Verify no plaintext protocols in data pipeline configs
grep -rn "http://\|ftp://\|telnet:" \
  --include="*.yaml" --include="*.yml" --include="*.json" --include="*.py" \
  /opt/ai-pipeline/config/

# Verify TLS on data ingestion endpoints
openssl s_client -connect <DATA_ENDPOINT>:443 </dev/null 2>/dev/null | \
  grep "Protocol"
```

---

## 2. Data Storage Encryption Verification (2.1.3)

```bash
# Check database encryption at rest
# PostgreSQL
psql -c "SHOW ssl;" 2>/dev/null
psql -c "SELECT datname, datallowconn FROM pg_database;" 2>/dev/null

# Check S3 bucket encryption (AWS)
aws s3api get-bucket-encryption --bucket <TRAINING_DATA_BUCKET> 2>/dev/null

# Check filesystem encryption
lsblk -o NAME,FSTYPE,MOUNTPOINT,SIZE | grep -i crypt
```

---

## 3. Data Integrity Verification (2.2.1)

```bash
# Generate checksums for training dataset
find /data/training/ -type f -exec sha256sum {} \; > /data/checksums/training.sha256

# Verify dataset integrity before training
sha256sum -c /data/checksums/training.sha256 | grep -c "FAILED"

# Check for unexpected file modifications
find /data/training/ -newer /data/checksums/training.sha256 -type f
```

---

## 4. Data Access Control Audit (2.2.2)

```bash
# List users with access to training data directory
getfacl /data/training/ 2>/dev/null || ls -la /data/training/

# Check database access privileges
# PostgreSQL
psql -c "SELECT grantee, privilege_type FROM information_schema.role_table_grants WHERE table_schema = 'ai_training';" 2>/dev/null

# Check S3 bucket policy (AWS)
aws s3api get-bucket-policy --bucket <TRAINING_DATA_BUCKET> 2>/dev/null

# Verify no public access
aws s3api get-public-access-block --bucket <TRAINING_DATA_BUCKET> 2>/dev/null
```

---

## 5. Data Poisoning Detection (2.3.1)

```bash
# Statistical anomaly detection on training data
python3 -c "
import json, statistics

# Load data distribution metadata
# Check for sudden distribution shifts
print('=== Data Distribution Check ===')
print('Check for:')
print('  - Label distribution skew (>20% deviation)')
print('  - Outlier ratio (>5% of dataset)')
print('  - Duplicate ratio (>10% of dataset)')
print('  - New class injection')
print('  - Feature range anomalies')
"

# Check data provenance logs
ls -la /data/provenance/
cat /data/provenance/latest.json 2>/dev/null | python3 -m json.tool
```

---

## 6. Data Retention & Deletion Policy Check (2.1.2, 6.1)

```bash
# Find training data older than retention period
find /data/training/ -type f -mtime +365 -exec ls -la {} \;

# Check for residual data from deleted models
find /opt/models/archived/ -type f -name "*.bin" -o -name "*.pt" -o -name "*.h5" | \
  while read f; do
    echo "Residual model file: $f ($(stat -c %y "$f" 2>/dev/null || stat -f %Sm "$f"))"
  done

# Verify secure deletion capability
which shred srm 2>/dev/null && echo "Secure deletion tools available" || echo "WARNING: No secure deletion tools found"
```

---

## 7. PII & Sensitive Data Detection (2.1.2)

```bash
# Scan training data for potential PII patterns
grep -rn -E \
  "[0-9]{6}-[0-9]{7}|[0-9]{3}-[0-9]{2}-[0-9]{5}|[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}" \
  /data/training/ --include="*.csv" --include="*.json" --include="*.txt" | head -20

# Check for Korean resident registration numbers (주민등록번호)
grep -rn -E "[0-9]{6}-[1-4][0-9]{6}" \
  /data/training/ --include="*.csv" --include="*.json" | head -10
```

---

## Verification Checklist

| Item | Check Command | Expected |
|------|--------------|----------|
| No plaintext protocols | `grep http://` in configs | No matches |
| Storage encryption | DB SSL / S3 encryption | Enabled |
| Data integrity | `sha256sum -c` | 0 FAILED |
| Access control | `getfacl` / DB grants | Least privilege |
| Data provenance | Provenance log check | Logs exist and current |
| Expired data | `find -mtime +365` | No files beyond retention |
| PII detection | `grep` for PII patterns | No unmasked PII |
