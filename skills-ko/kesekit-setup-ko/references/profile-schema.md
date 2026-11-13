# KESE 프로필 스키마

## 파일

| 경로 | 설명 |
|------|------|
| `.kesekit/profile.json` | 저장된 프로필. 모든 kesekit 스킬이 0단계에서 읽습니다 |
| `.kesekit/setup.html`, `.kesekit/setup-form.js`, `.kesekit/setup-i18n.js` | 입력 화면, 화면 동작, 화면 문구 (임시, 저장에 성공하면 삭제) |
| `.kesekit/setup-data.js` | 입력 화면에 넘기는 탐지 결과 (임시, 저장에 성공하면 삭제) |

`.kesekit/`은 Claude Code를 실행한 작업 폴더 안에 만듭니다. 점검 대상 프로젝트(`project.path`)는 기본적으로 작업 폴더와 같지만, 사용자가 입력 화면에서 바꿀 수 있습니다. 호스트명 같은 환경 정보가 들어가므로 `.kesekit/`은 Git에 올리지 않습니다.

## profile.json 구조

```json
{
  "schemaVersion": 1,
  "updatedAt": "2026-11-14T15:20:00+09:00",
  "project": {
    "path": "C:/work/shop-api",
    "name": "shop-api",
    "gitRemote": "https://github.com/acme/shop-api.git",
    "gitRemoteEdited": false,
    "workspace": "C:/work/shop-api",
    "fingerprint": {
      "gitRemote": "https://github.com/acme/shop-api.git",
      "manifests": ["Dockerfile", "package.json"]
    }
  },
  "system": {
    "os": "windows",
    "osVersion": "Windows 11 Pro 10.0.26200",
    "arch": "x64",
    "cpu": "Intel(R) Core(TM) i7-1360P",
    "memoryGb": 32,
    "hostname": "DEV-PC01",
    "role": "dev-pc",
    "roleEdited": false,
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
  "environmentSource": {
    "languages": "auto", "frameworks": "manual", "services": "auto", "webServers": "auto",
    "databases": "auto", "containers": "auto", "cloudClis": "auto", "aiLibraries": "auto"
  },
  "assessment": {
    "purpose": "other",
    "scope": ["host", "project-code"],
    "domains": ["secure-coding", "supply-chain"],
    "ciiTargets": [],
    "ztTargetMaturity": null,
    "organizationType": "startup",
    "source": {
      "purpose": "custom",
      "scope": "recommended",
      "domains": "recommended",
      "ciiTargets": null,
      "ztTargetMaturity": null,
      "organizationType": "selected"
    },
    "custom": {
      "purpose": "ISMS-P 인증 심사 전에 자체 점검",
      "scope": "",
      "domains": "",
      "ciiTargets": "",
      "ztTargetMaturity": "",
      "organizationType": ""
    }
  },
  "notes": {
    "common": "",
    "start": "",
    "check": "결과를 PR에 붙일 수 있게 마크다운 표로 정리",
    "fix": "스크립트는 만들기만 하고 적용하지 않음",
    "guide": "",
    "advisory": ""
  }
}
```

| 필드 | 뜻 |
|------|----|
| `project.path` | 점검 대상 프로젝트의 절대 경로. 기본값은 작업 폴더이며 사용자가 바꿀 수 있습니다 |
| `project.gitRemote` | 보고서에 쓰는 Git 원격 주소(자격 증명 제거). `project.gitRemoteEdited`가 `true`면 사용자가 직접 고친 값입니다 |
| `project.workspace` | 프로필을 저장한 작업 폴더. 프로필이 다른 폴더로 복사·이동됐는지 판단하는 데 씁니다 |
| `project.fingerprint` | `project.path`에서 탐지한 Git 원격 주소와 구성 파일 목록. 변경 감지에만 씁니다 |
| `system.roleEdited` | `true`면 사용자가 장비 역할을 직접 골랐습니다. `false`면 탐지값이며 다음 실행 때 새 탐지값을 따릅니다 |
| `environmentSource` | 환경 목록별 출처: `auto`(자동 분석, 저장할 때 Claude가 `project.path`에서 다시 탐지) 또는 `manual`(사용자가 직접 고름) |
| `assessment.source` | 점검 설정 값의 출처: `selected`(사용자가 고름), `custom`(직접 입력을 Claude가 해석), `recommended`(비워 둬서 추천값 사용), `null`(해당 없음) |
| `assessment.custom` | 항목별 직접 입력 원문. 선택값이 있어도 함께 보관하며, 스킬이 사용자 설명으로 참고합니다 |

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
- 환경 목록(`environment.*`)의 기본 선택지는 `templates/setup-form.html`의 `kesekit-detect`에 있으며 `references/detection.md`의 기록 이름과 같습니다. 목록에 없는 값도 사용자가 추가할 수 있습니다.

## 필수 항목

다음 중 하나라도 없거나 비어 있으면 `INCOMPLETE`입니다.

- `schemaVersion`(= 1), `updatedAt`
- `project.path`, `project.workspace`
- `system.os`, `system.role`
- `assessment.purpose`, `assessment.scope`(1개 이상), `assessment.domains`(1개 이상)
- `assessment.domains`에 `cii`가 있으면 `assessment.ciiTargets`(1개 이상)
- `assessment.domains`에 `zero-trust`가 있으면 `assessment.ztTargetMaturity`
- 선택지 값 표에 없는 값이 들어 있어도 결측으로 봅니다

`assessment.organizationType`은 선택 사항입니다. 사용자가 비워 둔 항목은 저장 전에 추천값으로 채우고, 추천값도 비지 않게 만들기 때문에(`references/detection.md`의 "추천 분야") 정상적으로 저장된 프로필은 결측이 생기지 않습니다.

## 진단 규칙

| 코드 | 조건 |
|------|------|
| `MISSING` | 파일이 없거나, JSON으로 읽을 수 없거나, `schemaVersion`이 1이 아님. 이 경우 다른 코드는 보지 않습니다 |
| `INCOMPLETE` | 필수 항목 결측 |
| `STALE` | 오늘 날짜 − `updatedAt` 날짜 ≥ 14일 |
| `CHANGED` | 아래 비교 항목 중 하나라도 다름 |
| `MANUAL` | 위 코드에 해당하지 않지만 사용자가 setup을 직접 실행함 |

`MISSING`·`INCOMPLETE`·`STALE`·`CHANGED`가 하나도 없으면 OK입니다. 여러 코드가 동시에 해당하면 모두 `reasons`에 넣습니다.

**경로 비교 방법**: 두 경로 모두 구분자를 `/`로 바꾸고 끝의 `/`를 지운 뒤 비교합니다. Windows에서는 대소문자를 무시합니다. 이 문서와 SKILL.md에서 "경로가 같다"는 모두 이 방법을 뜻합니다.

변경 비교는 아래 순서로 합니다. 앞 단계에서 `CHANGED`가 나오면 저장된 경로로 명령을 실행하지 않고 멈춥니다.

| 순서 | 항목 | 비교 방법 |
|:---:|------|-----------|
| 1 | `project.workspace` | 현재 작업 폴더와 같지 않으면 `CHANGED`. 다른 곳에서 복사된 프로필일 수 있으므로 그 안의 경로로는 명령을 실행하지 않습니다 |
| 2 | `project.path` | `references/detection.md`의 "경로 안전 규칙"을 통과하지 못하거나 그 폴더가 없으면 `CHANGED` |
| 3 | `project.fingerprint.gitRemote` | `project.path`에서 다시 얻은 `origin` 주소(자격 증명 제거)와 비교합니다. 둘 다 없으면 같은 것으로 봅니다 |
| 3 | `project.fingerprint.manifests` | `project.path`에서 다시 찾은 구성 파일 목록과 집합으로 비교합니다(순서 무관) |
| 3 | `system.hostname` | 저장값과 현재값이 둘 다 있을 때만 대소문자를 무시하고 비교합니다. 탐지하지 못한 호스트명은 결측이나 변경으로 보지 않습니다 |
| 3 | `system.os` | 그대로 비교합니다 |

사용자가 고친 `project.gitRemote`는 비교하지 않습니다. 변경 감지는 탐지값인 `project.fingerprint`로만 합니다.

## 붙여넣기 블록 (입력 화면 → Claude)

입력 화면의 [복사]·[파일로 저장]은 다음 형식의 텍스트를 만듭니다.

```
KESEKIT_PROFILE_INPUT v1
{ "meta": {…}, "project": {…}, "system": {…}, "environment": {…}, "environmentSource": {…}, "assessment": {…}, "notes": {…} }
END_KESEKIT_PROFILE_INPUT
```

| 키 | 내용 |
|----|------|
| `meta.projectPath` | 화면을 만들 때 탐지한 `project.path` |
| `meta.generatedAt` | 화면을 만들 때 `setup-data.js`에 넣은 `generatedAt` |
| `meta.lang` | 화면 언어 (`ko` 또는 `en`) |
| `project` | `path`, `gitRemote`, `gitRemoteEdited`, `picked` |
| `project.picked` | [폴더 선택]으로 고른 경우만: `{ "name": 폴더 이름, "manifests": [구성 파일] }`. 이때 `path`는 전체 경로가 아니라 폴더 이름입니다. 고르지 않았으면 `null` |
| `system` | 사용자가 고칠 수 있는 값만: `osVersion`, `cpu`, `memoryGb`, `role`, `roleEdited` |
| `environment` | `languages`, `frameworks`, `services`, `webServers`, `databases`, `containers`, `cloudClis`, `aiLibraries` |
| `environmentSource` | 위 8개 목록 각각의 `auto` 또는 `manual` |
| `assessment` | `purpose`, `scope`, `domains`, `ciiTargets`, `ztTargetMaturity`, `organizationType`, `source`, `custom` |
| `notes` | `common`, `start`, `check`, `fix`, `guide`, `advisory` |

입력 화면은 점검 설정 항목마다 **선택한 값 → 직접 입력 → 추천값** 순서로 값을 정합니다. 직접 입력만 있는 항목은 값이 `null`이고 `source`가 `custom`입니다. 이 값은 Claude가 "입력값 확정"에서 채웁니다.

### 붙여넣기 블록 검증

1. 시작 마커와 끝 마커 사이가 JSON 객체 하나여야 합니다. 블록이 여러 개면 마지막 블록만 씁니다.
2. `meta.projectPath`가 이번에 만든 `setup-data.js`의 `detected.project.path`와 같아야 합니다. 다르면 다른 화면에서 복사한 것이므로 거절합니다.
3. `meta.generatedAt`이 이번에 만든 `setup-data.js`의 값과 같아야 합니다. 다르면 예전 화면에서 복사한 것이므로 새 화면에서 다시 복사해 달라고 합니다.
4. 선택지 값 표에 없는 값은 거절합니다. `null`은 `source`가 `custom`이거나 `null`인 항목, 그리고 `organizationType`에서만 허용합니다.
5. `assessment.source` 값은 `selected`, `custom`, `recommended`, `null` 중 하나여야 하고, `custom`이면 같은 키의 `assessment.custom` 원문이 비어 있으면 안 됩니다. `environmentSource` 값은 `auto` 또는 `manual`이어야 합니다.
6. `project.path`는 `references/detection.md`의 "경로 안전 규칙"을 통과해야 하고 500자 이하여야 합니다. 절대 경로가 아니면 `project.picked`가 있고 `project.picked.name`과 같아야 합니다(폴더 이름 규칙 적용). `project.gitRemote`는 `null`이거나 `https://…`, `ssh://…`, `git@호스트:경로` 형식이고 300자 이하여야 합니다. 저장 전에 자격 증명과 `?`·`#` 뒤를 한 번 더 지웁니다.
7. 길이 제한: 노트는 각 2,000자, 직접 입력은 각 300자, `osVersion`·`cpu`는 각 200자, 목록 항목은 각 80자이고 목록당 50개까지입니다. `memoryGb`는 0 이상의 정수 또는 `null`이고, `system.role`은 선택지 값이어야 합니다.
8. 정의되지 않은 키는 버립니다.

### 입력값 확정

검증을 통과하면 저장하기 전에 다음 순서로 값을 확정합니다.

1. `project.path`가 `meta.projectPath`와 다르면 SKILL.md 4단계의 "프로젝트 변경" 절차를 먼저 따릅니다.
2. `source`가 `custom`이고 값이 `null`인 항목은 `assessment.custom`의 원문을 읽어 선택지 값으로 바꿉니다. 바꿀 수 없으면 `setup-data.js`의 추천값을 쓰고 `source`를 `recommended`로 바꾼 뒤, 요약에서 그렇게 처리했다고 알립니다.
3. 분야가 정해진 뒤 `cii`가 없으면 `ciiTargets`를 `[]`, `zero-trust`가 없으면 `ztTargetMaturity`를 `null`로 하고 각 `source`를 `null`로 둡니다. 반대로 분야는 있는데 값이 비어 있으면 추천값을 넣고 `source`를 `recommended`로 둡니다. 추천값마저 비어 있으면 `references/detection.md`의 대체값(`ciiTargets`는 `pc`/`windows`/`unix`, `ztTargetMaturity`는 `initial`)을 씁니다.
4. `environmentSource`가 `auto`인 목록은 `project.path`에서 이번에 탐지한 값으로 바꿉니다. `manual`인 목록은 입력값을 그대로 씁니다.
5. `assessment.custom` 원문은 값이 정해졌어도 그대로 저장합니다.

## 저장 시 병합 규칙

| 필드 | 출처 |
|------|------|
| `schemaVersion` | `1` |
| `updatedAt` | 저장 시점의 시스템 시각 (ISO 8601, 시간대 포함) |
| `project.path`, `project.gitRemote`, `project.gitRemoteEdited` | 입력값 (경로는 확정된 절대 경로, Git 주소는 자격 증명 제거) |
| `project.name` | `project.path`의 폴더 이름 |
| `project.workspace` | 현재 작업 폴더 |
| `project.fingerprint` | `project.path`에서 이번에 탐지한 Git 원격 주소와 구성 파일 목록 |
| `system.os`, `system.arch`, `system.hostname`, `system.remoteSession` | 이번 탐지값 (`os`는 실패해도 `other`) |
| `system.osVersion`, `system.cpu`, `system.memoryGb`, `system.role`, `system.roleEdited` | 입력값 |
| `environment`, `environmentSource` | "입력값 확정" 4번을 거친 값 |
| `notes` | 입력값 |
| `assessment` | "입력값 확정"을 거친 값과 `source`, `custom` |

`meta`, `project.picked`, `recommended`, `errors`는 저장하지 않습니다.

## 터미널 입력 템플릿 (브라우저가 없을 때)

탐지값과 기존 프로필로 미리 채우고, 대괄호 안에 추천값을 적어 출력합니다. 사용자는 고친 뒤 첫 줄부터 `[END]`까지 그대로 붙여넣습니다.

```
[KESEKIT 설정 입력] ':' 뒤를 채우고 [END]까지 그대로 붙여넣으세요.
비워 두면 [추천] 값으로 진행합니다. 선택지에 없는 내용은 자유롭게 적으면 Claude가 해석합니다. 여러 값은 쉼표로 구분합니다.
점검 프로젝트 경로: /srv/shop-api
Git 원격 주소: https://github.com/acme/shop-api.git
장비 역할 (dev-pc | server | vm | container | other) [추천: server]:
점검 목적 (cii-legal | pre-deploy | code-review | zt-maturity | general | other) [추천: pre-deploy]:
점검 범위 (host, project-code, remote-systems, cloud, management) [추천: host, project-code]:
점검 분야 (cii, ai-security, robot-security, space-security, secure-coding, zero-trust, supply-chain) [추천: cii, secure-coding]:
CII 대상 (unix, windows, web-service, security-equip, network, control-system, pc, database, mobile, webapp, virtualization, cloud, admin, physical) [추천: unix, web-service]:
제로트러스트 목표 성숙도 (traditional | initial | advanced | optimal) [추천: initial]:
조직 유형 (public | cii-operator | enterprise | startup | individual | other) [선택 사항]:
OS 버전: Ubuntu 22.04.4 LTS
CPU: Intel(R) Xeon(R) Silver 4310
메모리(GB): 64
[공통 요청]:
[start 요청]:
[check 요청]:
[fix 요청]:
[guide 요청]:
[advisory 요청]:
[END]
```

받은 내용은 다음처럼 처리합니다.

1. **경로가 바뀌었으면**: 경로 안전 규칙을 확인하고 폴더가 있는지 본 뒤, 그 경로에서 프로젝트를 다시 탐지하고 추천값을 다시 계산합니다. 사용자가 적은 답을 유지한 채 새 탐지값으로 템플릿을 다시 출력하고, 다시 붙여넣어 달라고 합니다.
2. 각 항목은 선택지 값이면 `selected`, 자유 서술이면 `custom`(원문은 `assessment.custom`에 보관), 비어 있으면 그 자리에 추천값을 넣고 `recommended`로 둡니다. 장비 역할을 비워 두면 탐지값을 쓰고 `roleEdited`는 `false`입니다. Git 주소가 탐지값과 다르면 `gitRemoteEdited`는 `true`입니다.
3. `environmentSource`는 모두 `auto`로 둡니다.
4. "붙여넣기 블록 검증" 4~8번과 "입력값 확정" 2~5번을 적용합니다.
