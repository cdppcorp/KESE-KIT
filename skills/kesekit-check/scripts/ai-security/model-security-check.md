# AI Model Security Check

> Source: 인공지능(AI) 보안 안내서 (KISA)
> Checklist refs: 3.1, 3.2, 4.1

---

## 1. Model File Integrity Verification (4.1.2)

```bash
# Generate SHA-256 hash of model file for integrity check
sha256sum model.bin > model.bin.sha256

# Verify model file integrity before deployment
sha256sum -c model.bin.sha256
```

---

## 2. Model File Permission Hardening (4.1.2)

```bash
# Restrict model file access to service account only
chown ai-service:ai-service /opt/models/*.bin
chmod 600 /opt/models/*.bin

# Verify permissions
ls -la /opt/models/
```

---

## 3. Model Serialization Safety Check (3.3.1)

```bash
# Check for unsafe pickle deserialization in Python model files
grep -rn "pickle.load\|torch.load\|joblib.load" --include="*.py" .

# Recommended: Use safetensors format instead of pickle
# pip install safetensors
# from safetensors.torch import load_file
# model = load_file("model.safetensors")
```

---

## 4. Open Source Dependency Vulnerability Scan (3.3.1)

```bash
# Python ML dependency audit
pip-audit

# Check for known vulnerabilities in ML frameworks
pip list --outdated | grep -E "torch|tensorflow|transformers|numpy|scipy"

# Generate SBOM for ML project
syft . -o json > ml-sbom.json
grype sbom:./ml-sbom.json
```

---

## 5. Model Encryption at Rest (4.1.2)

```bash
# Encrypt model file with AES-256
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in model.bin -out model.bin.enc

# Decrypt for inference
openssl enc -aes-256-cbc -d -pbkdf2 \
  -in model.bin.enc -out model.bin
```

---

## 6. Container Image Security for ML Inference (4.1.3)

```bash
# Scan container image for vulnerabilities
trivy image <ml-inference-image>:latest

# Check for running containers with excessive privileges
docker ps --format '{{.Names}} {{.Status}}' | while read name status; do
  docker inspect "$name" --format '{{.HostConfig.Privileged}}' | grep -q "true" && echo "WARNING: $name runs as privileged"
done

# Verify no model files are exposed via volume mounts
docker inspect <container-name> --format '{{json .Mounts}}'
```

---

## 7. GPU/Accelerator Access Control (4.1.3)

```bash
# Check GPU device permissions
ls -la /dev/nvidia*

# Verify CUDA runtime version (known vulnerabilities)
nvidia-smi
nvcc --version

# Check for GPU memory isolation (MIG on A100/H100)
nvidia-smi mig -lgi
```

---

## Verification Checklist

| Item | Check Command | Expected |
|------|--------------|----------|
| Model file hash | `sha256sum -c model.sha256` | OK |
| File permissions | `ls -la /opt/models/` | 600, ai-service owner |
| No unsafe pickle | `grep pickle.load` | No matches in production |
| Dependency CVEs | `pip-audit` | No critical/high CVEs |
| Container scan | `trivy image` | No critical vulnerabilities |
| GPU access | `ls -la /dev/nvidia*` | Restricted to service user |
