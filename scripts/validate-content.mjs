#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import vm from "node:vm";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const rootDir = path.resolve(__dirname, "..");
const errors = [];
const checks = [];

const skillRoots = ["skills", "skills-ko"];
const skillNames = ["start", "check", "fix", "guide"];

// Maps (skillRoot, skillName) to actual directory name
function skillDir(skillRoot, skillName) {
  if (skillRoot === "skills-ko") {
    return `kesekit-${skillName}-ko`;
  }
  return `kesekit-${skillName}`;
}

function skillPath(skillRoot, skillName, ...rest) {
  return path.join(rootDir, skillRoot, skillDir(skillRoot, skillName), ...rest);
}

const expectedCiiCounts = {
  "admin.md": 127,
  "cloud.md": 19,
  "control-system.md": 46,
  "database.md": 26,
  "mobile.md": 4,
  "network.md": 38,
  "pc.md": 18,
  "physical.md": 18,
  "security-equip.md": 23,
  "unix.md": 67,
  "virtualization.md": 25,
  "web-service.md": 26,
  "webapp.md": 21,
  "windows.md": 64,
};

const expectedRobotCounts = {
  "cyber-resilience.md": 13,
  "iec62443.md": 50,
  "ssdf.md": 19,
  "supply-chain.md": 7,
  "wireless.md": 14,
};

const expectedStartReferenceCounts = {
  "templates/cii/unix.md": 67,
  "templates/cii/windows.md": 64,
  "templates/cii/web-service.md": 26,
  "templates/cii/security-equip.md": 23,
  "templates/cii/network.md": 38,
  "templates/cii/control-system.md": 46,
  "templates/cii/pc.md": 18,
  "templates/cii/database.md": 26,
  "templates/cii/mobile.md": 4,
  "templates/cii/webapp.md": 21,
  "templates/cii/virtualization.md": 25,
  "templates/cii/cloud.md": 19,
  "templates/cii/admin.md": 127,
  "templates/cii/physical.md": 18,
};

const expectedReadmeEnglishCounts = {
  "U-01~U-67": 67,
  "W-01~W-64": 64,
  "WEB-01~WEB-26": 26,
  "S-01~S-23": 23,
  "N-01~N-38": 38,
  "C-01~C-51": 46,
  "PC-01~PC-18": 18,
  "D-01~D-26": 26,
  "M-01~M-04": 4,
  "21 codes": 21,
  "HV-01~HV-25": 25,
  "CA-01~CA-19": 19,
};

const expectedReadmeKoreanCounts = {
  "U-01~U-67": 67,
  "W-01~W-64": 64,
  "WEB-01~WEB-26": 26,
  "S-01~S-23": 23,
  "N-01~N-38": 38,
  "C-01~C-51": 46,
  "PC-01~PC-18": 18,
  "D-01~D-26": 26,
  "M-01~M-04": 4,
  "21개 코드": 21,
  "HV-01~HV-25": 25,
  "CA-01~CA-19": 19,
};

function rel(filePath) {
  return path.relative(rootDir, filePath).replaceAll(path.sep, "/");
}

function read(filePath) {
  return fs.readFileSync(filePath, "utf8");
}

function assert(condition, message) {
  if (!condition) {
    errors.push(message);
  }
}

function check(name, fn) {
  checks.push(name);
  try {
    fn();
  } catch (error) {
    errors.push(`${name}: ${error instanceof Error ? error.message : String(error)}`);
  }
}

function listMarkdownFiles(dirPath) {
  const result = [];

  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    const entryPath = path.join(dirPath, entry.name);

    if (entry.isDirectory()) {
      result.push(...listMarkdownFiles(entryPath));
      continue;
    }

    if (entry.isFile() && entry.name.endsWith(".md")) {
      result.push(rel(entryPath));
    }
  }

  return result.sort();
}

function parseItemCountFromCell(cell) {
  const trimmed = cell.trim();

  if (/^(코드|Code|#|항목|Item|대상|Target)$/i.test(trimmed)) {
    return 0;
  }

  let match = trimmed.match(/^([A-Z]{1,5})-(\d+)\s*~\s*\1-(\d+)$/);
  if (match) {
    const start = Number(match[2]);
    const end = Number(match[3]);
    return end - start + 1;
  }

  match = trimmed.match(/^([A-Z]{1,5})-(\d+)$/);
  if (match) {
    return 1;
  }

  if (/^[A-Z]{2}$/.test(trimmed)) {
    return 1;
  }

  return 0;
}

function countReferenceItems(filePath) {
  return read(filePath)
    .split(/\r?\n/)
    .reduce((sum, line) => {
      const match = line.match(/^\|\s*([^|]+?)\s*\|/);
      return sum + (match ? parseItemCountFromCell(match[1]) : 0);
    }, 0);
}

function sectionBetween(content, startMarker, endMarker) {
  const start = content.indexOf(startMarker);
  if (start === -1) {
    return null;
  }

  const end = content.indexOf(endMarker, start + startMarker.length);
  if (end === -1) {
    return null;
  }

  return content.slice(start, end);
}

function parseStartReferenceTable(filePath) {
  const content = read(filePath);
  const rows = {};

  for (const line of content.split(/\r?\n/)) {
    const match = line.match(/^\|\s*[^|]+?\s*\|\s*`(templates\/cii\/[^`]+)`\s*\|\s*(\d+)\s*\|$/);
    if (match) {
      rows[match[1]] = Number(match[2]);
    }
  }

  return rows;
}

function parseReadmeTechnicalTable(content, startMarker, endMarker) {
  const section = sectionBetween(content, startMarker, endMarker);
  if (!section) {
    return null;
  }

  const rows = {};

  for (const line of section.split(/\r?\n/)) {
    const match = line.match(/^\|\s*[^|]+?\s*\|\s*([^|]+?)\s*\|\s*(\d+)\s*\|$/);
    if (match) {
      rows[match[1].trim()] = Number(match[2]);
    }
  }

  return rows;
}

function assertObjectEqual(actual, expected, name) {
  const actualJson = JSON.stringify(actual, Object.keys(actual).sort());
  const expectedJson = JSON.stringify(expected, Object.keys(expected).sort());
  assert(actualJson === expectedJson, `${name} mismatch.\nactual: ${actualJson}\nexpected: ${expectedJson}`);
}

function assertIncludes(filePath, pattern, description) {
  const content = read(filePath);
  const ok = pattern instanceof RegExp ? pattern.test(content) : content.includes(pattern);
  assert(ok, `${rel(filePath)} is missing ${description}`);
}

check("reference-tree-parity", () => {
  for (const skillRoot of skillRoots) {
    const baseDir = skillPath(skillRoot, "start", "references");
    const basePrefix = `${skillRoot}/${skillDir(skillRoot, "start")}/`;
    const expectedFiles = listMarkdownFiles(baseDir).map((file) => file.replace(basePrefix, ""));

    for (const skillName of skillNames.slice(1)) {
      const dirPath = skillPath(skillRoot, skillName, "references");
      const prefix = `${skillRoot}/${skillDir(skillRoot, skillName)}/`;
      const actualFiles = listMarkdownFiles(dirPath).map((file) => file.replace(prefix, ""));
      assertObjectEqual(actualFiles, expectedFiles, `${skillRoot}/${skillDir(skillRoot, skillName)}/references file list`);
    }
  }
});

check("reference-content-parity", () => {
  for (const skillRoot of skillRoots) {
    const baseDir = skillPath(skillRoot, "start", "references");
    const basePrefix = `${skillRoot}/${skillDir(skillRoot, "start")}/`;
    const relativeFiles = listMarkdownFiles(baseDir).map((file) => file.replace(basePrefix, ""));

    for (const relativeFile of relativeFiles) {
      const baseline = read(skillPath(skillRoot, "start", relativeFile));

      for (const skillName of skillNames.slice(1)) {
        const candidatePath = skillPath(skillRoot, skillName, relativeFile);
        const candidate = read(candidatePath);
        assert(
          candidate === baseline,
          `${rel(candidatePath)} diverged from ${skillRoot}/${skillDir(skillRoot, "start")}/${relativeFile}`,
        );
      }
    }
  }
});

check("cii-reference-counts", () => {
  const ciiDir = skillPath("skills", "start", "templates", "cii");

  for (const [fileName, expectedCount] of Object.entries(expectedCiiCounts)) {
    const filePath = path.join(ciiDir, fileName);
    const actualCount = countReferenceItems(filePath);
    assert(actualCount === expectedCount, `${rel(filePath)} expected ${expectedCount} items, found ${actualCount}`);
  }
});

check("robot-reference-counts", () => {
  const robotDir = skillPath("skills", "start", "templates", "robot-security");
  let total = 0;

  for (const [fileName, expectedCount] of Object.entries(expectedRobotCounts)) {
    const filePath = path.join(robotDir, fileName);
    const actualCount = countReferenceItems(filePath);
    total += actualCount;
    assert(actualCount === expectedCount, `${rel(filePath)} expected ${expectedCount} items, found ${actualCount}`);
  }

  assert(total === 103, `Robot Security total expected 103 items, found ${total}`);
});

check("start-skill-count-tables", () => {
  const englishStart = parseStartReferenceTable(skillPath("skills", "start", "SKILL.md"));
  const koreanStart = parseStartReferenceTable(skillPath("skills-ko", "start", "SKILL.md"));

  assertObjectEqual(englishStart, expectedStartReferenceCounts, "skills/kesekit-start/SKILL.md reference table");
  assertObjectEqual(koreanStart, expectedStartReferenceCounts, "skills-ko/kesekit-start-ko/SKILL.md reference table");
});

check("readme-count-tables", () => {
  const content = read(path.join(rootDir, "README.md"));
  const englishTable = parseReadmeTechnicalTable(content, "**Technical Assessment**", "**Administrative Assessment**");
  const koreanTable = parseReadmeTechnicalTable(content, "**기술적 취약점 평가**", "**관리적 취약점 평가**");

  assert(englishTable !== null, "README.md English technical assessment table was not found");
  assert(koreanTable !== null, "README.md Korean technical assessment table was not found");

  if (englishTable) {
    assertObjectEqual(englishTable, expectedReadmeEnglishCounts, "README.md English CII count table");
  }

  if (koreanTable) {
    assertObjectEqual(koreanTable, expectedReadmeKoreanCounts, "README.md Korean CII count table");
  }
});

check("router-robot-branch-coverage", () => {
  for (const skillName of skillNames) {
    assertIncludes(skillPath("skills", skillName, "SKILL.md"), /## Robot Security Branch/, "an English Robot Security branch section");
    assertIncludes(skillPath("skills-ko", skillName, "SKILL.md"), /## 로봇 보안 분기 시/, "a Korean robot branch section");
  }
});

check("metadata-mentions-robot-security", () => {
  assertIncludes(path.join(rootDir, ".claude-plugin", "marketplace.json"), /Robot Security|로봇 보안/, "Robot Security metadata");
  assertIncludes(path.join(rootDir, "README.md"), /Robot Security/, "Robot Security in the English README");
  assertIncludes(path.join(rootDir, "README.md"), /로봇 보안/, "robot security in the Korean README");
});

// --- Templates and Scripts directory checks ---

function listAllFiles(dirPath) {
  const result = [];
  if (!fs.existsSync(dirPath)) return result;
  for (const entry of fs.readdirSync(dirPath, { withFileTypes: true })) {
    const entryPath = path.join(dirPath, entry.name);
    if (entry.isDirectory()) {
      result.push(...listAllFiles(entryPath));
    } else if (entry.isFile()) {
      result.push(rel(entryPath));
    }
  }
  return result.sort();
}

function countFiles(dirPath) {
  return listAllFiles(dirPath).length;
}

const expectedTemplateFileCounts = {
  "cii": 14,
  "robot-security": 6,
  "space-security": 5,
  "ai-security": 3,
};

const expectedScriptFileCounts = {
  "cii": 8,
  "robot-security": 4,
  "ai-security": 3,
  "zero-trust": 3,
};

// fix skills have additional space-security scripts
const expectedFixScriptFileCounts = {
  ...expectedScriptFileCounts,
  "space-security": 3,
};

check("templates-directories-exist", () => {
  for (const skillRoot of skillRoots) {
    for (const skillName of skillNames) {
      const templatesDir = skillPath(skillRoot, skillName, "templates");
      const label = `${skillRoot}/${skillDir(skillRoot, skillName)}/templates`;
      assert(fs.existsSync(templatesDir), `${label} directory does not exist`);
    }
  }
});

check("scripts-directories-exist", () => {
  for (const skillRoot of skillRoots) {
    for (const skillName of skillNames) {
      const scriptsDir = skillPath(skillRoot, skillName, "scripts");
      const label = `${skillRoot}/${skillDir(skillRoot, skillName)}/scripts`;
      assert(fs.existsSync(scriptsDir), `${label} directory does not exist`);
    }
  }
});

check("template-file-counts", () => {
  for (const skillRoot of skillRoots) {
    for (const skillName of skillNames) {
      for (const [subDir, expectedCount] of Object.entries(expectedTemplateFileCounts)) {
        const dirPath = skillPath(skillRoot, skillName, "templates", subDir);
        const label = `${skillRoot}/${skillDir(skillRoot, skillName)}/templates/${subDir}`;
        assert(fs.existsSync(dirPath), `${label} directory does not exist`);
        if (fs.existsSync(dirPath)) {
          const actual = countFiles(dirPath);
          assert(actual === expectedCount, `${label} expected ${expectedCount} files, found ${actual}`);
        }
      }
    }
  }
});

check("script-file-counts", () => {
  for (const skillRoot of skillRoots) {
    for (const skillName of skillNames) {
      const expected = skillName === "fix" ? expectedFixScriptFileCounts : expectedScriptFileCounts;
      for (const [subDir, expectedCount] of Object.entries(expected)) {
        const dirPath = skillPath(skillRoot, skillName, "scripts", subDir);
        const label = `${skillRoot}/${skillDir(skillRoot, skillName)}/scripts/${subDir}`;
        assert(fs.existsSync(dirPath), `${label} directory does not exist`);
        if (fs.existsSync(dirPath)) {
          const actual = countFiles(dirPath);
          assert(actual === expectedCount, `${label} expected ${expectedCount} files, found ${actual}`);
        }
      }
    }
  }
});

check("template-content-parity", () => {
  for (const skillRoot of skillRoots) {
    const baseDir = skillPath(skillRoot, "start", "templates");
    const basePrefix = `${skillRoot}/${skillDir(skillRoot, "start")}/`;

    for (const subDir of Object.keys(expectedTemplateFileCounts)) {
      const subDirPath = path.join(baseDir, subDir);
      if (!fs.existsSync(subDirPath)) continue;

      const baselineFiles = listAllFiles(subDirPath).map((f) => f.replace(basePrefix, ""));

      for (const skillName of skillNames.slice(1)) {
        const candidateDir = skillPath(skillRoot, skillName, "templates", subDir);
        const prefix = `${skillRoot}/${skillDir(skillRoot, skillName)}/`;
        const candidateFiles = listAllFiles(candidateDir).map((f) => f.replace(prefix, ""));
        assertObjectEqual(candidateFiles, baselineFiles, `${skillRoot}/${skillDir(skillRoot, skillName)}/templates/${subDir} file list`);

        for (const relFile of baselineFiles) {
          const baselinePath = skillPath(skillRoot, "start", relFile);
          const candidatePath = skillPath(skillRoot, skillName, relFile);
          const baselineContent = read(baselinePath);
          const candidateContent = read(candidatePath);
          assert(
            candidateContent === baselineContent,
            `${rel(candidatePath)} diverged from ${skillRoot}/${skillDir(skillRoot, "start")}/${relFile}`,
          );
        }
      }
    }
  }
});

check("script-content-parity", () => {
  // Scripts in cii/ and robot-security/ should be identical across all skills.
  // space-security/ scripts only exist in fix skills, so parity is checked between
  // skills/kesekit-fix and skills-ko/kesekit-fix-ko (handled by cross-language parity below).
  const sharedSubDirs = ["cii", "robot-security", "ai-security", "zero-trust"];

  for (const skillRoot of skillRoots) {
    for (const subDir of sharedSubDirs) {
      const baseDir = skillPath(skillRoot, "start", "scripts", subDir);
      if (!fs.existsSync(baseDir)) continue;

      const basePrefix = `${skillRoot}/${skillDir(skillRoot, "start")}/`;
      const baselineFiles = listAllFiles(baseDir).map((f) => f.replace(basePrefix, ""));

      for (const skillName of skillNames.slice(1)) {
        const candidateDir = skillPath(skillRoot, skillName, "scripts", subDir);
        const prefix = `${skillRoot}/${skillDir(skillRoot, skillName)}/`;
        const candidateFiles = listAllFiles(candidateDir).map((f) => f.replace(prefix, ""));
        assertObjectEqual(candidateFiles, baselineFiles, `${skillRoot}/${skillDir(skillRoot, skillName)}/scripts/${subDir} file list`);

        for (const relFile of baselineFiles) {
          const baselinePath = skillPath(skillRoot, "start", relFile);
          const candidatePath = skillPath(skillRoot, skillName, relFile);
          const baselineContent = read(baselinePath);
          const candidateContent = read(candidatePath);
          assert(
            candidateContent === baselineContent,
            `${rel(candidatePath)} diverged from ${skillRoot}/${skillDir(skillRoot, "start")}/${relFile}`,
          );
        }
      }
    }
  }
});

check("cross-language-template-parity", () => {
  // templates should be identical between skills/ and skills-ko/ for each skill type
  for (const skillName of skillNames) {
    for (const subDir of Object.keys(expectedTemplateFileCounts)) {
      const enDir = skillPath("skills", skillName, "templates", subDir);
      const koDir = skillPath("skills-ko", skillName, "templates", subDir);
      if (!fs.existsSync(enDir) || !fs.existsSync(koDir)) continue;

      const enPrefix = `skills/${skillDir("skills", skillName)}/`;
      const koPrefix = `skills-ko/${skillDir("skills-ko", skillName)}/`;
      const enFiles = listAllFiles(enDir).map((f) => f.replace(enPrefix, ""));
      const koFiles = listAllFiles(koDir).map((f) => f.replace(koPrefix, ""));
      assertObjectEqual(koFiles, enFiles, `skills-ko/${skillDir("skills-ko", skillName)}/templates/${subDir} vs EN file list`);

      for (const relFile of enFiles) {
        const enContent = read(skillPath("skills", skillName, relFile));
        const koContent = read(skillPath("skills-ko", skillName, relFile));
        assert(
          koContent === enContent,
          `skills-ko/${skillDir("skills-ko", skillName)}/${relFile} diverged from skills/${skillDir("skills", skillName)}/${relFile}`,
        );
      }
    }
  }
});

check("cross-language-script-parity", () => {
  // scripts should be identical between skills/ and skills-ko/ for each skill type
  for (const skillName of skillNames) {
    const expected = skillName === "fix" ? expectedFixScriptFileCounts : expectedScriptFileCounts;
    for (const subDir of Object.keys(expected)) {
      const enDir = skillPath("skills", skillName, "scripts", subDir);
      const koDir = skillPath("skills-ko", skillName, "scripts", subDir);
      if (!fs.existsSync(enDir) || !fs.existsSync(koDir)) continue;

      const enPrefix = `skills/${skillDir("skills", skillName)}/`;
      const koPrefix = `skills-ko/${skillDir("skills-ko", skillName)}/`;
      const enFiles = listAllFiles(enDir).map((f) => f.replace(enPrefix, ""));
      const koFiles = listAllFiles(koDir).map((f) => f.replace(koPrefix, ""));
      assertObjectEqual(koFiles, enFiles, `skills-ko/${skillDir("skills-ko", skillName)}/scripts/${subDir} vs EN file list`);

      for (const relFile of enFiles) {
        const enContent = read(skillPath("skills", skillName, relFile));
        const koContent = read(skillPath("skills-ko", skillName, relFile));
        assert(
          koContent === enContent,
          `skills-ko/${skillDir("skills-ko", skillName)}/${relFile} diverged from skills/${skillDir("skills", skillName)}/${relFile}`,
        );
      }
    }
  }
});

// --- Setup skill checks ---
// Every kesekit skill runs the setup skill first (Step 0). The setup skill opens an
// HTML form, and the user hands the result back by pasting a marker-delimited block.

const setupSkillDirs = { skills: "kesekit-setup", "skills-ko": "kesekit-setup-ko" };
const setupRequiredFiles = [
  "SKILL.md",
  "references/profile-schema.md",
  "references/detection.md",
  "templates/setup-form.html",
  "templates/setup-form.js",
  "templates/setup-i18n.js",
];
const setupTemplateFiles = ["templates/setup-form.html", "templates/setup-form.js", "templates/setup-i18n.js"];
const setupFormMarkers = [
  '<script src="setup-i18n.js"></script>',
  '<script src="setup-data.js"></script>',
  '<script src="setup-form.js"></script>',
  'id="kesekit-enums"',
  'id="kesekit-detect"',
  'id="project-edit-btn"',
  'id="pick-folder-btn"',
  'id="projectPath"',
  'id="gitRemote"',
  'id="fs-reportFormat"',
  'id="report-status"',
];
// Enums rendered without a free-text input or resolved-value preview.
const enumsWithoutFreeText = ["role", "reportFormat"];
const reportToolKeys = ["builtin", "unknown", "ready", "pdfNone", "pptxNone", "hwpxKordoc", "hwpxMcp", "hwpxNpx", "hwpxNone"];
// Every skill that writes report files reads the shared report-output rules from its own references.
const reportOutputSkills = {
  skills: ["kesekit-start", "kesekit-check", "kesekit-fix", "kesekit-guide", "kesekit-advisory"],
  "skills-ko": ["kesekit-start-ko", "kesekit-check-ko", "kesekit-fix-ko", "kesekit-guide-ko", "kesekit-advisory-ko"],
};
const reportOutputMarkers = ["`output.reportFormat`", "report.html", "`templates/report/report.html`", "--print-to-pdf", "kordoc generate", "--preset 보고서", "pandoc", "`npx -y kordoc`"];
// The HTML report template: same layout in both languages, a fixed finding structure, print-ready, no scripts.
const reportTemplateMarkers = {
  skills: ["## Report Structure", "## Writing a Finding"],
  "skills-ko": ["## 보고서 구성", "## 발견 사항 쓰는 법"],
};
const reportTemplateFields = {
  skills: ["<dt>Current state</dt>", "<dt>Risk</dt>", "<dt>Example</dt>", "<dt>Remediation</dt>"],
  "skills-ko": ["<dt>현황</dt>", "<dt>문제점</dt>", "<dt>예시</dt>", "<dt>조치 방안</dt>"],
};
const reportTemplateCommon = ['class="finding"', 'class="cover"', 'class="toc"', "@media print", "@page"];
const setupScriptMarkers = ["KESEKIT_PROFILE_INPUT v1", "END_KESEKIT_PROFILE_INPUT", "showDirectoryPicker", "environmentSource"];
const envKeys = ["aiLibraries", "cloudClis", "containers", "databases", "frameworks", "languages", "services", "webServers"];
const setupSchemaFields = [
  "`project.picked`",
  "`environmentSource`",
  "`project.workspace`",
  "`project.fingerprint`",
  "`assessment.source`",
  "`assessment.custom`",
  "`output.reportFormat`",
];
const expectedEnumKeys = [
  "ciiTargets",
  "domains",
  "organizationType",
  "purpose",
  "reportFormat",
  "role",
  "scope",
  "ztTargetMaturity",
];
const enumFields = {
  purpose: "assessment.purpose",
  scope: "assessment.scope",
  domains: "assessment.domains",
  ciiTargets: "assessment.ciiTargets",
  ztTargetMaturity: "assessment.ztTargetMaturity",
  organizationType: "assessment.organizationType",
  role: "system.role",
  reportFormat: "output.reportFormat",
};
const gateHeadings = { skills: "## Step 0: Setup Check", "skills-ko": "## 0단계: 초기 설정 확인" };
const STALE_DAYS = 14;

function setupPath(skillRoot, ...rest) {
  return path.join(rootDir, skillRoot, setupSkillDirs[skillRoot], ...rest);
}

function readSetupEnums() {
  const html = read(setupPath("skills", "templates", "setup-form.html"));
  const match = html.match(/<script type="application\/json" id="kesekit-enums">([\s\S]*?)<\/script>/);
  if (!match) {
    throw new Error("setup-form.html has no kesekit-enums JSON block");
  }
  return JSON.parse(match[1]);
}

check("setup-skill-files-exist", () => {
  for (const skillRoot of skillRoots) {
    for (const relFile of setupRequiredFiles) {
      const filePath = setupPath(skillRoot, relFile);
      assert(fs.existsSync(filePath), `${rel(filePath)} does not exist`);
    }
  }
});

check("setup-skill-frontmatter", () => {
  for (const skillRoot of skillRoots) {
    const namePattern = new RegExp(`^name: ${setupSkillDirs[skillRoot]}\\r?$`, "m");
    assertIncludes(setupPath(skillRoot, "SKILL.md"), namePattern, "a matching name in frontmatter");
  }
});

check("setup-form-cross-language-parity", () => {
  for (const relFile of setupTemplateFiles) {
    const en = read(setupPath("skills", relFile));
    const ko = read(setupPath("skills-ko", relFile));
    assert(en === ko, `skills-ko/kesekit-setup-ko/${relFile} diverged from the English copy`);
  }
});

function keyShape(value, prefix = "") {
  if (Array.isArray(value)) {
    return [`${prefix}[${value.length}]`];
  }
  if (value === null || typeof value !== "object") {
    return [prefix];
  }
  return Object.keys(value).sort().flatMap((key) => keyShape(value[key], prefix ? `${prefix}.${key}` : key));
}

function loadSetupStrings() {
  const sandbox = { window: {} };
  vm.runInNewContext(read(setupPath("skills", "templates", "setup-i18n.js")), sandbox);
  return sandbox.window.KESEKIT_I18N;
}

function lookup(strings, key) {
  return key.split(".").reduce((node, part) => (node && typeof node === "object" ? node[part] : undefined), strings);
}

check("setup-scripts-parse", () => {
  for (const relFile of ["templates/setup-form.js", "templates/setup-i18n.js"]) {
    const filePath = setupPath("skills", relFile);
    try {
      new vm.Script(read(filePath), { filename: rel(filePath) });
    } catch (error) {
      assert(false, `${rel(filePath)} does not parse: ${error.message}`);
    }
  }
});

check("setup-i18n-key-parity", () => {
  const strings = loadSetupStrings();
  assert(strings && strings.ko && strings.en, "setup-i18n.js must define window.KESEKIT_I18N with ko and en");
  if (strings && strings.ko && strings.en) {
    assertObjectEqual(keyShape(strings.en), keyShape(strings.ko), "setup-i18n.js en vs ko keys");
  }
});

check("setup-i18n-covers-form", () => {
  const strings = loadSetupStrings();
  const html = read(setupPath("skills", "templates", "setup-form.html"));
  const script = read(setupPath("skills", "templates", "setup-form.js"));
  const keys = new Set([
    ...Array.from(html.matchAll(/data-i18n(?:-placeholder)?="([^"]+)"/g), (match) => match[1]),
    ...Array.from(script.matchAll(/\bt\("([A-Za-z.]+)"\)/g), (match) => match[1]),
    ...Array.from(script.matchAll(/setPickStatus\("([A-Za-z.]+)"/g), (match) => match[1]).filter(Boolean),
  ]);
  for (const [key, values] of Object.entries(readSetupEnums())) {
    values.forEach((value) => keys.add(`enum.${key}.${value}`));
    if (key !== "role") keys.add(`legend.${key}`);
    if (!enumsWithoutFreeText.includes(key)) keys.add(`customPlaceholder.${key}`);
    if (key === "reportFormat") {
      const builtinMatch = script.match(/const BUILTIN_FORMATS = (\[[^\]]*\]);/);
      const builtin = builtinMatch ? JSON.parse(builtinMatch[1]) : [];
      assert(builtinMatch !== null, "setup-form.js must declare BUILTIN_FORMATS");
      values.forEach((value) => {
        keys.add(`reportDesc.${value}`);
        if (!builtin.includes(value)) keys.add(`reportTool.${value}None`);
      });
    }
  }
  reportToolKeys.forEach((key) => keys.add(`reportTool.${key}`));
  keys.add("reportDefault");
  envKeys.forEach((key) => keys.add(`env.${key}`));
  ["MISSING", "INCOMPLETE", "STALE", "CHANGED", "MANUAL"].forEach((code) => keys.add(`reason.${code}`));

  for (const lang of ["ko", "en"]) {
    for (const key of keys) {
      assert(typeof lookup(strings && strings[lang], key) === "string", `setup-i18n.js ${lang} is missing the string ${key}`);
    }
  }
});

check("setup-skill-handles-template-files", () => {
  for (const skillRoot of skillRoots) {
    const content = read(setupPath(skillRoot, "SKILL.md"));
    for (const fileName of ["setup.html", "setup-form.js", "setup-i18n.js", "setup-data.js"]) {
      const count = content.split(`.kesekit/${fileName}`).length - 1;
      assert(count >= 2, `${skillRoot}/${setupSkillDirs[skillRoot]}/SKILL.md must both create and delete .kesekit/${fileName} (found ${count} mention(s))`);
    }
  }
});

check("setup-form-contract", () => {
  const formPath = setupPath("skills", "templates", "setup-form.html");
  for (const marker of setupFormMarkers) {
    assertIncludes(formPath, marker, `the contract marker ${marker}`);
  }
  const scriptPath = setupPath("skills", "templates", "setup-form.js");
  for (const marker of setupScriptMarkers) {
    assertIncludes(scriptPath, marker, `the contract marker ${marker}`);
  }
  assert(!/<script>\s*\S/.test(read(formPath)), "setup-form.html must not contain inline scripts (CSP has no 'unsafe-inline')");

  const enums = readSetupEnums();
  assertObjectEqual(Object.keys(enums).sort(), expectedEnumKeys, "setup-form.html enum keys");
  for (const [key, values] of Object.entries(enums)) {
    assert(Array.isArray(values) && values.length > 0, `setup-form.html enum ${key} must be a non-empty array`);
    if (!enumsWithoutFreeText.includes(key)) {
      assertIncludes(formPath, `id="custom-${key}"`, `the free-text input for ${key}`);
      assertIncludes(formPath, `id="preview-${key}"`, `the resolved-value preview for ${key}`);
    }
  }
});

check("setup-detect-options-documented", () => {
  const html = read(setupPath("skills", "templates", "setup-form.html"));
  const match = html.match(/<script type="application\/json" id="kesekit-detect">([\s\S]*?)<\/script>/);
  assert(match !== null, "setup-form.html has no kesekit-detect JSON block");
  if (!match) return;

  const detect = JSON.parse(match[1]);
  assertObjectEqual(Object.keys(detect.envOptions).sort(), envKeys, "kesekit-detect envOptions keys");
  for (const skillRoot of skillRoots) {
    const detectionPath = setupPath(skillRoot, "references", "detection.md");
    for (const name of [...detect.manifests, ...detect.excludedDirs]) {
      assertIncludes(detectionPath, `\`${name}\``, `the manifest/excluded name \`${name}\``);
    }
    for (const [key, options] of Object.entries(detect.envOptions)) {
      for (const option of options) {
        assertIncludes(detectionPath, option, `the ${key} option ${option}`);
      }
    }
  }
});

check("setup-schema-documents-enums", () => {
  const enums = readSetupEnums();

  for (const skillRoot of skillRoots) {
    const schemaPath = setupPath(skillRoot, "references", "profile-schema.md");
    for (const [key, values] of Object.entries(enums)) {
      const expectedList = values.map((value) => `\`${value}\``).join(", ");
      const expectedRow = `| \`${enumFields[key]}\` | ${expectedList} |`;
      assertIncludes(schemaPath, expectedRow, `the exact allowed-values row ${expectedRow}`);
    }
    assertIncludes(schemaPath, "KESEKIT_PROFILE_INPUT v1", "the paste block marker");
    for (const field of setupSchemaFields) {
      assertIncludes(schemaPath, field, `the ${field} field`);
    }
    assertIncludes(schemaPath, `≥ ${STALE_DAYS}`, `the ${STALE_DAYS}-day staleness rule (≥ ${STALE_DAYS})`);
  }
});

check("skills-run-setup-gate", () => {
  for (const skillRoot of skillRoots) {
    for (const skillName of skillNames) {
      const filePath = skillPath(skillRoot, skillName, "SKILL.md");
      const content = read(filePath);
      const gateIndex = content.indexOf(gateHeadings[skillRoot]);
      const firstSectionIndex = content.indexOf("\n## ");

      assert(gateIndex !== -1, `${rel(filePath)} is missing the "${gateHeadings[skillRoot]}" section`);
      assert(gateIndex === firstSectionIndex + 1, `${rel(filePath)} must place "${gateHeadings[skillRoot]}" before every other section`);
      assertIncludes(filePath, `\`kesekit:${setupSkillDirs[skillRoot]}\``, "the setup skill invocation for its own language");
      assertIncludes(filePath, `notes.${skillName}`, `the notes.${skillName} profile field`);
      assertIncludes(filePath, "`assessment.scope`", "the assessment.scope rule in Step 0");
      assertIncludes(filePath, "`project.path`", "the project.path target rule in Step 0");
      assertIncludes(filePath, "`assessment.custom`", "the assessment.custom rule in Step 0");
    }
  }
});

check("report-output-rules", () => {
  for (const skillRoot of skillRoots) {
    const [baselineDir, ...others] = reportOutputSkills[skillRoot];
    const baselinePath = path.join(rootDir, skillRoot, baselineDir, "references", "report-output.md");
    assert(fs.existsSync(baselinePath), `${rel(baselinePath)} does not exist`);
    if (!fs.existsSync(baselinePath)) continue;

    const baseline = read(baselinePath);
    for (const marker of reportOutputMarkers) {
      assertIncludes(baselinePath, marker, `the report rule marker ${marker}`);
    }
    for (const dir of others) {
      const candidatePath = path.join(rootDir, skillRoot, dir, "references", "report-output.md");
      assert(fs.existsSync(candidatePath) && read(candidatePath) === baseline, `${rel(candidatePath)} must exist and match ${rel(baselinePath)}`);
    }
    for (const dir of reportOutputSkills[skillRoot]) {
      const skillFile = path.join(rootDir, skillRoot, dir, "SKILL.md");
      const content = read(skillFile).replaceAll("\r\n", "\n");
      const gateStart = content.indexOf(gateHeadings[skillRoot]);
      const gateEnd = gateStart === -1 ? -1 : content.indexOf("\n## ", gateStart + 1);
      const stepZero = gateStart === -1 ? "" : content.slice(gateStart, gateEnd === -1 ? undefined : gateEnd);
      assert(stepZero.includes("`output.reportFormat`"), `${rel(skillFile)} Step 0 must apply \`output.reportFormat\``);
      assert(stepZero.includes("`references/report-output.md`"), `${rel(skillFile)} Step 0 must point to \`references/report-output.md\``);
    }
    assertIncludes(setupPath(skillRoot, "references", "detection.md"), "`reportTools`", "the report tool detection (`reportTools`)");
    for (const marker of reportTemplateMarkers[skillRoot]) {
      assertIncludes(baselinePath, marker, `the report rule section ${marker}`);
    }
  }
});

function reportTemplatePath(skillRoot, dir) {
  return path.join(rootDir, skillRoot, dir, "templates", "report", "report.html");
}

check("report-template", () => {
  const styles = {};
  for (const skillRoot of skillRoots) {
    const [baselineDir, ...others] = reportOutputSkills[skillRoot];
    const baselinePath = reportTemplatePath(skillRoot, baselineDir);
    assert(fs.existsSync(baselinePath), `${rel(baselinePath)} does not exist`);
    if (!fs.existsSync(baselinePath)) continue;

    const baseline = read(baselinePath);
    const markup = baseline.replace(/<!--[\s\S]*?-->/g, "");
    for (const marker of [...reportTemplateCommon, ...reportTemplateFields[skillRoot]]) {
      assertIncludes(baselinePath, marker, `the report template marker ${marker}`);
    }
    assert(!/<script\b|\son[a-z]+\s*=|javascript:/i.test(markup), `${rel(baselinePath)} must not contain scripts, event handlers, or javascript: URLs`);
    assert(
      !/(?:href|src|action|srcset)\s*=\s*["']?(?:[a-z][a-z0-9+.-]*:)?\/\/|@import|url\(\s*["']?(?:[a-z][a-z0-9+.-]*:)?\/\//i.test(markup),
      `${rel(baselinePath)} must not load external resources`,
    );
    styles[skillRoot] = (markup.match(/<style>[\s\S]*?<\/style>/) || [""])[0];

    for (const dir of others) {
      const candidatePath = reportTemplatePath(skillRoot, dir);
      assert(fs.existsSync(candidatePath) && read(candidatePath) === baseline, `${rel(candidatePath)} must exist and match ${rel(baselinePath)}`);
    }
  }
  if (styles.skills && styles["skills-ko"]) {
    assert(styles.skills === styles["skills-ko"], "the English and Korean report templates must share the same <style>");
  }
});

check("setup-skill-registered", () => {
  const marketplace = JSON.parse(read(path.join(rootDir, ".claude-plugin", "marketplace.json")));
  const skills = marketplace.plugins.flatMap((plugin) => plugin.skills ?? []);

  for (const skillRoot of skillRoots) {
    const skillRef = `./${skillRoot}/${setupSkillDirs[skillRoot]}`;
    assert(skills.includes(skillRef), `marketplace.json does not list ${skillRef}`);
  }

  assertIncludes(path.join(rootDir, "README.md"), "/kesekit-setup-ko", "the Korean setup command");
  assertIncludes(path.join(rootDir, "README.md"), /\/kesekit-setup\s/, "the English setup command");
});

// --- KISA security notice (advisory) skills ---

const advisorySkills = [
  { root: "skills", dir: "kesekit-advisory", statsPattern: /\*\*(\d+) notices\*\*/ },
  { root: "skills-ko", dir: "kesekit-advisory-ko", statsPattern: /총 \*\*(\d+)건\*\*/ },
];

const advisoryRequiredFiles = [
  "SKILL.md",
  "scripts/advisory_lookup.py",
  "references/kisa-advisories/overview.md",
  "references/kisa-advisories/advisories.json",
  "references/kisa-advisories/vendor-index.md",
  "references/kisa-advisories/threat-response.md",
];

const advisoryStringKeys = ["no", "ntt", "date", "type", "title", "vendor", "url", "summary", "text"];
const advisoryArrayKeys = ["cves", "affected", "attachments", "refs"];
const statsBegin = "<!-- BEGIN:STATS";
const statsEnd = "<!-- END:STATS -->";

function advisoryPath(skill, ...rest) {
  return path.join(rootDir, skill.root, skill.dir, ...rest);
}

check("advisory-skill-files", () => {
  for (const skill of advisorySkills) {
    for (const file of advisoryRequiredFiles) {
      assert(fs.existsSync(advisoryPath(skill, file)), `${skill.root}/${skill.dir}/${file} is missing`);
    }
    if (fs.existsSync(advisoryPath(skill, "SKILL.md"))) {
      assertIncludes(advisoryPath(skill, "SKILL.md"), new RegExp(`^name: ${skill.dir}$`, "m"), `frontmatter name ${skill.dir}`);
    }
  }
});

check("advisory-data-parity", () => {
  const [en, ko] = advisorySkills;
  for (const file of ["scripts/advisory_lookup.py", "references/kisa-advisories/advisories.json"]) {
    assert(
      read(advisoryPath(en, file)) === read(advisoryPath(ko, file)),
      `${ko.root}/${ko.dir}/${file} diverged from ${en.root}/${en.dir}/${file}`,
    );
  }
});

check("advisory-data-schema", () => {
  const data = JSON.parse(read(advisoryPath(advisorySkills[0], "references/kisa-advisories/advisories.json")));
  assert(data.schema === 1, "advisories.json schema must be 1");
  assert(Array.isArray(data.advisories) && data.advisories.length > 0, "advisories.json has no advisories");
  const total = data.advisories.length;
  assert(data.coverage?.count === total, `advisories.json coverage.count ${data.coverage?.count} != ${total}`);

  const seenNtt = new Set();
  for (const advisory of data.advisories) {
    const label = `advisory ${advisory?.no}/${advisory?.ntt}`;
    const badStrings = advisoryStringKeys.filter((key) => typeof advisory?.[key] !== "string");
    const badArrays = advisoryArrayKeys.filter((key) => !Array.isArray(advisory?.[key]));
    assert(badStrings.length === 0, `${label} needs string field(s): ${badStrings.join(", ")}`);
    assert(badArrays.length === 0, `${label} needs array field(s): ${badArrays.join(", ")}`);
    assert(/^\d{4}-\d{2}-\d{2}$/.test(advisory?.date ?? ""), `${label} has invalid date ${advisory?.date}`);
    assert(/^\d+$/.test(advisory?.ntt ?? ""), `${label} has no numeric nttId`);
    const badRefs = (Array.isArray(advisory?.refs) ? advisory.refs : []).filter((ref) => !/^https?:\/\/\S+$/.test(ref?.url ?? ""));
    assert(badRefs.length === 0, `${label} has malformed reference URL(s): ${badRefs.map((ref) => ref?.url).join(", ")}`);
    assert(!seenNtt.has(advisory?.ntt), `duplicate advisory nttId ${advisory?.ntt}`);
    seenNtt.add(advisory?.ntt);
  }

  const cveMeta = data.cve_meta ?? {};
  assert(typeof cveMeta === "object" && !Array.isArray(cveMeta), "advisories.json cve_meta must be an object");
  const referenced = new Set(data.advisories.flatMap((advisory) => (Array.isArray(advisory?.cves) ? advisory.cves : [])));
  const inRange = (value, upper) => value === undefined || (typeof value === "number" && value >= 0 && value <= upper);
  for (const [cve, meta] of Object.entries(cveMeta)) {
    assert(referenced.has(cve), `cve_meta lists ${cve}, which no advisory references`);
    assert(inRange(meta?.epss, 1) && inRange(meta?.pct, 1) && inRange(meta?.cvss, 10), `cve_meta ${cve} has an out-of-range score`);
    assert(meta?.kev === undefined || typeof meta.kev === "string", `cve_meta ${cve} kev must be a date string`);
  }

  for (const skill of advisorySkills) {
    const overview = read(advisoryPath(skill, "references/kisa-advisories/overview.md"));
    const block = sectionBetween(overview, statsBegin, statsEnd) ?? "";
    const match = block.match(skill.statsPattern);
    assert(
      match && Number(match[1]) === total,
      `${skill.root}/${skill.dir} overview stats do not match ${total} advisories (rerun scripts/build_kisa_advisories.py)`,
    );
  }
});

check("advisory-threat-response-parity", () => {
  const codes = advisorySkills.map((skill) =>
    [...read(advisoryPath(skill, "references/kisa-advisories/threat-response.md")).matchAll(/^### (TR-\d+)/gm)].map((m) => m[1]),
  );
  assert(codes[0].length > 0, "skills/kesekit-advisory threat-response.md has no TR items");
  assertObjectEqual(codes[1], codes[0], "skills-ko/kesekit-advisory-ko threat-response.md TR codes vs EN");
});

check("advisory-runs-setup-gate", () => {
  for (const skill of advisorySkills) {
    const filePath = advisoryPath(skill, "SKILL.md");
    if (!fs.existsSync(filePath)) continue;
    const content = read(filePath);
    const heading = gateHeadings[skill.root];
    assert(content.indexOf(heading) !== -1 && content.indexOf(heading) === content.indexOf("\n## ") + 1,
      `${rel(filePath)} must start with the "${heading}" section`);
    const required = [`\`kesekit:${setupSkillDirs[skill.root]}\``, "`notes.advisory`", "`assessment.scope`", "`project.path`",
      "`assessment.custom`", "`environment`", "--doctor"];
    for (const token of required) {
      assert(content.includes(token), `${rel(filePath)} Step 0 is missing ${token}`);
    }
  }
  for (const skillRoot of skillRoots) {
    assertIncludes(setupPath(skillRoot, "templates", "setup-form.js"), /NOTE_KEYS = \[[^\]]*"advisory"/, "the advisory notes field");
    assertIncludes(setupPath(skillRoot, "references", "profile-schema.md"), "`guide`, `advisory`", "notes.advisory in the schema");
  }
});

check("marketplace-skills-exist", () => {
  const marketplace = JSON.parse(read(path.join(rootDir, ".claude-plugin", "marketplace.json")));
  const listed = marketplace.plugins.flatMap((plugin) => plugin.skills);
  for (const skill of listed) {
    assert(fs.existsSync(path.join(rootDir, skill, "SKILL.md")), `marketplace.json lists ${skill} but its SKILL.md is missing`);
  }
  for (const skill of advisorySkills) {
    assert(listed.includes(`./${skill.root}/${skill.dir}`), `marketplace.json does not list ./${skill.root}/${skill.dir}`);
  }
});

// --- Plugin hooks ---

check("plugin-hooks", () => {
  const hooksPath = path.join(rootDir, "hooks", "hooks.json");
  const scriptPath = path.join(rootDir, "hooks", "security-check-trigger.sh");
  const config = JSON.parse(read(hooksPath));
  const commands = (config.hooks?.UserPromptSubmit ?? []).flatMap((entry) => entry.hooks ?? []).map((hook) => hook.command);
  assert(commands.some((command) => command?.includes("${CLAUDE_PLUGIN_ROOT}/hooks/security-check-trigger.sh")),
    "hooks/hooks.json must run hooks/security-check-trigger.sh on UserPromptSubmit");
  assert(fs.existsSync(scriptPath), "hooks/security-check-trigger.sh is missing");
  if (fs.existsSync(scriptPath)) {
    assert(!fs.readFileSync(scriptPath).includes(0x0d), "hooks/security-check-trigger.sh must use LF line endings");
  }
  assertIncludes(path.join(rootDir, ".gitattributes"), /^\*\.sh\s+text\s+eol=lf$/m, "the *.sh eol=lf rule");
});

if (errors.length > 0) {
  console.error(`Validation failed with ${errors.length} issue(s):`);
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Validated ${checks.length} content checks successfully.`);
