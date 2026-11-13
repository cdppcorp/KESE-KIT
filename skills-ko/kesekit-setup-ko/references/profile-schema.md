# KESE 프로필 스키마

## 파일

| 경로 | 설명 |
|------|------|
| `.kesekit/profile.json` | 저장된 프로필. 모든 kesekit 스킬이 0단계에서 읽습니다 |
| `.kesekit/setup.html` | 입력 화면 (임시, 저장에 성공하면 삭제) |
| `.kesekit/setup-data.js` | 입력 화면에 넘기는 탐지 결과 (임시, 저장에 성공하면 삭제) |

`.kesekit/`은 점검하는 프로젝트(현재 작업 폴더) 안에 만듭니다. 호스트명 같은 환경 정보가 들어가므로 Git에 올리지 않습니다.

## profile.json 구조

```json
{
  "schemaVersion": 1,
  "updatedAt": "2026-11-14T15:20:00+09:00",
  "project": {
    "path": "C:/work/shop-api",
    "name": "shop-api",
    "gitRemote": "https://github.com/acme/shop-api.git",
    "manifests": ["Dockerfile", "package.json"]
  },
  "system": {
    "os": "windows",
    "osVersion": "Windows 11 Pro 10.0.26200",
    "arch": "x64",
    "cpu": "Intel(R) Core(TM) i7-1360P",
    "memoryGb": 32,
    "hostname": "DEV-PC01",
    "role": "dev-pc",
    "remoteSession": false
  },
  "environment": {
    "languages": ["JavaScript"],
    "frameworks": ["Express"],
    "services": [],
    "webServers": [],
    "databases": ["MySQL"],
    "containers": ["Docker"],
    "cloudClis": ["aws"],
    "aiLibraries": []
  },
  "assessment": {
    "purpose": "pre-deploy",
    "scope": ["host", "project-code"],
    "domains": ["secure-coding", "supply-chain"],
    "ciiTargets": [],
    "ztTargetMaturity": null,
    "organizationType": "startup"
  },
  "notes": {
    "common": "",
    "start": "",
    "check": "결과를 PR에 붙일 수 있게 마크다운 표로 정리",
    "fix": "스크립트는 만들기만 하고 적용하지 않음",
    "guide": ""
  }
}
```

## 선택지 값

입력 화면(`templates/setup-form.html`의 `kesekit-enums`)과 같은 순서입니다. 표에 없는 값은 저장하지 않습니다.

| 필드 | 허용 값 |
|------|---------|
| `assessment.purpose` | `cii-legal`, `pre-deploy`, `code-review`, `zt-maturity`, `general`, `other` |
| `assessment.scope` | `host`, `project-code`, `remote-systems`, `cloud`, `management` |
| `assessment.domains` | `cii`, `ai-security`, `robot-security`, `space-security`, `secure-coding`, `zero-trust`, `supply-chain` |
| `assessment.ciiTargets` | `unix`, `windows`, `web-service`, `security-equip`, `network`, `control-system`, `pc`, `database`, `mobile`, `webapp`, `virtualization`, `cloud`, `admin`, `physical` |
| `assessment.ztTargetMaturity` | `traditional`, `initial`, `advanced`, `optimal` |
| `assessment.organizationType` | `public`, `cii-operator`, `enterprise`, `startup`, `individual`, `other` |
| `system.role` | `dev-pc`, `server`, `vm`, `container`, `other` |
| `system.os` (탐지값) | `windows`, `linux`, `macos`, `other` |

- `assessment.ciiTargets` 값은 각 스킬의 `templates/cii/<값>.md` 파일 이름과 같습니다.
- `assessment.domains` 값은 각 스킬의 분야별 분기(CII, AI 보안, 로봇 보안, 우주 보안, 시큐어코딩, 제로트러스트, SW 공급망)에 대응합니다.
- `ztTargetMaturity`는 기존(`traditional`) → 초기(`initial`) → 향상(`advanced`) → 최적화(`optimal`) 순입니다.

## 필수 항목

다음 중 하나라도 없거나 비어 있으면 `INCOMPLETE`입니다.

- `schemaVersion`(= 1), `updatedAt`
- `project.path`
- `system.os`, `system.role`
- `assessment.purpose`, `assessment.scope`(1개 이상), `assessment.domains`(1개 이상)
- `assessment.domains`에 `cii`가 있으면 `assessment.ciiTargets`(1개 이상)
- `assessment.domains`에 `zero-trust`가 있으면 `assessment.ztTargetMaturity`
- 선택지 값 표에 없는 값이 들어 있어도 결측으로 봅니다

## 진단 규칙

| 코드 | 조건 |
|------|------|
| `MISSING` | 파일이 없거나, JSON으로 읽을 수 없거나, `schemaVersion`이 1이 아님. 이 경우 다른 코드는 보지 않습니다 |
| `INCOMPLETE` | 필수 항목 결측 |
| `STALE` | 오늘 날짜 − `updatedAt` 날짜 ≥ 14일 |
| `CHANGED` | 아래 비교 항목 중 하나라도 현재 값과 다름 |
| `MANUAL` | 위 코드에 해당하지 않지만 사용자가 setup을 직접 실행함 |

`MISSING`·`INCOMPLETE`·`STALE`·`CHANGED`가 하나도 없으면 OK입니다. 여러 코드가 동시에 해당하면 모두 `reasons`에 넣습니다.

변경 비교 항목:

| 항목 | 비교 방법 |
|------|-----------|
| `project.path` | 현재 작업 폴더의 절대 경로. 구분자를 `/`로 바꾸고 끝의 `/`를 지운 뒤 비교합니다. Windows에서는 대소문자를 무시합니다 |
| `project.gitRemote` | `origin` 주소(자격 증명 제거 후). 둘 다 없으면 같은 것으로 봅니다 |
| `project.manifests` | 구성 파일 목록을 집합으로 비교합니다(순서 무관) |
| `system.hostname` | 저장값과 현재값이 둘 다 있을 때만 대소문자를 무시하고 비교합니다. 탐지하지 못한 호스트명은 결측이나 변경으로 보지 않습니다 |
| `system.os` | 그대로 비교합니다 |

## 붙여넣기 블록 (입력 화면 → Claude)

입력 화면의 [복사]·[파일로 저장]은 다음 형식의 텍스트를 만듭니다.

```
KESEKIT_PROFILE_INPUT v1
{ "meta": {…}, "system": {…}, "environment": {…}, "assessment": {…}, "notes": {…} }
END_KESEKIT_PROFILE_INPUT
```

| 키 | 내용 |
|----|------|
| `meta.projectPath` | 화면을 만들 때의 `project.path` |
| `meta.generatedAt` | 화면을 만들 때 `setup-data.js`에 넣은 `generatedAt` |
| `meta.lang` | 화면 언어 (`ko` 또는 `en`) |
| `system` | 사용자가 고칠 수 있는 값만: `osVersion`, `cpu`, `memoryGb`, `role` |
| `environment` | `languages`, `frameworks`, `services`, `webServers`, `databases`, `containers`, `cloudClis`, `aiLibraries` |
| `assessment` | `purpose`, `scope`, `domains`, `ciiTargets`, `ztTargetMaturity`, `organizationType` |
| `notes` | `common`, `start`, `check`, `fix`, `guide` |

### 붙여넣기 블록 검증

1. 시작 마커와 끝 마커 사이가 JSON 객체 하나여야 합니다. 블록이 여러 개면 마지막 블록만 씁니다.
2. `meta.projectPath`가 현재 작업 폴더와 같아야 합니다(비교 방법은 진단 규칙과 같음). 다르면 다른 프로젝트의 입력이므로 거절합니다.
3. `meta.generatedAt`이 이번에 만든 `setup-data.js`의 값과 같아야 합니다. 다르면 예전 화면에서 복사한 것이므로 새 화면에서 다시 복사해 달라고 합니다.
4. 선택지 값 표에 없는 값은 거절합니다.
5. 필수 항목 중 `system.role`과 `assessment.*` 항목(조건부 필수 포함)을 확인합니다.
6. 길이 제한: 노트는 각 2,000자, `osVersion`·`cpu`는 각 200자, 목록 항목은 각 80자이고 목록당 50개까지입니다. `memoryGb`는 0 이상의 정수 또는 `null`입니다.
7. 정의되지 않은 키는 버립니다.

## 저장 시 병합 규칙

| 필드 | 출처 |
|------|------|
| `schemaVersion` | `1` |
| `updatedAt` | 저장 시점의 시스템 시각 (ISO 8601, 시간대 포함) |
| `project.*` | 이번 탐지값 |
| `system.os`, `system.arch`, `system.hostname`, `system.remoteSession` | 이번 탐지값 |
| `system.osVersion`, `system.cpu`, `system.memoryGb`, `system.role` | 입력값 |
| `environment`, `assessment`, `notes` | 입력값 |

`meta`, `recommended`, `errors`는 저장하지 않습니다.

## 터미널 입력 템플릿 (브라우저가 없을 때)

탐지값과 기존 프로필로 `:` 뒤를 미리 채워 출력합니다. 사용자는 고친 뒤 첫 줄부터 `[END]`까지 그대로 붙여넣습니다.

```
[KESEKIT 설정 입력] ':' 뒤를 채우고 [END]까지 그대로 붙여넣으세요. 여러 값은 쉼표로 구분합니다.
장비 역할 (dev-pc | server | vm | container | other): server
점검 목적 (cii-legal | pre-deploy | code-review | zt-maturity | general | other):
점검 범위 (host, project-code, remote-systems, cloud, management): host
점검 분야 (cii, ai-security, robot-security, space-security, secure-coding, zero-trust, supply-chain): cii
CII 대상 (unix, windows, web-service, security-equip, network, control-system, pc, database, mobile, webapp, virtualization, cloud, admin, physical): unix, web-service
제로트러스트 목표 성숙도 (traditional | initial | advanced | optimal):
조직 유형 [선택] (public | cii-operator | enterprise | startup | individual | other):
OS 버전: Ubuntu 22.04.4 LTS
CPU: Intel(R) Xeon(R) Silver 4310
메모리(GB): 64
[공통 요청]:
[start 요청]:
[check 요청]:
[fix 요청]:
[guide 요청]:
[END]
```

받은 내용을 붙여넣기 블록과 같은 구조로 바꾼 뒤 "붙여넣기 블록 검증" 4~7번을 적용합니다. `environment`는 이번 탐지값을 그대로 씁니다.
