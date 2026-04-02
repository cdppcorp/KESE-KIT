# Chapter 10. Virtualization and Cloud Assessment

> Part II. Technical Vulnerability Assessment

---

## Overview

Virtualization and cloud environments are core to modern infrastructure. This chapter covers Virtualization equipment (V-01 ~ V-36) and Cloud (CL-01 ~ CL-14) assessments.

```
┌─────────────────────────────────────────────────────────────────┐
│     Virtualization and Cloud Vulnerability Assessment (50)       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │   Virtualization Env   │    │      Cloud Env         │      │
│  │     V-01 ~ V-36        │    │     CL-01 ~ CL-14      │      │
│  │        (36)            │    │        (14)            │      │
│  └───────────┬────────────┘    └───────────┬────────────┘      │
│              │                              │                    │
│              ▼                              ▼                    │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │ • VMware vSphere       │    │ • AWS                  │      │
│  │ • Microsoft Hyper-V    │    │ • Microsoft Azure      │      │
│  │ • KVM/QEMU             │    │ • Google Cloud (GCP)   │      │
│  │ • Citrix Xen           │    │ • NHN Cloud / NCP      │      │
│  └───────────┬────────────┘    └───────────┬────────────┘      │
│              │                              │                    │
│              └──────────────┬───────────────┘                   │
│                             │                                    │
│                             ▼                                    │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                Common Assessment Domains                 │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │   │ Account │  │ Network │  │ Storage │  │Container│   │   │
│  │   │  Mgmt   │  │Isolation│  │Security │  │Security │   │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
│  │                                                         │   │
│  │  • IAM Policy       • VLAN/VPC      • Encryption       │   │
│  │  • MFA              • Security Group • Block public    │   │
│  │  • Least privilege  • Firewall rules • Backup policy   │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10-1. Virtualization Equipment (V-01 ~ V-36)

### V-01. Hypervisor Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | VMware vSphere, Hyper-V, KVM |
| **Purpose** | Hypervisor admin account security |

#### VMware vSphere Assessment

```powershell
# Check users with PowerCLI
Connect-VIServer -Server vcenter.example.com
Get-VIPermission | Select Principal, Role
```

---

### V-12. Virtual Network Segregation

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Network isolation between VMs |

#### Recommendations

- Separate VLAN/port groups by purpose
- Isolate management network
- Separate production/development environments

---

### V-25. Snapshot Management

| Item | Content |
|------|---------|
| **Severity** | Medium |
| **Purpose** | Prevent performance degradation from snapshot accumulation |

#### Check Points

- Identify old snapshots (7+ days)
- Verify snapshot chain length

```powershell
# VMware snapshot check
Get-VM | Get-Snapshot | Select VM, Name, Created, SizeGB
```

---

## 10-2. Cloud Environment (CL-01 ~ CL-14)

### CL-01. IAM Account Management

| Item | Content |
|------|---------|
| **Severity** | High |
| **Target** | AWS, Azure, GCP |
| **Purpose** | Cloud account and permission management |

#### AWS IAM Assessment

```bash
# Check unused accounts
aws iam generate-credential-report
aws iam get-credential-report --output text | base64 -d

# Check users without MFA
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    mfa=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
    if [ -z "$mfa" ]; then
        echo "No MFA: $user"
    fi
done
```

---

### CL-04. Principle of Least Privilege

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Prevent excessive permission grants |

#### AWS Permission Assessment

```bash
# Users with AdministratorAccess policy
aws iam list-entities-for-policy \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

> **WARNING**
> Minimize AdministratorAccess and *:* permissions.

---

### CL-07. Storage Security

| Item | Content |
|------|---------|
| **Severity** | High |
| **Purpose** | Block public access, encryption |

#### AWS S3 Bucket Assessment

```bash
# Check public buckets
aws s3api list-buckets --query 'Buckets[*].Name' --output text | while read bucket; do
    acl=$(aws s3api get-bucket-acl --bucket $bucket --query 'Grants[?Grantee.URI==`http://acs.amazonaws.com/groups/global/AllUsers`]' --output text)
    if [ -n "$acl" ]; then
        echo "Public bucket: $bucket"
    fi
done
```

---

## 10-3. Container Security (Docker, K8s)

### Docker Security Assessment

| Item | Check For |
|------|-----------|
| Image vulnerabilities | Base image vulnerability scan |
| Privileged execution | Prohibit --privileged flag |
| root execution | Use non-root user in container |
| Network | Prohibit unnecessary port exposure |

#### Docker Assessment Commands

```bash
# Check privileged mode containers
docker ps --quiet | xargs docker inspect --format '{{.Name}}: Privileged={{.HostConfig.Privileged}}'

# Containers running as root
docker ps --quiet | xargs docker inspect --format '{{.Name}}: User={{.Config.User}}'
```

### Kubernetes Security Assessment

```bash
# Check Pod Security
kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged==true) | .metadata.name'

# Check ServiceAccount permissions
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[].kind=="ServiceAccount")'
```

---

## Summary

| Domain | Key Assessment Items | Priority |
|--------|---------------------|:--------:|
| Virtualization | Hypervisor accounts, network segregation | Highest |
| Cloud | IAM, least privilege, storage security | Highest |
| Container | Image vulnerabilities, privilege restriction | High |

---

*Next Chapter: Chapter 11. PC and Endpoint Assessment*
