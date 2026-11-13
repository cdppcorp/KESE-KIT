# Read-Only Detection

Every command is read-only. If a command fails, keep going: set the value to `null` and add a short note to `errors`. The one exception is `system.os`: never leave it `null`; use `other` when it cannot be determined. Never run commands that need administrator privileges.

## Path Safety Rules

Every path (`<path>`) and folder name (`<folder name>`) placed in a command must pass these rules first. Never run a command with a value that fails them.

- Paths must be absolute paths on this machine: a drive path such as `C:\…` or `C:/…`, or a path starting with `/`. Never use network (UNC) paths such as `\\server\…` or `//server/…`; touching them can send Windows credentials to that server.
- No single quotes (`'`), double quotes (`"`), backticks (`` ` ``), or control characters such as newlines. Always wrap the value in single quotes in commands.
- Folder names also must not contain `*`, `?`, `[`, `]`, `/`, or `\`.
- Use a path read from an existing profile only when that profile's `project.workspace` is the same path as the current working directory (path comparison in `profile-schema.md`). Never run commands on paths from a profile copied from elsewhere.

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
| `project.path` | Absolute path chosen by "Choosing the Project Path" below, `/` separators |
| `project.name` | Name of that project folder |
| `project.gitRemote` | The "Git Remote" command below, which strips credentials before `@` (e.g. `user:token@` in `https://user:token@host/…`) and anything after `?` or `#` in its own output; `null` on failure |
| `project.manifests` | Relative paths (`/` separators, sorted) of the manifest files below, found in the project root and its direct subfolders (depth 2) |

Manifest files: `package.json`, `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle`, `build.gradle.kts`, `Gemfile`, `composer.json`, `*.csproj`, `*.sln`, `Dockerfile`, `docker-compose.yml`, `docker-compose.yaml`, `compose.yml`, `compose.yaml`, `Chart.yaml`, `main.tf`, `serverless.yml`, `package.xml`, `CMakeLists.txt`

Excluded folders: `node_modules`, `.git`, `vendor`, `venv`, `.venv`, `dist`, `build`, `.kesekit`

### Choosing the Project Path

1. If the user changed the path in the form, use that path ("Project change" in Step 4 of SKILL.md).
2. Otherwise, if the existing profile's `project.workspace` is the same path as the current working directory, and its `project.path` passes the Path Safety Rules and the folder still exists, use that path.
3. Otherwise, use the current working directory.

`<path>` in the commands below is the project path chosen this way.

### Finding a Path by Folder Name

When the user picks a folder with [Choose folder] in the form, the browser never reveals the full path for security; it sends only the folder name (`project.picked.name`) and manifest list (`project.picked.manifests`). If the folder name passes the Path Safety Rules, search these locations for folders with that name:

```powershell
# Windows: parent of the working directory, the user folder, and local fixed drive roots
$name = '<folder name>'
$skip = '\\(node_modules|\.git|AppData|\$Recycle\.Bin|Windows|Program Files[^\\]*|ProgramData)\\'
$roots = @(@{ Path = (Split-Path -Parent (Get-Location).Path); Depth = 2 }, @{ Path = $env:USERPROFILE; Depth = 4 }) +
  @(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | ForEach-Object { @{ Path = $_.DeviceID + '\'; Depth = 2 } })
foreach ($r in $roots) {
  Get-ChildItem -LiteralPath $r.Path -Directory -Recurse -Depth $r.Depth -Filter $name -ErrorAction SilentlyContinue |
    Where-Object { "$($_.FullName)\" -notmatch $skip } | Select-Object -ExpandProperty FullName
}
```

```bash
# Linux and macOS
name='<folder name>'
for root in "$(dirname "$PWD")" "$HOME"; do
  find "$root" -maxdepth 5 -type d -name "$name" -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/Library/*' 2>/dev/null
done | LC_ALL=C sort -u
```

For each candidate, get its list with the "Manifests" commands and compare it as a set with `project.picked.manifests`:

- Exactly one match: use that path and show it in the summary.
- Several matches: show the candidate paths and let the user choose.
- No match: ask the user to paste the full path (in Explorer, right-click the folder → 'Copy as path').

### Git Remote (Credentials Stripped)

Never run a command that prints the raw URL. Strip credentials in the command output itself:

```powershell
# Windows
((git -C '<path>' remote get-url origin 2>$null) -replace '://[^/\s]*@', '://') -replace '[?#].*$', ''
```

```bash
# Linux and macOS
git -C '<path>' remote get-url origin 2>/dev/null | sed -E 's|://[^/[:space:]]*@|://|; s|[?#].*$||'
```

### Manifests — Windows

```powershell
$root = (Resolve-Path -LiteralPath '<path>').Path.TrimEnd('\')
$names = 'package.json','requirements.txt','pyproject.toml','Pipfile','setup.py','go.mod','Cargo.toml','pom.xml',
         'build.gradle','build.gradle.kts','Gemfile','composer.json','*.csproj','*.sln','Dockerfile',
         'docker-compose.yml','docker-compose.yaml','compose.yml','compose.yaml','Chart.yaml','main.tf',
         'serverless.yml','package.xml','CMakeLists.txt'
Get-ChildItem -LiteralPath $root -Recurse -Depth 1 -File -Include $names -ErrorAction SilentlyContinue |
  ForEach-Object { $_.FullName.Substring($root.Length + 1).Replace('\', '/') } |
  Where-Object { "/$_" -notmatch '/(node_modules|\.git|vendor|venv|\.venv|dist|build|\.kesekit)/' } |
  Sort-Object -Unique
```

### Manifests — Linux and macOS

```bash
(cd '<path>' && find . -maxdepth 2 -type f \( -name package.json -o -name requirements.txt -o -name pyproject.toml \
  -o -name Pipfile -o -name setup.py -o -name go.mod -o -name Cargo.toml -o -name pom.xml \
  -o -name build.gradle -o -name build.gradle.kts -o -name Gemfile -o -name composer.json \
  -o -name '*.csproj' -o -name '*.sln' -o -name Dockerfile -o -name docker-compose.yml \
  -o -name docker-compose.yaml -o -name compose.yml -o -name compose.yaml -o -name Chart.yaml \
  -o -name main.tf -o -name serverless.yml -o -name package.xml -o -name CMakeLists.txt \) \
  -not -path '*/node_modules/*' -not -path '*/.git/*' -not -path '*/vendor/*' -not -path '*/venv/*' \
  -not -path '*/.venv/*' -not -path '*/dist/*' -not -path '*/build/*' -not -path '*/.kesekit/*' \
  | sed 's|^\./||' | LC_ALL=C sort -u)
```

## Languages, Frameworks, AI Libraries

Decide by reading the manifest files only.

| Evidence | `languages` |
|----------|-------------|
| `package.json` | JavaScript (plus TypeScript if `tsconfig.json` exists) |
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py` | Python |
| `go.mod` / `Cargo.toml` / `pom.xml`, `build.gradle*` / `Gemfile` / `composer.json` / `*.csproj`, `*.sln` / `CMakeLists.txt` | Go / Rust / Java / Ruby / PHP / C# / C/C++ |

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

If the rules above leave `domains` empty, add `cii`. Always fill `ciiTargets`, whether or not `cii` is suggested (the user may pick CII later). If the rules give no target, fall back to `pc` when `role` is `dev-pc`, otherwise `windows` or `unix` by OS.

Suggestions for the remaining items. Items the user leaves blank in the form use these values.

| Item | Suggestion |
|------|------------|
| `purpose` | `pre-deploy` if there is at least one manifest, otherwise `general` |
| `scope` | `project-code` if there are manifests; `host` if `role` is not `dev-pc` or `webServers`, `databases`, or `services` is not empty; `cloud` if `cloudClis` is not empty. If none apply, `host` |
| `ztTargetMaturity` | `initial` (used only when Zero Trust is chosen) |
| `organizationType` | No suggestion (blank means not specified) |
| `role` | Result of "Role Inference" above |

Put `purpose`, `scope`, `domains`, `ciiTargets`, and `ztTargetMaturity` in `detected.recommended` of `setup-data.js`, and never leave any of them empty.

## Report Conversion Tools (`reportTools`)

Checked so the form's "Report format" section can show what is available. Only look for installed tools; never install or download anything. Put the result in `detected.reportTools` of `setup-data.js` and do not save it in the profile (it is checked again when a report is written).

| Key | Values | Rule |
|-----|--------|------|
| `pdf` | `Edge`, `Chrome`, `Chromium`, `LibreOffice`, `null` | The first browser found, otherwise LibreOffice (`soffice`) |
| `hwpx` | `kordoc`, `kordoc-mcp`, `npx`, `null` | `kordoc` if the command exists, `kordoc-mcp` if Claude's tool list has kordoc MCP tools, `npx` if only Node.js 20 or later is available (consent needed before running), otherwise `null` |
| `pptx` | `pandoc`, `python-pptx`, `null` | The `pandoc` command, otherwise Python `import pptx` |

```powershell
# Windows
@("${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe", "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe") |
  Where-Object { Test-Path -LiteralPath $_ }
foreach ($c in 'soffice','kordoc','node','pandoc') { if (Get-Command $c -ErrorAction SilentlyContinue) { $c } }
node --version 2>$null
python -c "import pptx" 2>$null; if ($LASTEXITCODE -eq 0) { 'python-pptx' }
```

```bash
# Linux and macOS
for c in microsoft-edge google-chrome chromium chromium-browser soffice kordoc node pandoc; do command -v "$c" >/dev/null 2>&1 && echo "$c"; done
[ -d '/Applications/Microsoft Edge.app' ] && echo edge-app; [ -d '/Applications/Google Chrome.app' ] && echo chrome-app
node --version 2>/dev/null
python3 -c 'import pptx' 2>/dev/null && echo python-pptx
```

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
