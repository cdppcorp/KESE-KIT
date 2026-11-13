# Read-Only Detection

Every command is read-only. If a command fails, keep going: set the value to `null` and add a short note to `errors`. Never run commands that need administrator privileges.

## System

| Field | Value |
|-------|-------|
| `os` | `windows`, `linux`, `macos`, `other` |
| `osVersion` | Human-readable OS name and version |
| `arch` | `x64` (AMD64, x86_64), `arm64` (ARM64, aarch64), otherwise the raw value |
| `cpu` | Model name of the first CPU |
| `memoryGb` | Total memory in GB, rounded to a whole number |
| `hostname` | Hostname |
| `remoteSession` | Whether this is an SSH or RDP session (`true`/`false`) |
| `role` | Result of "Role Inference" below |

### Windows (PowerShell)

```powershell
$os = Get-CimInstance Win32_OperatingSystem
$os.Caption; $os.Version
$os.ProductType                                   # 1 = workstation, 2 or 3 = server
$env:PROCESSOR_ARCHITECTURE                       # AMD64 / ARM64 (OSArchitecture is localized, so avoid it)
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

## Services and Tools (Names Only)

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

Never store the full service list. Record only matches for the patterns below, using the normalized names (case-insensitive).

| Pattern | Field | Recorded name |
|---------|-------|---------------|
| `nginx` / `httpd`, `apache2`, `Apache*` / `W3SVC` / `tomcat*` | `webServers` | Nginx / Apache / IIS / Tomcat |
| `mysql*`, `mariadb*` / `postgresql*`, `psql` / `MSSQL*`, `sqlcmd` / `OracleService*` / `mongod`, `MongoDB` / `redis*` | `databases` | MySQL / PostgreSQL / MSSQL / Oracle / MongoDB / Redis |
| `docker`, `com.docker.service`, `containerd` / `podman` / `kubelet`, `kubectl` | `containers` | Docker / Podman / Kubernetes |
| `aws` / `az` / `gcloud` / `terraform` | `cloudClis` | aws / az / gcloud / terraform |
| `sshd`, `ssh.service` / `WinRM` / `TermService` / `vmms` / `libvirtd` / `vmware*` | `services` | SSH / WinRM / RDP / Hyper-V / libvirt / VMware |

## Project Fingerprint

| Field | How |
|-------|-----|
| `project.path` | Absolute path of the current working directory, `/` separators |
| `project.name` | Name of the working directory |
| `project.gitRemote` | The "Git Remote" command below, which strips credentials before `@` (e.g. `user:token@` in `https://user:token@host/…`) in its own output; `null` on failure |
| `project.manifests` | Relative paths (`/` separators, sorted) of the manifest files below, found in the project root and its direct subfolders (depth 2) |

Manifest files: `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `Gemfile`, `composer.json`, `*.csproj`, `*.sln`, `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`, `Chart.yaml`, `main.tf`, `serverless.yml`, `package.xml`, `CMakeLists.txt`

Excluded folders: `node_modules`, `.git`, `vendor`, `venv`, `.venv`, `dist`, `build`, `.kesekit`

### Git Remote (Credentials Stripped)

Never run a command that prints the raw URL. Strip credentials in the command output itself:

```powershell
# Windows
(git remote get-url origin 2>$null) -replace '://[^/@]+@', '://'
```

```bash
# Linux and macOS
git remote get-url origin 2>/dev/null | sed -E 's#://[^/@]+@#://#'
```

### Manifests — Windows

```powershell
$root = (Get-Location).Path.TrimEnd('\')
$names = 'package.json','requirements.txt','pyproject.toml','Pipfile','setup.py','go.mod','Cargo.toml','pom.xml',
         'build.gradle','build.gradle.kts','Gemfile','composer.json','*.csproj','*.sln','Dockerfile',
         'docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml','Chart.yaml','main.tf',
         'serverless.yml','package.xml','CMakeLists.txt'
Get-ChildItem -Path . -Recurse -Depth 1 -File -Include $names -ErrorAction SilentlyContinue |
  ForEach-Object { $_.FullName.Substring($root.Length + 1).Replace('\', '/') } |
  Where-Object { "/$_" -notmatch '/(node_modules|\.git|vendor|venv|\.venv|dist|build|\.kesekit)/' } |
  Sort-Object -Unique
```

### Manifests — Linux and macOS

```bash
find . -maxdepth 2 -type f \( -name package.json -o -name requirements.txt -o -name pyproject.toml \
  -o -name Pipfile -o -name setup.py -o -name go.mod -o -name Cargo.toml -o -name pom.xml \
  -o -name build.gradle -o -name build.gradle.kts -o -name Gemfile -o -name composer.json \
  -o -name '*.csproj' -o -name '*.sln' -o -name Dockerfile -o -name docker-compose.yml \
  -o -name docker-compose.yaml -o -name compose.yml -o -name compose.yaml -o -name Chart.yaml \
  -o -name main.tf -o -name serverless.yml -o -name package.xml -o -name CMakeLists.txt \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/venv/*' \
  -not -path '*/.venv/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.kesekit/*' \
  | sed 's|^\./||' | LC_ALL=C sort -u
```

## Languages, Frameworks, AI Libraries

Decide by reading the manifest files only.

| Evidence | `languages` |
|----------|-------------|
| `package.json` | JavaScript (plus TypeScript if `tsconfig.json` exists) |
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python |
| `go.mod` / `Cargo.toml` / `pom.xml`, `build.gradle*` / `Gemfile` / `composer.json` / `*.csproj`, `*.sln` / `CMakeLists.txt` | Go / Rust / Java / Ruby / PHP / C# / C·C++ |

| Evidence (dependency name) | Field | Recorded name |
|----------------------------|-------|---------------|
| `express`, `next`, `react`, `vue`, `@angular/core`, `@nestjs/core`, `koa`, `fastify`, `sequelize`, `mongoose`, `prisma` | `frameworks` | Express, Next.js, React, Vue, Angular, NestJS, Koa, Fastify, Sequelize, Mongoose, Prisma |
| `django`, `flask`, `fastapi`, `sqlalchemy` | `frameworks` | Django, Flask, FastAPI, SQLAlchemy |
| `catkin` or `ament` in `package.xml` | `frameworks` | ROS |
| `torch`, `tensorflow`, `@tensorflow/tfjs`, `keras`, `transformers`, `scikit-learn`, `openai`, `anthropic`, `@anthropic-ai/sdk`, `langchain`, `llama-index`, `onnxruntime`, `ultralytics` | `aiLibraries` | Package name as-is |
| `Dockerfile`, compose files / `Chart.yaml` | `containers` | Docker / Kubernetes |
| `main.tf` / `serverless.yml` | `cloudClis` | terraform / serverless |

## Role Inference (`system.role`)

Use the first rule that matches. This is only a guess; the user confirms it in the form.

1. Linux with `/.dockerenv`, or `docker`/`kubepods` in `/proc/1/cgroup` → `container`
2. Windows `ProductType` 2 or 3, or Linux with no `DISPLAY`/`WAYLAND_DISPLAY` over a remote session → `server`
3. Linux `systemd-detect-virt --vm` returns something other than `none` → `vm`
4. Otherwise → `dev-pc`

## Domain Suggestions (`recommended`)

| Condition | Add to `domains` | Add to `ciiTargets` |
|-----------|------------------|---------------------|
| `role` is `server` or `vm` | `cii` | `windows` on Windows, otherwise `unix` |
| `webServers` is not empty | `cii` | `web-service` |
| `databases` is not empty | `cii` | `database` |
| `cloudClis` is not empty | `cii` | `cloud` |
| `services` includes Hyper-V, libvirt, or VMware | `cii` | `virtualization` |
| `cii` is suggested and a web framework (Express, NestJS, Koa, Fastify, Next.js, Django, Flask, FastAPI) exists | — | `webapp` |
| `languages` includes JavaScript, TypeScript, or Python | `secure-coding` | — |
| `manifests` has at least one file | `supply-chain` | — |
| `aiLibraries` is not empty | `ai-security` | — |
| `frameworks` includes ROS | `robot-security` | — |

Never suggest `space-security` or `zero-trust`; those are organization-level decisions. Remove duplicates and sort in the Allowed Values order of `profile-schema.md`.

## Browser Availability

Treat the browser as unavailable, and use the terminal input template, if any of these holds:

- The `SSH_CONNECTION` environment variable is set (remote session)
- On Linux, both `DISPLAY` and `WAYLAND_DISPLAY` are empty
- The command that opens the browser fails

## Date Math

- Current time (`updatedAt`, `generatedAt`): Windows `Get-Date -Format o`, Linux/macOS `date +%Y-%m-%dT%H:%M:%S%z`
- Elapsed days: use the date part (`YYYY-MM-DD`) of `updatedAt`.

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
