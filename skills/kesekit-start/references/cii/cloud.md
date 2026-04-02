# 클라우드 취약점 분석·평가 항목

> KISA 주요정보통신기반시설 기술적 취약점 분석·평가 방법 상세가이드 (2026)
> 대상: AWS, Azure, GCP 등 클라우드 환경

## 1. 계정 관리 (4항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| CA-01 | 클라우드 관리 콘솔 기본 계정 변경 | 상 |
| CA-02 | 비밀번호 복잡성 및 MFA 설정 | 상 |
| CA-03 | 불필요한 계정/키 제거 | 상 |
| CA-04 | 루트/관리자 계정 직접 사용 제한 | 상 |

## 2. 권한 관리 (2항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| CA-05 | IAM 최소 권한 원칙 적용 | 상 |
| CA-06 | 서비스 계정/역할 권한 제한 | 상 |

## 3. 가상 리소스 관리 (4항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| CA-07 | 보안 그룹/네트워크 ACL 설정 | 상 |
| CA-08 | 스토리지 접근 권한 및 암호화 | 상 |
| CA-09 | 가상 네트워크 분리 (VPC/서브넷) | 상 |
| CA-10 | 미사용 리소스 점검 및 제거 | 중 |

## 4. 운영 관리 (9항목)

| 코드 | 항목 | 중요도 |
|------|------|:------:|
| CA-11 | 클라우드 감사 로깅 활성화 | 상 |
| CA-12 | 보안 모니터링 및 알림 설정 | 상 |
| CA-13 | 데이터 백업 및 복구 정책 | 상 |
| CA-14 | 보안 패치 및 이미지 관리 | 상 |
| CA-15 | API 키/시크릿 관리 | 상 |
| CA-16 | 전송 중/저장 시 암호화 | 상 |
| CA-17 | 인스턴스 메타데이터 보호 | 중 |
| CA-18 | 컨테이너/서버리스 보안 설정 | 중 |
| CA-19 | 클라우드 서비스 가용성 관리 | 중 |

### 주요 점검 명령어
```bash
# AWS
aws iam list-users
aws iam get-credential-report
aws ec2 describe-security-groups
aws s3api get-bucket-encryption --bucket <bucket>
aws cloudtrail describe-trails

# Azure
az ad user list
az network nsg list
az storage account list

# GCP
gcloud iam service-accounts list
gcloud compute firewall-rules list
```

## 통계: 총 19항목 (상 14, 중 5, 하 0)
