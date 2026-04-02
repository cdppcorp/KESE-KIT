# SBOM & Supply Chain Audit

> Source: 로봇 보안취약점 점검 체크리스트 해설서 (KISA)
> Checklist refs: SC-05

---

## 1. SBOM Generation with Syft (SC-05)

Generate a Software Bill of Materials from source code or container images using Anchore Syft.

```bash
# Syft를 통한 SBOM 생성 (JSON format)
syft <소스코드 경로> -o json > sbom.json
```

---

## 2. Vulnerability Scanning with Grype (SC-05)

Scan the generated SBOM for known vulnerabilities (CVEs).

```bash
# Grype를 통한 취약점 식별
grype sbom:/<SBOM 경로>/sbom.json
```

---

## 3. Package Manager Built-in Audit Commands (SC-05)

Use built-in security features of each package manager to analyze declared dependencies and automatically scan for known vulnerabilities.

### Node.js (NPM)

```bash
npm audit
```

### Python (pip)

```bash
pip-audit
```

### Java (Maven)

```bash
mvn dependency-check:check
```

### .NET (NuGet)

```bash
dotnet list package --vulnerable
```

### Rust (Cargo)

```bash
cargo audit
```

---

## 4. CI/CD Pipeline Integration (SC-05)

Integrate vulnerability scanning into CI/CD pipelines (GitHub Actions, GitLab CI/CD, Azure DevOps, Jenkins, etc.) to automatically detect vulnerabilities before deployment.

### Vulnerability Response Record Fields

| Field | Description |
|---|---|
| CVE ID | 취약점 식별자 |
| 구성요소 | 영향받는 컴포넌트(이름/버전) |
| 기술적 위험 | 공개 PoC/익스플로잇 존재 여부, CVSS 점수 |
| 비즈니스 영향 | 영향을 받는 서비스/데이터/운영 영향 |
| EoS 여부 | 해당 구성요소의 지원상태 |
| 우선 순위 | P0/P1/P2 또는 High/Medium/Low |
| 대응방안 | 패치/업그레이드/가상패치/격리 등 |
| SLA | 목표 기간 |
| 담당자 및 일정 | 책임부서, 담당자, 완료예정일 |
| 검증 방법 | 재스캔, 기능/회귀 테스트 결과 링크 |
| 상태 | 계획/진행/완료/예외(승인) |
