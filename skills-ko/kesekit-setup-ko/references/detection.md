# 읽기 전용 탐지

모든 명령은 읽기 전용입니다. 명령이 실패해도 멈추지 말고 해당 값을 `null`로 둔 뒤 `errors`에 짧게 적습니다. 단 `system.os`는 `null`로 두지 않고, 판단할 수 없으면 `other`로 둡니다. 관리자 권한이 필요한 명령은 실행하지 않습니다.

## 경로 안전 규칙

명령에 넣는 모든 경로(`<경로>`)와 폴더 이름(`<폴더 이름>`)은 먼저 이 규칙을 통과해야 합니다. 통과하지 못한 값으로는 명령을 실행하지 않습니다.

- 경로는 이 PC의 절대 경로여야 합니다. `C:\…`·`C:/…` 같은 드라이브 경로나 `/`로 시작하는 경로만 허용합니다. `\\서버\…`·`//서버/…` 같은 네트워크(UNC) 경로는 쓰지 않습니다(접근하는 순간 Windows 인증 정보가 넘어갈 수 있음).
- 작은따옴표(`'`), 큰따옴표(`"`), 백틱(`` ` ``), 줄바꿈 같은 제어 문자가 있으면 안 됩니다. 명령에서는 값을 항상 작은따옴표로 감쌉니다.
- 폴더 이름에는 `*`, `?`, `[`, `]`, `/`, `\`도 있으면 안 됩니다.
- 기존 프로필에서 읽은 경로는 그 프로필의 `project.workspace`가 현재 작업 폴더와 같은 경로일 때만 씁니다(`profile-schema.md`의 경로 비교 방법). 다른 곳에서 복사된 프로필의 경로로는 명령을 실행하지 않습니다.

## 시스템

| 필드 | 값 |
|------|----|
| `os` | `windows`, `linux`, `macos`, `other` |
| `osVersion` | 사람이 읽는 OS 이름과 버전 |
| `arch` | `x64`(AMD64·x86_64), `arm64`(ARM64·aarch64), 그 외는 원래 값 |
| `cpu` | 첫 번째 CPU 모델명 |
| `memoryGb` | 전체 메모리(GB, 반올림한 정수) |
| `hostname` | 호스트명 |
| `remoteSession` | SSH·RDP 원격 접속 여부 (`true`/`false`) |
| `role` | 아래 "장비 역할 추정" 결과 |

### Windows (PowerShell)

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$os.Caption; $os.Version
$os.ProductType                                   # 1 = 워크스테이션, 2·3 = 서버
$env:PROCESSOR_ARCHITECTURE                       # AMD64 / ARM64 (OSArchitecture는 언어별로 달라서 쓰지 않음)
(Get-CimInstance Win32_Processor | Select-Object -First 1).Name
[math]::Round((Get-CimInstance Win32_ComputerSystem).TotalPhysicalMemory / 1GB)
$env:COMPUTERNAME
[bool]$env:SSH_CONNECTION -or ($env:SESSIONNAME -like 'RDP-*')
```

### Linux

```bash
grep '^PRETTY_NAME=' /etc/os-release 2>/dev/null | cut -d= -f2- | tr -d '"'
uname -m
uname -n
grep -m1 'model name' /proc/cpuinfo | cut -d: -f2- | sed 's/^ *//'
awk '/MemTotal/ {printf "%d\n", $2/1048576 + 0.5}' /proc/meminfo
[ -n "$SSH_CONNECTION" ] && echo remote || echo local
```

### macOS

```bash
echo "$(sw_vers -productName) $(sw_vers -productVersion)"
uname -m
scutil --get LocalHostName 2>/dev/null || uname -n
sysctl -n machdep.cpu.brand_string
echo $(( $(sysctl -n hw.memsize) / 1073741824 ))
[ -n "$SSH_CONNECTION" ] && echo remote || echo local
```

## 서비스·도구 (이름만)

### Windows

```powershell
Get-Service | Where-Object Status -eq 'Running' | Select-Object -ExpandProperty Name
foreach ($c in 'docker','podman','kubectl','aws','az','gcloud','terraform','nginx','httpd','mysql','psql','sqlcmd','mongod','redis-server') {
  if (Get-Command $c -ErrorAction SilentlyContinue) { $c }
}
```

### Linux

```bash
systemctl list-units --type=service --state=running --no-pager --no-legend 2>/dev/null | awk '{print $1}'
for c in docker podman kubectl aws az gcloud terraform nginx httpd apache2 mysql psql mongod redis-server; do
  command -v "$c" >/dev/null 2>&1 && echo "$c"
done
```

### macOS

```bash
launchctl list 2>/dev/null | awk 'NR>1 {print $3}'
for c in docker podman kubectl aws az gcloud terraform nginx httpd mysql psql mongod redis-server; do
  command -v "$c" >/dev/null 2>&1 && echo "$c"
done
```

서비스 전체 목록은 저장하지 않습니다. 아래 패턴에 맞는 것만 정리된 이름으로 기록합니다(대소문자 무시).

| 패턴 | 필드 | 기록할 이름 |
|------|------|-------------|
| `nginx` / `httpd`, `apache2`, `Apache*` / `W3SVC` / `tomcat*` | `webServers` | Nginx / Apache / IIS / Tomcat |
| `mysql*`, `mariadb*` / `postgresql*`, `psql` / `MSSQL*`, `sqlcmd` / `OracleService*` / `mongod`, `MongoDB` / `redis*` | `databases` | MySQL / PostgreSQL / MSSQL / Oracle / MongoDB / Redis |
| `docker`, `com.docker.service`, `containerd` / `podman` / `kubelet`, `kubectl` | `containers` | Docker / Podman / Kubernetes |
| `aws` / `az` / `gcloud` / `terraform` | `cloudClis` | aws / az / gcloud / terraform |
| `sshd`, `ssh.service` / `WinRM` / `TermService` / `vmms` / `libvirtd` / `vmware*` | `services` | SSH / WinRM / RDP / Hyper-V / libvirt / VMware |

## 프로젝트 지문

| 필드 | 방법 |
|------|------|
| `project.path` | 아래 "점검 대상 경로 정하기"로 정한 절대 경로, 구분자 `/` |
| `project.name` | 점검 대상 폴더 이름 |
| `project.gitRemote` | 아래 "Git 원격 주소" 명령. `https://user:token@host/…`의 `user:token@`처럼 `@` 앞 자격 증명과 `?`·`#` 뒤를 출력 단계에서 지웁니다. 실패하면 `null` |
| `project.manifests` | 아래 구성 파일을 프로젝트 루트와 바로 아래 하위 폴더(깊이 2)에서 찾은 상대 경로 목록(`/` 구분, 정렬) |

구성 파일: `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `Gemfile`, `composer.json`, `*.csproj`, `*.sln`, `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`, `Chart.yaml`, `main.tf`, `serverless.yml`, `package.xml`, `CMakeLists.txt`

제외 폴더: `node_modules`, `.git`, `vendor`, `venv`, `.venv`, `dist`, `build`, `.kesekit`

### 점검 대상 경로 정하기

1. 사용자가 입력 화면에서 경로를 바꿔 보냈으면 그 경로를 씁니다(SKILL.md 4단계 "프로젝트 변경").
2. 아니면, 기존 프로필의 `project.workspace`가 현재 작업 폴더와 같은 경로이고, 그 `project.path`가 경로 안전 규칙을 통과하며 폴더가 아직 있으면 그 경로를 씁니다.
3. 둘 다 아니면 현재 작업 폴더를 씁니다.

아래 명령의 `<경로>`는 이렇게 정한 점검 대상 경로입니다.

### 폴더 이름으로 경로 찾기

입력 화면의 [폴더 선택]으로 고르면 브라우저는 보안상 전체 경로를 주지 않고 폴더 이름(`project.picked.name`)과 구성 파일 목록(`project.picked.manifests`)만 보냅니다. 폴더 이름이 경로 안전 규칙을 통과하면 아래 위치에서 같은 이름의 폴더를 찾습니다.

```powershell
# Windows: 작업 폴더의 상위 폴더, 사용자 폴더, 로컬 고정 드라이브 루트
$name = '<폴더 이름>'
$skip = '\\(node_modules|\.git|AppData|\$Recycle\.Bin|Windows|Program Files[^\\]*|ProgramData)\\'
$roots = @(@{ Path = (Split-Path -Parent (Get-Location).Path); Depth = 2 }, @{ Path = $env:USERPROFILE; Depth = 4 }) +
  @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object { @{ Path = $_.DeviceID + '\'; Depth = 2 } })
foreach ($r in $roots) {
  Get-ChildItem -LiteralPath $r.Path -Directory -Recurse -Depth $r.Depth -Filter $name -ErrorAction SilentlyContinue |
    Where-Object { "$($_.FullName)\" -notmatch $skip } | Select-Object -ExpandProperty FullName
}
```

```bash
# Linux·macOS
name='<폴더 이름>'
for root in "$(dirname "$PWD")" "$HOME"; do
  find "$root" -maxdepth 5 -type d -name "$name" -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/Library/*' 2>/dev/null
done | LC_ALL=C sort -u
```

찾은 후보마다 "구성 파일" 명령으로 목록을 구해 `project.picked.manifests`와 집합으로 비교합니다.

- 정확히 하나가 일치하면 그 경로를 쓰고, 요약에 찾은 경로를 보여 줍니다.
- 여러 개가 일치하면 후보 경로를 보여 주고 사용자에게 고르게 합니다.
- 하나도 없으면 전체 경로를 붙여 넣어 달라고 합니다(탐색기에서 폴더 우클릭 → '경로로 복사').

### Git 원격 주소 (자격 증명 제거)

원본 주소를 출력하는 명령은 쓰지 않습니다. 아래처럼 출력 단계에서 바로 지웁니다.

```powershell
# Windows
((git -C '<경로>' remote get-url origin 2>$null) -replace '://[^/\s]*@', '://') -replace '[?#].*$', ''
```

```bash
# Linux·macOS
git -C '<경로>' remote get-url origin 2>/dev/null | sed -E 's|://[^/[:space:]]*@|://|; s|[?#].*$||'
```

### 구성 파일 — Windows

```powershell
$root = (Resolve-Path -LiteralPath '<경로>').Path.TrimEnd('\')
$names = 'package.json','requirements.txt','pyproject.toml','Pipfile','setup.py','go.mod','Cargo.toml','pom.xml',
         'build.gradle','build.gradle.kts','Gemfile','composer.json','*.csproj','*.sln','Dockerfile',
         'docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml','Chart.yaml','main.tf',
         'serverless.yml','package.xml','CMakeLists.txt'
Get-ChildItem -LiteralPath $root -Recurse -Depth 1 -File -Include $names -ErrorAction SilentlyContinue |
  ForEach-Object { $_.FullName.Substring($root.Length + 1).Replace('\', '/') } |
  Where-Object { "/$_" -notmatch '/(node_modules|\.git|vendor|venv|\.venv|dist|build|\.kesekit)/' } |
  Sort-Object -Unique
```

### 구성 파일 — Linux·macOS

```bash
(cd '<경로>' && find . -maxdepth 2 -type f \( -name package.json -o -name requirements.txt -o -name pyproject.toml \
  -o -name Pipfile -o -name setup.py -o -name go.mod -o -name Cargo.toml -o -name pom.xml \
  -o -name build.gradle -o -name build.gradle.kts -o -name Gemfile -o -name composer.json \
  -o -name '*.csproj' -o -name '*.sln' -o -name Dockerfile -o -name docker-compose.yml \
  -o -name docker-compose.yaml -o -name compose.yml -o -name compose.yaml -o -name Chart.yaml \
  -o -name main.tf -o -name serverless.yml -o -name package.xml -o -name CMakeLists.txt \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/venv/*' \
  -not -path '*/.venv/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.kesekit/*' \
  | sed 's|^\./||' | LC_ALL=C sort -u)
```

## 언어·프레임워크·AI 라이브러리

찾은 구성 파일을 읽기만 해서 판단합니다.

| 근거 | `languages` |
|------|-------------|
| `package.json` | JavaScript (`tsconfig.json`이 있으면 TypeScript도) |
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python |
| `go.mod` / `Cargo.toml` / `pom.xml`, `build.gradle*` / `Gemfile` / `composer.json` / `*.csproj`, `*.sln` / `CMakeLists.txt` | Go / Rust / Java / Ruby / PHP / C# / C/C++ |

| 근거 (의존성 이름) | 필드 | 기록할 이름 |
|--------------------|------|-------------|
| `express`, `next`, `react`, `vue`, `@angular/core`, `@nestjs/core`, `koa`, `fastify`, `sequelize`, `mongoose`, `prisma` | `frameworks` | Express, Next.js, React, Vue, Angular, NestJS, Koa, Fastify, Sequelize, Mongoose, Prisma |
| `django`, `flask`, `fastapi`, `sqlalchemy` | `frameworks` | Django, Flask, FastAPI, SQLAlchemy |
| `package.xml`에 `catkin` 또는 `ament` | `frameworks` | ROS |
| `torch`, `tensorflow`, `@tensorflow/tfjs`, `keras`, `transformers`, `scikit-learn`, `openai`, `anthropic`, `@anthropic-ai/sdk`, `langchain`, `llama-index`, `onnxruntime`, `ultralytics` | `aiLibraries` | 패키지 이름 그대로 |
| `Dockerfile`, compose 파일 / `Chart.yaml` | `containers` | Docker / Kubernetes |
| `main.tf` / `serverless.yml` | `cloudClis` | terraform / serverless |

## 장비 역할 추정 (`system.role`)

위에서부터 처음 맞는 것을 씁니다. 추정값일 뿐이며 사용자가 입력 화면에서 확인합니다.

1. Linux에서 `/.dockerenv`가 있거나 `/proc/1/cgroup`에 `docker`·`kubepods`가 있음 → `container`
2. Windows `ProductType`이 2 또는 3, 또는 Linux에서 `DISPLAY`·`WAYLAND_DISPLAY`가 없고 원격 접속 중 → `server`
3. Linux `systemd-detect-virt --vm` 결과가 `none`이 아님 → `vm`
4. 그 외 → `dev-pc`

## 추천 분야 (`recommended`)

| 조건 | `domains`에 추가 | `ciiTargets`에 추가 |
|------|------------------|---------------------|
| `role`이 `server` 또는 `vm` | `cii` | OS가 Windows면 `windows`, 아니면 `unix` |
| `webServers`가 있음 | `cii` | `web-service` |
| `databases`가 있음 | `cii` | `database` |
| `cloudClis`가 있음 | `cii` | `cloud` |
| `services`에 Hyper-V·libvirt·VMware | `cii` | `virtualization` |
| `cii`를 추천했고 웹 프레임워크(Express, NestJS, Koa, Fastify, Next.js, Django, Flask, FastAPI)가 있음 | — | `webapp` |
| `languages`에 JavaScript·TypeScript·Python | `secure-coding` | — |
| `manifests`가 1개 이상 | `supply-chain` | — |
| `aiLibraries`가 있음 | `ai-security` | — |
| `frameworks`에 ROS | `robot-security` | — |

`space-security`와 `zero-trust`는 조직 차원에서 정할 일이므로 추천하지 않습니다. 중복을 지우고 `profile-schema.md`의 선택지 값 순서로 정렬합니다.

위 규칙으로 `domains`가 비면 `cii`를 넣습니다. `ciiTargets`는 `cii`를 추천했는지와 상관없이 항상 채웁니다(사용자가 나중에 CII를 고를 수 있으므로). 규칙에서 나온 값이 없으면 대체값으로 `role`이 `dev-pc`면 `pc`, 아니면 OS에 따라 `windows` 또는 `unix`를 씁니다.

나머지 항목의 추천값입니다. 사용자가 입력 화면에서 비워 둔 항목은 이 값으로 진행합니다.

| 항목 | 추천값 |
|------|--------|
| `purpose` | 구성 파일이 1개 이상이면 `pre-deploy`, 아니면 `general` |
| `scope` | 구성 파일이 있으면 `project-code`, `role`이 `dev-pc`가 아니거나 `webServers`·`databases`·`services`가 있으면 `host`, `cloudClis`가 있으면 `cloud`. 하나도 없으면 `host` |
| `ztTargetMaturity` | `initial` (제로트러스트를 고른 경우에만 씀) |
| `organizationType` | 추천하지 않음 (비워 두면 지정 안 함) |
| `role` | 위 "장비 역할 추정" 결과 |

`setup-data.js`의 `detected.recommended`에는 `purpose`, `scope`, `domains`, `ciiTargets`, `ztTargetMaturity`를 모두 넣고, 어느 것도 비워 두지 않습니다.

## 브라우저 사용 가능 여부

다음 중 하나라도 해당하면 브라우저를 쓸 수 없다고 보고 터미널 입력 템플릿을 씁니다.

- `SSH_CONNECTION` 환경변수가 있음 (원격 접속)
- Linux에서 `DISPLAY`와 `WAYLAND_DISPLAY`가 모두 비어 있음
- 브라우저 열기 명령이 실패함

## 날짜 계산

- 현재 시각(`updatedAt`, `generatedAt`): Windows `Get-Date -Format o`, Linux·macOS `date +%Y-%m-%dT%H:%M:%S%z`
- 경과 일수: `updatedAt`의 날짜 부분(`YYYY-MM-DD`)으로 계산합니다.

```powershell
# Windows
((Get-Date).Date - [datetime]::ParseExact('2026-10-29', 'yyyy-MM-dd', $null)).Days
```

```bash
# Linux
echo $(( ( $(date +%s) - $(date -d 2026-10-29 +%s) ) / 86400 ))
# macOS
echo $(( ( $(date +%s) - $(date -j -f %Y-%m-%d 2026-10-29 +%s) ) / 86400 ))
```
