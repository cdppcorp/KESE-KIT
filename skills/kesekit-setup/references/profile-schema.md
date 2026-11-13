# KESE Profile Schema

## Files

| Path | Description |
|------|-------------|
| `.kesekit/profile.json` | The saved profile. Every kesekit skill reads it in Step 0 |
| `.kesekit/setup.html` | The input form (temporary, deleted after a successful save) |
| `.kesekit/setup-data.js` | Detection results handed to the form (temporary, deleted after a successful save) |

Create `.kesekit/` inside the project being assessed (the current working directory). It holds host details such as the hostname, so keep it out of Git.

## profile.json Structure

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
    "check": "Summarize results as a Markdown table for the PR",
    "fix": "Generate scripts only; do not apply them",
    "guide": ""
  }
}
```

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

## Required Fields

The profile is `INCOMPLETE` if any of these is missing or empty:

- `schemaVersion` (= 1), `updatedAt`
- `project.path`
- `system.os`, `system.role`
- `assessment.purpose`, `assessment.scope` (at least one), `assessment.domains` (at least one)
- `assessment.ciiTargets` (at least one) when `assessment.domains` contains `cii`
- `assessment.ztTargetMaturity` when `assessment.domains` contains `zero-trust`
- A value outside the Allowed Values table also counts as missing

## Diagnosis Rules

| Code | Condition |
|------|-----------|
| `MISSING` | The file is absent, is not valid JSON, or `schemaVersion` is not 1. Skip the other codes in this case |
| `INCOMPLETE` | A required field is missing |
| `STALE` | Today's date − the `updatedAt` date ≥ 14 days |
| `CHANGED` | Any comparison item below differs from the current value |
| `MANUAL` | None of the above, but the user ran setup directly |

The profile is OK when none of `MISSING`, `INCOMPLETE`, `STALE`, `CHANGED` applies. When several apply, put all of them in `reasons`.

Comparison items:

| Item | How to compare |
|------|----------------|
| `project.path` | Absolute path of the current working directory. Convert separators to `/` and drop a trailing `/` before comparing. Ignore case on Windows |
| `project.gitRemote` | The `origin` URL with credentials stripped. Two missing values are equal |
| `project.manifests` | Compare as sets (order does not matter) |
| `system.hostname` | Compare ignoring case, only when both the saved and current values exist. An undetected hostname is neither missing nor changed |
| `system.os` | Compare as-is |

## Paste Block (Form → Claude)

The form's [Copy] and [Save as file] produce text in this format:

```
KESEKIT_PROFILE_INPUT v1
{ "meta": {…}, "system": {…}, "environment": {…}, "assessment": {…}, "notes": {…} }
END_KESEKIT_PROFILE_INPUT
```

| Key | Content |
|-----|---------|
| `meta.projectPath` | `project.path` when the form was generated |
| `meta.generatedAt` | The `generatedAt` written to `setup-data.js` for this form |
| `meta.lang` | Form language (`ko` or `en`) |
| `system` | Only the user-editable values: `osVersion`, `cpu`, `memoryGb`, `role` |
| `environment` | `languages`, `frameworks`, `services`, `webServers`, `databases`, `containers`, `cloudClis`, `aiLibraries` |
| `assessment` | `purpose`, `scope`, `domains`, `ciiTargets`, `ztTargetMaturity`, `organizationType` |
| `notes` | `common`, `start`, `check`, `fix`, `guide` |

### Paste Block Validation

1. The text between the markers must be a single JSON object. If there are several blocks, use only the last one.
2. `meta.projectPath` must equal the current working directory (compared as in Diagnosis Rules). Otherwise it is input for another project; reject it.
3. `meta.generatedAt` must equal the value in the `setup-data.js` written this time. Otherwise it was copied from an older form; ask the user to copy again from the new form.
4. Reject any value outside the Allowed Values table.
5. Check `system.role` and the `assessment.*` required fields, including the conditional ones.
6. Length limits: each note 2,000 characters, `osVersion` and `cpu` 200 characters each, list items 80 characters each and at most 50 per list. `memoryGb` is a whole number of 0 or more, or `null`.
7. Drop any undefined keys.

## Merge Rules on Save

| Field | Source |
|-------|--------|
| `schemaVersion` | `1` |
| `updatedAt` | System time at save (ISO 8601 with time zone) |
| `project.*` | This run's detection |
| `system.os`, `system.arch`, `system.hostname`, `system.remoteSession` | This run's detection |
| `system.osVersion`, `system.cpu`, `system.memoryGb`, `system.role` | Input |
| `environment`, `assessment`, `notes` | Input |

Do not save `meta`, `recommended`, or `errors`.

## Terminal Input Template (No Browser)

Pre-fill the text after each `:` with detected values and the previous profile, then print it. The user edits it and pastes everything from the first line through `[END]`.

```
[KESEKIT SETUP INPUT] Fill in after each ':' and paste everything through [END]. Separate multiple values with commas.
Machine role (dev-pc | server | vm | container | other): server
Purpose (cii-legal | pre-deploy | code-review | zt-maturity | general | other):
Scope (host, project-code, remote-systems, cloud, management): host
Domains (cii, ai-security, robot-security, space-security, secure-coding, zero-trust, supply-chain): cii
CII targets (unix, windows, web-service, security-equip, network, control-system, pc, database, mobile, webapp, virtualization, cloud, admin, physical): unix, web-service
Zero Trust target maturity (traditional | initial | advanced | optimal):
Organization type [optional] (public | cii-operator | enterprise | startup | individual | other):
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

Convert the reply into the paste block structure, then apply rules 4–7 of "Paste Block Validation". Use this run's detected values for `environment`.
