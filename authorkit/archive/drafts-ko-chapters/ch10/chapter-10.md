# 10장. 가상화 및 클라우드 점검

> Part II. 기술적 취약점 점검

---

## 개요

가상화 및 클라우드 환경은 현대 인프라의 핵심입니다. 이 장에서는 가상화 장비(V-01 ~ V-36)와 클라우드(CL-01 ~ CL-14) 점검을 다룹니다.

```
┌─────────────────────────────────────────────────────────────────┐
│            가상화 및 클라우드 취약점 점검 체계 (50개)              │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌────────────────────────┐    ┌────────────────────────┐      │
│  │      가상화 환경        │    │      클라우드 환경       │      │
│  │     V-01 ~ V-36        │    │     CL-01 ~ CL-14      │      │
│  │       (36개)           │    │       (14개)           │      │
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
│  │                    공통 점검 영역                         │   │
│  ├─────────────────────────────────────────────────────────┤   │
│  │   ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐   │   │
│  │   │  계정   │  │ 네트워크│  │ 스토리지│  │ 컨테이너│   │   │
│  │   │  관리   │  │  분리   │  │  보안   │  │  보안   │   │   │
│  │   └─────────┘  └─────────┘  └─────────┘  └─────────┘   │   │
│  │                                                         │   │
│  │  • IAM 정책          • VLAN/VPC       • 암호화        │   │
│  │  • MFA 적용          • 보안 그룹      • 퍼블릭 차단   │   │
│  │  • 최소 권한         • 방화벽 규칙    • 백업 정책     │   │
│  └─────────────────────────────────────────────────────────┘   │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 10-1. 가상화 장비 (V-01 ~ V-36)

### V-01. 하이퍼바이저 계정 관리

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **대상** | VMware vSphere, Hyper-V, KVM |
| **점검 목적** | 하이퍼바이저 관리 계정 보안 |

#### VMware vSphere 점검

```powershell
# PowerCLI로 사용자 확인
Connect-VIServer -Server vcenter.example.com
Get-VIPermission | Select Principal, Role
```

---

### V-12. 가상 네트워크 분리

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | VM 간 네트워크 격리 |

#### 권장 사항

- 용도별 VLAN/포트 그룹 분리
- 관리 네트워크 분리
- 프로덕션/개발 환경 분리

---

### V-25. 스냅샷 관리

| 항목 | 내용 |
|------|------|
| **중요도** | 중 |
| **점검 목적** | 스냅샷 누적으로 인한 성능 저하 방지 |

#### 점검 포인트

- 오래된 스냅샷 확인 (7일 이상)
- 스냅샷 체인 길이 확인

```powershell
# VMware 스냅샷 확인
Get-VM | Get-Snapshot | Select VM, Name, Created, SizeGB
```

---

## 10-2. 클라우드 환경 (CL-01 ~ CL-14)

### CL-01. IAM 계정 관리

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **대상** | AWS, Azure, GCP |
| **점검 목적** | 클라우드 계정 및 권한 관리 |

#### AWS IAM 점검

```bash
# 미사용 계정 확인
aws iam generate-credential-report
aws iam get-credential-report --output text | base64 -d

# MFA 미설정 사용자 확인
aws iam list-users --query 'Users[*].UserName' --output text | while read user; do
    mfa=$(aws iam list-mfa-devices --user-name $user --query 'MFADevices' --output text)
    if [ -z "$mfa" ]; then
        echo "MFA 미설정: $user"
    fi
done
```

---

### CL-04. 최소 권한 원칙

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 과도한 권한 부여 방지 |

#### AWS 권한 점검

```bash
# AdministratorAccess 정책 사용자
aws iam list-entities-for-policy \
    --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

> **WARNING**
> AdministratorAccess나 *:* 권한은 최소화하세요.

---

### CL-07. 스토리지 보안

| 항목 | 내용 |
|------|------|
| **중요도** | 상 |
| **점검 목적** | 퍼블릭 접근 차단, 암호화 |

#### AWS S3 버킷 점검

```bash
# 퍼블릭 버킷 확인
aws s3api list-buckets --query 'Buckets[*].Name' --output text | while read bucket; do
    acl=$(aws s3api get-bucket-acl --bucket $bucket --query 'Grants[?Grantee.URI==`http://acs.amazonaws.com/groups/global/AllUsers`]' --output text)
    if [ -n "$acl" ]; then
        echo "퍼블릭 버킷: $bucket"
    fi
done
```

---

## 10-3. 컨테이너 보안 (Docker, K8s)

### Docker 보안 점검

| 항목 | 점검 내용 |
|------|----------|
| 이미지 취약점 | 베이스 이미지 취약점 스캔 |
| 권한 실행 | --privileged 플래그 사용 금지 |
| root 실행 | 컨테이너 내 non-root 사용자 |
| 네트워크 | 불필요한 포트 노출 금지 |

#### Docker 점검 명령어

```bash
# 특권 모드 컨테이너 확인
docker ps --quiet | xargs docker inspect --format '{{.Name}}: Privileged={{.HostConfig.Privileged}}'

# root로 실행 중인 컨테이너
docker ps --quiet | xargs docker inspect --format '{{.Name}}: User={{.Config.User}}'
```

### Kubernetes 보안 점검

```bash
# Pod Security 확인
kubectl get pods --all-namespaces -o json | jq '.items[] | select(.spec.containers[].securityContext.privileged==true) | .metadata.name'

# ServiceAccount 권한 확인
kubectl get clusterrolebindings -o json | jq '.items[] | select(.subjects[].kind=="ServiceAccount")'
```

---

## 요약

| 영역 | 핵심 점검 항목 | 우선순위 |
|------|---------------|:--------:|
| 가상화 | 하이퍼바이저 계정, 네트워크 분리 | 최우선 |
| 클라우드 | IAM, 최소 권한, 스토리지 보안 | 최우선 |
| 컨테이너 | 이미지 취약점, 권한 제한 | 높음 |

---

*다음 장: 11장. PC 및 단말기 점검*
