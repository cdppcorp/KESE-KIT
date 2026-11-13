# KESE Profile Schema

## Files

| Path | Description |
|------|-------------|
| `.kesekit/profile.json` | The saved profile. Every kesekit skill reads it in Step 0 |
| `.kesekit/setup.html`, `.kesekit/setup-form.js`, `.kesekit/setup-i18n.js` | The input form, its behavior, and its display strings (temporary, deleted after a successful save) |
| `.kesekit/setup-data.js` | Detection results handed to the form (temporary, deleted after a successful save) |

Create `.kesekit/` inside the working directory where Claude Code runs. The project to assess (`project.path`) defaults to the working directory, but the user can change it in the form. `.kesekit/` holds host details such as the hostname, so keep it out of Git.

## profile.json Structure

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
      "purpose": "Self-check before the ISMS-P certification audit",
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
    "check": "Summarize results as a Markdown table for the PR",
    "fix": "Generate scripts only; do not apply them",
    "guide": ""
  }
}
```

| Field | Meaning |
|-------|---------|
| `project.path` | Absolute path of the project to assess. Defaults to the working directory; the user can change it |
| `project.gitRemote` | The Git remote used in reports (credentials stripped). When `project.gitRemoteEdited` is `true`, the user typed it |
| `project.workspace` | The working directory where the profile was saved. Detects a profile that was copied or moved |
| `project.fingerprint` | The Git remote and manifest list detected at `project.path`. Used only for change detection |
| `system.roleEdited` | `true` if the user picked the machine role; `false` means it was detected and follows the next detection |
| `environmentSource` | Per environment list: `auto` (auto-detected; Claude re-detects at `project.path` when saving) or `manual` (picked by the user) |
| `assessment.source` | Where each assessment value came from: `selected` (the user picked it), `custom` (Claude mapped the user's own words), `recommended` (left blank, so the suggestion was used), `null` (not applicable) |
| `assessment.custom` | The user's own words per item. Kept even when a value was selected; skills read it as the user's explanation |

## Allowed Values

Same order as the form (`kesekit-enums` in `templates/setup-form.html`). Values not in this table are never saved.

| Field | Allowed values |
|-------|----------------|
| `assessment.purpose` | `cii-legal`, `pre-deploy`, `code-review`, `zt-maturity`, `general`, `other` |
| `assessment.scope` | `host`, `project-code`, `remote-systems`, `cloud`, `management` |
| `assessment.domains` | `cii`, `ai-security`, `robot-security`, `space-security`, `secure-coding`, `zero-trust`, `supply-chain` |
| `assessment.ciiTargets` | `unix`, `windows`, `web-service`, `security-equip`, `network`, `control-system`, `pc`, `database`, `mobile`, `webapp`, `virtualization`, `cloud`, `admin`, `physical` |
| `assessment.ztTargetMaturity` | `traditional`, `initial`, `advanced`, `optimal` |
| `assessment.organizationType` | `public`, `cii-operator`, `enterprise`, `startup`, `individual`, `other` |
| `system.role` | `dev-pc`, `server`, `vm`, `container`, `other` |
| `system.os` (detected) | `windows`, `linux`, `macos`, `other` |

- `assessment.ciiTargets` values match the file names in each skill's `templates/cii/<value>.md`.
- `assessment.domains` values map to each skill's domain branches (CII, AI Security, Robot Security, Space Security, Secure Coding, Zero Trust, SW Supply Chain).
- `ztTargetMaturity` goes `traditional` → `initial` → `advanced` → `optimal`.
- The default options for the environment lists (`environment.*`) live in `kesekit-detect` in `templates/setup-form.html` and match the recorded names in `references/detection.md`. Users may add values that are not listed.

## Required Fields

The profile is `INCOMPLETE` if any of these is missing or empty:

- `schemaVersion` (= 1), `updatedAt`
- `project.path`, `project.workspace`
- `system.os`, `system.role`
- `assessment.purpose`, `assessment.scope` (at least one), `assessment.domains` (at least one)
- `assessment.ciiTargets` (at least one) when `assessment.domains` contains `cii`
- `assessment.ztTargetMaturity` when `assessment.domains` contains `zero-trust`
- A value outside the Allowed Values table also counts as missing

`assessment.organizationType` is optional. Items the user leaves blank are filled with suggestions before saving, and suggestions are never empty ("Domain Suggestions" in `references/detection.md`), so a normally saved profile has nothing missing.

## Diagnosis Rules

| Code | Condition |
|------|-----------|
| `MISSING` | The file is absent, is not valid JSON, or `schemaVersion` is not 1. Skip the other codes in this case |
| `INCOMPLETE` | A required field is missing |
| `STALE` | Today's date − the `updatedAt` date ≥ 14 days |
| `CHANGED` | Any comparison item below differs |
| `MANUAL` | None of the above, but the user ran setup directly |

The profile is OK when none of `MISSING`, `INCOMPLETE`, `STALE`, `CHANGED` applies. When several apply, put all of them in `reasons`.

**Path comparison**: convert separators in both paths to `/` and drop a trailing `/` before comparing; ignore case on Windows. "Same path" in this document and in SKILL.md always means this.

Compare in the order below. Once an earlier step yields `CHANGED`, stop and never run commands on the saved paths.

| Order | Item | How to compare |
|:---:|------|----------------|
| 1 | `project.workspace` | `CHANGED` if it is not the same path as the current working directory. The profile may have been copied from elsewhere, so never run commands on the paths inside it |
| 2 | `project.path` | `CHANGED` if it fails the "Path Safety Rules" in `references/detection.md` or the folder no longer exists |
| 3 | `project.fingerprint.gitRemote` | Compare with the `origin` URL re-read at `project.path` (credentials stripped). Two missing values are equal |
| 3 | `project.fingerprint.manifests` | Compare as sets with the manifest list re-detected at `project.path` (order does not matter) |
| 3 | `system.hostname` | Compare ignoring case, only when both the saved and current values exist. An undetected hostname is neither missing nor changed |
| 3 | `system.os` | Compare as-is |

Never compare the user-edited `project.gitRemote`; change detection uses only the detected `project.fingerprint`.

## Paste Block (Form → Claude)

The form's [Copy] and [Save as file] produce text in this format:

```
KESEKIT_PROFILE_INPUT v1
{ "meta": {…}, "project": {…}, "system": {…}, "environment": {…}, "environmentSource": {…}, "assessment": {…}, "notes": {…} }
END_KESEKIT_PROFILE_INPUT
```

| Key | Content |
|-----|---------|
| `meta.projectPath` | `project.path` detected when the form was generated |
| `meta.generatedAt` | The `generatedAt` written to `setup-data.js` for this form |
| `meta.lang` | Form language (`ko` or `en`) |
| `project` | `path`, `gitRemote`, `gitRemoteEdited`, `picked` |
| `project.picked` | Only when chosen with [Choose folder]: `{ "name": folder name, "manifests": [manifest files] }`. In that case `path` is the folder name, not a full path. Otherwise `null` |
| `system` | Only the user-editable values: `osVersion`, `cpu`, `memoryGb`, `role`, `roleEdited` |
| `environment` | `languages`, `frameworks`, `services`, `webServers`, `databases`, `containers`, `cloudClis`, `aiLibraries` |
| `environmentSource` | `auto` or `manual` for each of the 8 lists above |
| `assessment` | `purpose`, `scope`, `domains`, `ciiTargets`, `ztTargetMaturity`, `organizationType`, `source`, `custom` |
| `notes` | `common`, `start`, `check`, `fix`, `guide` |

The form decides each assessment item in the order **selected options → the user's own words → suggestion**. An item with only the user's own words has the value `null` and `source` `custom`; Claude fills it in "Resolving the Input".

### Paste Block Validation

1. The text between the markers must be a single JSON object. If there are several blocks, use only the last one.
2. `meta.projectPath` must equal `detected.project.path` in the `setup-data.js` written this time. Otherwise it was copied from another form; reject it.
3. `meta.generatedAt` must equal the value in the `setup-data.js` written this time. Otherwise it was copied from an older form; ask the user to copy again from the new form.
4. Reject any value outside the Allowed Values table. `null` is allowed only for items whose `source` is `custom` or `null`, and for `organizationType`.
5. Each `assessment.source` value must be `selected`, `custom`, `recommended`, or `null`; for `custom`, the matching `assessment.custom` text must not be empty. Each `environmentSource` value must be `auto` or `manual`.
6. `project.path` must pass the "Path Safety Rules" in `references/detection.md` and be 500 characters or fewer. If it is not absolute, `project.picked` must exist and `project.picked.name` must equal it (the folder name rule applies). `project.gitRemote` must be `null` or look like `https://…`, `ssh://…`, or `git@host:path`, 300 characters or fewer. Strip credentials and anything after `?` or `#` once more before saving.
7. Length limits: each note 2,000 characters, each custom text 300, `osVersion` and `cpu` 200 each, list items 80 each and at most 50 per list. `memoryGb` is a whole number of 0 or more, or `null`; `system.role` must be an allowed value.
8. Drop any undefined keys.

### Resolving the Input

After validation passes, resolve values in this order before saving:

1. If `project.path` differs from `meta.projectPath`, first follow "Project change" in Step 4 of SKILL.md.
2. For items whose `source` is `custom` and value is `null`, map the text in `assessment.custom` to allowed values. If it cannot be mapped, use the suggestion from `setup-data.js`, set `source` to `recommended`, and say so in the summary.
3. Once the domains are settled: without `cii`, set `ciiTargets` to `[]`; without `zero-trust`, set `ztTargetMaturity` to `null`; set their `source` to `null`. Conversely, if the domain is present but the value is empty, use the suggestion and set `source` to `recommended`. If even the suggestion is empty, use the fallback in `references/detection.md` (`pc`/`windows`/`unix` for `ciiTargets`, `initial` for `ztTargetMaturity`).
4. Replace every environment list whose `environmentSource` is `auto` with the values detected at `project.path` in this run. Keep `manual` lists as entered.
5. Keep the `assessment.custom` text as-is even after the value is resolved.

## Merge Rules on Save

| Field | Source |
|-------|--------|
| `schemaVersion` | `1` |
| `updatedAt` | System time at save (ISO 8601 with time zone) |
| `project.path`, `project.gitRemote`, `project.gitRemoteEdited` | Input (the path is the resolved absolute path; credentials stripped from the remote) |
| `project.name` | Folder name of `project.path` |
| `project.workspace` | Current working directory |
| `project.fingerprint` | The Git remote and manifest list detected at `project.path` in this run |
| `system.os`, `system.arch`, `system.hostname`, `system.remoteSession` | This run's detection (`os` falls back to `other`, never `null`) |
| `system.osVersion`, `system.cpu`, `system.memoryGb`, `system.role`, `system.roleEdited` | Input |
| `environment`, `environmentSource` | Values after step 4 of "Resolving the Input" |
| `notes` | Input |
| `assessment` | Values after "Resolving the Input", plus `source` and `custom` |

Do not save `meta`, `project.picked`, `recommended`, or `errors`.

## Terminal Input Template (No Browser)

Pre-fill it with detected values and the previous profile, show suggestions in brackets, then print it. The user edits it and pastes everything from the first line through `[END]`.

```
[KESEKIT SETUP INPUT] Fill in after each ':' and paste everything through [END].
Blank items use the [suggested] value. Anything not in the options can be written freely; Claude maps it. Separate multiple values with commas.
Project path to assess: /srv/shop-api
Git remote: https://github.com/acme/shop-api.git
Machine role (dev-pc | server | vm | container | other) [suggested: server]:
Purpose (cii-legal | pre-deploy | code-review | zt-maturity | general | other) [suggested: pre-deploy]:
Scope (host, project-code, remote-systems, cloud, management) [suggested: host, project-code]:
Domains (cii, ai-security, robot-security, space-security, secure-coding, zero-trust, supply-chain) [suggested: cii, secure-coding]:
CII targets (unix, windows, web-service, security-equip, network, control-system, pc, database, mobile, webapp, virtualization, cloud, admin, physical) [suggested: unix, web-service]:
Zero Trust target maturity (traditional | initial | advanced | optimal) [suggested: initial]:
Organization type (public | cii-operator | enterprise | startup | individual | other) [optional]:
OS version: Ubuntu 22.04.4 LTS
CPU: Intel(R) Xeon(R) Silver 4310
Memory (GB): 64
[All skills]:
[start]:
[check]:
[fix]:
[guide]:
[END]
```

Process the reply as follows:

1. **If the path changed**: check the Path Safety Rules and that the folder exists, re-detect the project at that path, and recompute suggestions. Print the template again with the user's answers kept and the new detection filled in, and ask the user to paste it again.
2. Each item is `selected` when it uses allowed values, `custom` when it is free text (keep the text in `assessment.custom`), and when blank, fill in the suggestion and mark it `recommended`. A blank machine role uses the detected role with `roleEdited` `false`. If the Git remote differs from the detected one, `gitRemoteEdited` is `true`.
3. Set every `environmentSource` to `auto`.
4. Apply rules 4–8 of "Paste Block Validation" and steps 2–5 of "Resolving the Input".
