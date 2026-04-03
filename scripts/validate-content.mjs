#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
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

if (errors.length > 0) {
  console.error(`Validation failed with ${errors.length} issue(s):`);
  for (const error of errors) {
    console.error(`- ${error}`);
  }
  process.exit(1);
}

console.log(`Validated ${checks.length} content checks successfully.`);
