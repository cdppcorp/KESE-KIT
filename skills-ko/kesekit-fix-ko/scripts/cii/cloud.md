# 클라우드 점검 스크립트 (CA-01 ~ CA-19)

## 1. 계정 관리

### CA-01: 사용자 계정 관리
**점검:**
```bash
# AWS: IAM 사용자 목록 및 마지막 로그인 확인
aws iam list-users --output table
aws iam generate-credential-report
aws iam get-credential-report --output text --query Content | base64 -d

# Azure: 사용자 목록 확인
az ad user list --output table
az ad user list --query "[].{Name:displayName, UPN:userPrincipalName, Enabled:accountEnabled}" --output table

# GCP: IAM 사용자 확인
gcloud iam service-accounts list
gcloud projects get-iam-policy <PROJECT_ID> --format=json
```
**조치:**
```bash
# AWS: 불필요 계정 삭제/비활성화
aws iam delete-user --user-name <사용자명>
aws iam delete-login-profile --user-name <사용자명>
# 액세스 키 비활성화
aws iam update-access-key --user-name <사용자명> --access-key-id <키ID> --status Inactive

# Azure: 불필요 계정 삭제/비활성화
az ad user update --id <사용자ID> --account-enabled false
az ad user delete --id <사용자ID>

# GCP: 서비스 계정 삭제/비활성화
gcloud iam service-accounts disable <서비스계정이메일>
gcloud iam service-accounts delete <서비스계정이메일>
```

### CA-02: 사용자 정책 관리
**점검:**
```bash
# AWS: 사용자별 정책 확인
aws iam list-attached-user-policies --user-name <사용자명>
aws iam list-user-policies --user-name <사용자명>
aws iam list-groups-for-user --user-name <사용자명>

# Azure: 역할 할당 확인
az role assignment list --all --output table

# GCP: IAM 정책 확인
gcloud projects get-iam-policy <PROJECT_ID>
```
**조치:**
```bash
# AWS: 불필요 권한 제거, 최소 권한 원칙 적용
aws iam detach-user-policy --user-name <사용자명> --policy-arn <정책ARN>
# 그룹 기반 권한 관리
aws iam create-group --group-name <그룹명>
aws iam attach-group-policy --group-name <그룹명> --policy-arn <정책ARN>
aws iam add-user-to-group --user-name <사용자명> --group-name <그룹명>

# Azure: 역할 할당 변경
az role assignment delete --assignee <사용자ID> --role <역할명>
az role assignment create --assignee <사용자ID> --role <역할명> --scope <범위>

# GCP: IAM 바인딩 변경
gcloud projects remove-iam-policy-binding <PROJECT_ID> --member=user:<이메일> --role=<역할>
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=user:<이메일> --role=<역할>
```

### CA-03: MFA(Multi-Factor Authentication) 설정
**점검:**
```bash
# AWS: MFA 설정 여부 확인
aws iam list-virtual-mfa-devices
aws iam list-mfa-devices --user-name <사용자명>
# MFA 미설정 사용자 확인 (credential report 활용)
aws iam get-credential-report --output text --query Content | base64 -d | grep -i "false"

# Azure: MFA 상태 확인
az ad user list --query "[].{UPN:userPrincipalName}" --output table
# Azure Portal: Azure AD > 보안 > MFA 에서 확인

# GCP: 2단계 인증은 Google Workspace Admin Console에서 확인
```
**조치:**
```bash
# AWS: 가상 MFA 디바이스 생성 및 활성화
aws iam create-virtual-mfa-device --virtual-mfa-device-name <디바이스명> --outfile QRCode.png --bootstrap-method QRCodePNG
aws iam enable-mfa-device --user-name <사용자명> --serial-number <MFA ARN> --authentication-code1 <코드1> --authentication-code2 <코드2>

# Azure: 조건부 액세스 정책으로 MFA 강제 (Azure Portal에서 설정)
# Azure AD > 보안 > 조건부 액세스 > 새 정책 > MFA 필수

# GCP: Google Workspace Admin Console에서 2단계 인증 강제
```

### CA-04: 클라우드 계정 비밀번호 정책 관리
**점검:**
```bash
# AWS: 비밀번호 정책 확인
aws iam get-account-password-policy

# Azure: 비밀번호 정책 확인 (Azure AD)
az ad group list --output table
# Azure Portal: Azure AD > 보안 > 인증 방법 > 비밀번호 보호
```
**조치:**
```bash
# AWS: 비밀번호 정책 설정
aws iam update-account-password-policy \
  --minimum-password-length 8 \
  --require-symbols \
  --require-numbers \
  --require-uppercase-characters \
  --require-lowercase-characters \
  --max-password-age 90 \
  --password-reuse-prevention 24 \
  --allow-users-to-change-password

# Azure: Azure AD Portal에서 비밀번호 정책 설정
# Azure AD > 보안 > 인증 방법 > 비밀번호 보호 > 사용자 지정 금지 비밀번호 목록
```

## 2. 권한 관리

### CA-05: 인스턴스 서비스 정책 관리
**점검:**
```bash
# AWS: EC2 관련 IAM 정책 확인
aws iam list-policies --query "Policies[?contains(PolicyName,'EC2')]" --output table
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,IamInstanceProfile]" --output table

# Azure: VM 관련 역할 확인
az vm list --output table
az role assignment list --query "[?contains(scope,'Microsoft.Compute')]" --output table

# GCP: Compute Engine IAM 확인
gcloud compute instances list
```
**조치:**
```bash
# AWS: 인스턴스 관련 권한 최소화
# 전용 IAM 역할 생성 후 인스턴스에 할당
aws iam create-role --role-name <역할명> --assume-role-policy-document file://trust-policy.json
aws iam attach-role-policy --role-name <역할명> --policy-arn <정책ARN>
aws ec2 associate-iam-instance-profile --instance-id <인스턴스ID> --iam-instance-profile Name=<프로필명>

# Azure: 리소스 그룹 단위 역할 할당
az role assignment create --assignee <사용자ID> --role "Virtual Machine Contributor" --scope /subscriptions/<구독ID>/resourceGroups/<리소스그룹>

# GCP: 커스텀 역할 적용
gcloud projects add-iam-policy-binding <PROJECT_ID> --member=user:<이메일> --role=roles/compute.instanceAdmin
```

### CA-06: 네트워크 서비스 정책 관리
**점검:**
```bash
# AWS: VPC/네트워크 관련 정책 확인
aws ec2 describe-vpcs --output table
aws ec2 describe-security-groups --output table

# Azure: NSG 확인
az network nsg list --output table
az network nsg rule list --nsg-name <NSG명> --resource-group <리소스그룹> --output table

# GCP: 방화벽 규칙 확인
gcloud compute firewall-rules list
```
**조치:**
```bash
# AWS: 보안 그룹 규칙 관리
aws ec2 revoke-security-group-ingress --group-id <SG-ID> --protocol tcp --port 22 --cidr 0.0.0.0/0
aws ec2 authorize-security-group-ingress --group-id <SG-ID> --protocol tcp --port 22 --cidr <관리자IP>/32

# Azure: NSG 규칙 관리
az network nsg rule delete --nsg-name <NSG명> --resource-group <RG> --name <규칙명>
az network nsg rule create --nsg-name <NSG명> --resource-group <RG> --name <규칙명> --priority 100 --access Allow --source-address-prefixes <IP> --destination-port-ranges 22

# GCP: 방화벽 규칙 관리
gcloud compute firewall-rules delete <규칙명>
gcloud compute firewall-rules create <규칙명> --allow tcp:22 --source-ranges=<IP>/32
```

## 3. 가상 리소스 관리

### CA-07: VPC 네트워크 서브넷 관리
**점검:**
```bash
# AWS: 서브넷 구성 확인 (Public/Private 분리 여부)
aws ec2 describe-subnets --output table
aws ec2 describe-route-tables --output table
aws ec2 describe-internet-gateways --output table
aws ec2 describe-nat-gateways --output table

# Azure: 가상 네트워크 서브넷 확인
az network vnet list --output table
az network vnet subnet list --vnet-name <VNet명> --resource-group <RG> --output table

# GCP: 서브넷 확인
gcloud compute networks subnets list
```
**조치:**
```bash
# Public 서브넷: 인터넷 게이트웨이 할당
# Private 서브넷: NAT 게이트웨이 할당
# 서브넷별 네트워크 리소스 별도 설정

# AWS: NAT 게이트웨이 생성 (Private 서브넷용)
aws ec2 create-nat-gateway --subnet-id <PublicSubnetID> --allocation-id <EIP-ID>

# Azure: Private 서브넷에 NSG 적용
az network vnet subnet update --vnet-name <VNet명> --name <서브넷명> --resource-group <RG> --network-security-group <NSG명>
```

### CA-08: 가상 네트워크 리소스 관리
**점검:**
```bash
# AWS: 공인 IP 할당 인스턴스 확인
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,PublicIpAddress,PrivateIpAddress]" --output table

# Azure: 공인 IP 확인
az network public-ip list --output table
az vm list-ip-addresses --output table

# GCP: 외부 IP 확인
gcloud compute instances list --format="table(name,networkInterfaces[0].accessConfigs[0].natIP)"
```
**조치:**
```bash
# AWS: 불필요 공인 IP 해제
aws ec2 disassociate-address --association-id <연결ID>
aws ec2 release-address --allocation-id <할당ID>

# Azure: 공인 IP 해제
az network nic ip-config update --resource-group <RG> --nic-name <NIC명> --name <IP설정명> --remove publicIpAddress

# GCP: 외부 IP 제거
gcloud compute instances delete-access-config <인스턴스명> --access-config-name "External NAT"
```

### CA-09: 접근 제어 설정 관리
**점검:**
```bash
# AWS: 보안 그룹 규칙 확인 (0.0.0.0/0 허용 여부)
aws ec2 describe-security-groups --query "SecurityGroups[*].{ID:GroupId,Name:GroupName,Ingress:IpPermissions}" --output json
# 0.0.0.0/0 허용 규칙 필터링
aws ec2 describe-security-groups --filters "Name=ip-permission.cidr,Values=0.0.0.0/0" --output table

# Azure: NSG 규칙 중 Any 허용 확인
az network nsg list --query "[].{Name:name,Rules:securityRules[?sourceAddressPrefix=='*']}" --output json

# GCP: 0.0.0.0/0 허용 방화벽 규칙 확인
gcloud compute firewall-rules list --filter="sourceRanges=0.0.0.0/0"
```
**조치:**
```bash
# AWS: 불필요한 0.0.0.0/0 규칙 제거
aws ec2 revoke-security-group-ingress --group-id <SG-ID> --protocol tcp --port <포트> --cidr 0.0.0.0/0

# Azure: 불필요 규칙 삭제
az network nsg rule delete --nsg-name <NSG명> --resource-group <RG> --name <규칙명>

# GCP: 불필요 방화벽 규칙 삭제
gcloud compute firewall-rules delete <규칙명>

# 공통: 관리자 IP 또는 특정 IP에서만 접속 허용
```

### CA-10: 스토리지 리소스 퍼블릭 접근 관리
**점검:**
```bash
# AWS: S3 버킷 퍼블릭 접근 확인
aws s3api get-bucket-acl --bucket <버킷명>
aws s3api get-public-access-block --bucket <버킷명>
aws s3api get-bucket-policy --bucket <버킷명>

# Azure: 스토리지 계정 공개 접근 확인
az storage account list --query "[].{Name:name,PublicAccess:allowBlobPublicAccess}" --output table

# GCP: 버킷 IAM 확인
gsutil iam get gs://<버킷명>
```
**조치:**
```bash
# AWS: S3 퍼블릭 접근 차단
aws s3api put-public-access-block --bucket <버킷명> --public-access-block-configuration BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

# Azure: 스토리지 공개 접근 비활성화
az storage account update --name <스토리지명> --resource-group <RG> --allow-blob-public-access false

# GCP: 버킷에서 allUsers/allAuthenticatedUsers 제거
gsutil iam ch -d allUsers gs://<버킷명>
gsutil iam ch -d allAuthenticatedUsers gs://<버킷명>
```

## 4. 운영 관리

### CA-11: 관계형 데이터베이스 암호화 설정
**점검:**
```bash
# AWS: RDS 암호화 확인
aws rds describe-db-instances --query "DBInstances[*].{ID:DBInstanceIdentifier,Encrypted:StorageEncrypted}" --output table

# Azure: SQL DB 암호화 확인
az sql db tde show --server <서버명> --database <DB명> --resource-group <RG>

# GCP: Cloud SQL 암호화 확인
gcloud sql instances describe <인스턴스명> --format="value(settings.dataDiskEncryptionConfiguration)"
```
**조치:**
```bash
# AWS: RDS 암호화 활성화 (생성 시 또는 스냅샷 복원)
aws rds create-db-instance --db-instance-identifier <ID> --storage-encrypted --kms-key-id <KMS키ARN> ...

# Azure: TDE 활성화
az sql db tde set --server <서버명> --database <DB명> --resource-group <RG> --status Enabled

# GCP: 기본적으로 저장 데이터 암호화 적용됨 (CMEK 설정 가능)
```

### CA-12: 통신 구간 암호화 설정
**점검:**
```bash
# AWS: ELB/ALB SSL 인증서 확인
aws elbv2 describe-listeners --load-balancer-arn <LB-ARN> --query "Listeners[*].{Port:Port,Protocol:Protocol,Certs:Certificates}" --output table

# Azure: Application Gateway SSL 확인
az network application-gateway ssl-cert list --gateway-name <게이트웨이명> --resource-group <RG>

# 공통: TLS 버전 확인
openssl s_client -connect <호스트>:443 -tls1_2
```
**조치:**
```bash
# 공통 권고사항:
#   서버 원격 접근 시 VPN, SSH 사용
#   TLS v1.2 이상 (TLS v1.3 권장) 사용
#   블록 암호: SEED, ARIA, AES (키 128bits 이상)
#   공개키 암호: RSA (키 2048bits 이상)
#   해시: SHA-2 이상
```

### CA-13: 클라우드 서비스 사용자 계정 로깅 설정
**점검:**
```bash
# AWS: CloudTrail 설정 확인
aws cloudtrail describe-trails --output table
aws cloudtrail get-trail-status --name <트레일명>

# Azure: Activity Log 확인
az monitor activity-log list --offset 1h --output table

# GCP: Cloud Audit Logs 확인
gcloud logging read "logName:cloudaudit.googleapis.com" --limit 10
```
**조치:**
```bash
# AWS: CloudTrail 활성화
aws cloudtrail create-trail --name <트레일명> --s3-bucket-name <버킷명> --is-multi-region-trail
aws cloudtrail start-logging --name <트레일명>

# Azure: 진단 설정 활성화
az monitor diagnostic-settings create --name <설정명> --resource <리소스ID> --logs '[{"category":"AuditEvent","enabled":true}]' --storage-account <스토리지ID>

# GCP: Audit Log 기본 활성화됨, 추가 설정 시
gcloud projects get-iam-policy <PROJECT_ID> --format=json
```

### CA-14: 인스턴스 로깅 설정
**점검:**
```bash
# AWS: CloudWatch 에이전트 설치 및 로그 그룹 확인
aws logs describe-log-groups --output table

# Azure: VM 진단 설정 확인
az vm diagnostics get-default-config

# GCP: Ops Agent 설치 확인
gcloud compute instances describe <인스턴스명> --format="value(metadata.items)"
```
**조치:**
```bash
# AWS: CloudWatch 에이전트 설치 및 로그 전송
aws ssm send-command --instance-ids <인스턴스ID> --document-name "AWS-ConfigureAWSPackage" --parameters '{"action":["Install"],"name":["AmazonCloudWatchAgent"]}'

# Azure: VM 진단 확장 설치
az vm diagnostics set --resource-group <RG> --vm-name <VM명> --settings <설정JSON>

# GCP: Ops Agent 설치
gcloud compute ssh <인스턴스명> -- 'curl -sSO https://dl.google.com/cloudagents/add-google-cloud-ops-agent-repo.sh && sudo bash add-google-cloud-ops-agent-repo.sh --also-install'
```

### CA-15: 관계형 데이터베이스 로깅 설정
**점검:**
```bash
# AWS: RDS 로깅 파라미터 확인
aws rds describe-db-instances --query "DBInstances[*].{ID:DBInstanceIdentifier,Logs:EnabledCloudwatchLogsExports}" --output table

# Azure: SQL 감사 설정 확인
az sql server audit-policy show --server <서버명> --resource-group <RG>

# GCP: Cloud SQL 로그 플래그 확인
gcloud sql instances describe <인스턴스명> --format="value(settings.databaseFlags)"
```
**조치:**
```bash
# AWS: RDS 로그 내보내기 활성화
aws rds modify-db-instance --db-instance-identifier <ID> --cloudwatch-logs-export-configuration '{"EnableLogTypes":["audit","error","general","slowquery"]}'

# Azure: SQL 감사 활성화
az sql server audit-policy update --server <서버명> --resource-group <RG> --state Enabled --storage-account <스토리지명>

# GCP: Cloud SQL 감사 로그 활성화
gcloud sql instances patch <인스턴스명> --database-flags=log_output=FILE,general_log=on,slow_query_log=on
```

### CA-16: 오브젝트 스토리지 버킷 로깅 설정
**점검:**
```bash
# AWS: S3 서버 액세스 로깅 확인
aws s3api get-bucket-logging --bucket <버킷명>

# Azure: Blob Storage 진단 로그 확인
az monitor diagnostic-settings list --resource <스토리지리소스ID>

# GCP: 버킷 로깅 확인
gsutil logging get gs://<버킷명>
```
**조치:**
```bash
# AWS: S3 서버 액세스 로깅 활성화
aws s3api put-bucket-logging --bucket <버킷명> --bucket-logging-status '{"LoggingEnabled":{"TargetBucket":"<로그버킷>","TargetPrefix":"logs/"}}'

# Azure: Blob Storage 진단 로그 활성화
az monitor diagnostic-settings create --name <설정명> --resource <스토리지리소스ID> --logs '[{"category":"StorageRead","enabled":true},{"category":"StorageWrite","enabled":true},{"category":"StorageDelete","enabled":true}]'

# GCP: 버킷 로깅 활성화
gsutil logging set on -b gs://<로그버킷> gs://<대상버킷>
```

### CA-17: 로그 보관 기간 설정
**점검:**
```bash
# AWS: CloudWatch Logs 보관 기간 확인
aws logs describe-log-groups --query "logGroups[*].{Name:logGroupName,Retention:retentionInDays}" --output table
# S3 수명 주기 정책 확인
aws s3api get-bucket-lifecycle-configuration --bucket <버킷명>

# Azure: 로그 보관 정책 확인
az monitor diagnostic-settings list --resource <리소스ID>

# GCP: 로그 버킷 보관 기간 확인
gcloud logging buckets describe <버킷명> --location=global
```
**조치:**
```bash
# AWS: CloudWatch Logs 보관 기간 설정 (예: 365일)
aws logs put-retention-policy --log-group-name <로그그룹명> --retention-in-days 365

# Azure: 진단 설정에서 보관 기간 설정 (일반적으로 Azure Portal에서 설정)

# GCP: 로그 버킷 보관 기간 설정
gcloud logging buckets update <버킷명> --location=global --retention-days=365
```

### CA-18: 백업 사용 여부
**점검:**
```bash
# AWS: 백업 설정 확인
aws backup list-backup-plans --output table
aws rds describe-db-instances --query "DBInstances[*].{ID:DBInstanceIdentifier,BackupRetention:BackupRetentionPeriod}" --output table
aws ec2 describe-snapshots --owner-ids self --output table

# Azure: 백업 항목 확인
az backup item list --vault-name <볼트명> --resource-group <RG> --output table

# GCP: 스냅샷 확인
gcloud compute snapshots list
gcloud sql backups list --instance=<인스턴스명>
```
**조치:**
```bash
# AWS: 자동 백업 설정
aws backup create-backup-plan --backup-plan file://backup-plan.json
# RDS 백업 보관 기간 설정
aws rds modify-db-instance --db-instance-identifier <ID> --backup-retention-period 7

# Azure: 백업 정책 설정
az backup protection enable-for-vm --resource-group <RG> --vault-name <볼트명> --vm <VM명> --policy-name <정책명>

# GCP: 스냅샷 스케줄 생성
gcloud compute resource-policies create snapshot-schedule <정책명> --region=<리전> --max-retention-days=14 --daily-schedule
```

### CA-19: 가상 리소스 이상징후 알림 설정
**점검:**
```bash
# AWS: CloudWatch 알람 확인
aws cloudwatch describe-alarms --output table

# Azure: 경고 규칙 확인
az monitor metrics alert list --output table

# GCP: 알림 정책 확인
gcloud alpha monitoring policies list
```
**조치:**
```bash
# AWS: CloudWatch 알람 생성 (예: CPU 사용률)
aws cloudwatch put-metric-alarm --alarm-name "HighCPU" --metric-name CPUUtilization --namespace AWS/EC2 --statistic Average --period 300 --threshold 80 --comparison-operator GreaterThanThreshold --evaluation-periods 2 --alarm-actions <SNS-ARN> --dimensions Name=InstanceId,Value=<인스턴스ID>

# Azure: 메트릭 경고 생성
az monitor metrics alert create --name "HighCPU" --resource-group <RG> --scopes <리소스ID> --condition "avg Percentage CPU > 80" --action <액션그룹ID>

# GCP: 알림 정책 생성 (gcloud 또는 Cloud Console에서 설정)
# Cloud Console > Monitoring > 알림 > 정책 만들기 > 조건 및 알림 채널(SMS, 이메일) 설정
```
