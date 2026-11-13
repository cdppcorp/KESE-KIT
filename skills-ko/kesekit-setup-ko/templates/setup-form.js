// Behavior for setup-form.html. Loaded after setup-i18n.js and setup-data.js.
(function () {
  "use strict";

  const BEGIN_MARKER = "KESEKIT_PROFILE_INPUT v1";
  const END_MARKER = "END_KESEKIT_PROFILE_INPUT";
  const DOWNLOAD_NAME = "kesekit-profile-input.txt";
  const MAX_NOTE = 2000;
  const MAX_CUSTOM = 300;
  const MAX_TEXT = 200;
  const MAX_PATH = 500;
  const MAX_REMOTE = 300;
  const MAX_ITEM = 80;
  const MAX_ITEMS = 50;
  const NOTE_KEYS = ["common", "start", "check", "fix", "guide"];
  const ENV_KEYS = ["languages", "frameworks", "services", "webServers", "databases", "containers", "cloudClis", "aiLibraries"];
  const CHOICE_KEYS = ["purpose", "scope", "domains", "ciiTargets", "ztTargetMaturity", "organizationType"];
  const MULTI_KEYS = ["scope", "domains", "ciiTargets"];
  const FALLBACK = { purpose: "general", scope: ["host"], domains: ["cii"], ztTargetMaturity: "initial", organizationType: "" };
  // Absolute local paths only: a drive path or a POSIX root, never a UNC/network path.
  const ABSOLUTE_PATH = /^(?:[A-Za-z]:[\\/]|\/(?!\/))/;
  // Characters that would break single-quoted shell arguments or folder-name searches.
  const UNSAFE_PATH = /['"`\u0000-\u001f]/;
  const UNSAFE_NAME = /['"`*?[\]\\/\u0000-\u001f]/;
  const REMOTE_URL = /^(?:(?:https?|ssh|git):\/\/\S+|[\w.-]+@[\w.-]+:\S+)$/i;
  const ENUMS = JSON.parse(document.getElementById("kesekit-enums").textContent);
  const DETECT = JSON.parse(document.getElementById("kesekit-detect").textContent);
  const MANIFEST_NAMES = new Set(DETECT.manifests.filter((name) => !name.startsWith("*")));
  const MANIFEST_SUFFIXES = DETECT.manifests.filter((name) => name.startsWith("*")).map((name) => name.slice(1));

  const I18N = window.KESEKIT_I18N;
  if (!isPlainObject(I18N) || !isPlainObject(I18N.ko) || !isPlainObject(I18N.en)) {
    document.body.replaceChildren(Object.assign(document.createElement("p"), {
      textContent: "setup-i18n.js를 불러오지 못했습니다. Claude에게 화면을 다시 열어 달라고 하세요. / Could not load setup-i18n.js. Ask Claude to reopen this page."
    }));
    return;
  }

  const setup = isPlainObject(window.KESEKIT_SETUP) ? window.KESEKIT_SETUP : null;
  const detected = isPlainObject(setup && setup.detected) ? setup.detected : {};
  const previous = isPlainObject(setup && setup.previous) ? setup.previous : null;
  let lang = pickLang();
  let showErrors = false;
  let projectPanelOpen = false;
  let picked = null;
  let pickStatus = { key: "", tone: "", name: "" };

  function isPlainObject(value) {
    return value !== null && typeof value === "object" && !Array.isArray(value);
  }

  function dig(source, path) {
    return path.split(".").reduce((node, key) => (isPlainObject(node) ? node[key] : undefined), source);
  }

  function text(value) {
    return typeof value === "string" ? value.trim() : (typeof value === "number" ? String(value) : "");
  }

  function list(value) {
    if (!Array.isArray(value)) return [];
    const items = value.map(text).filter(Boolean).map((item) => item.slice(0, MAX_ITEM));
    return Array.from(new Set(items)).slice(0, MAX_ITEMS);
  }

  function asList(value) {
    return Array.isArray(value) ? value : (value ? [value] : []);
  }

  function allowed(value, key) {
    return ENUMS[key].includes(value) ? value : "";
  }

  function allowedList(value, key) {
    return list(value).filter((item) => ENUMS[key].includes(item));
  }

  // Drops everything up to the last "@" of the authority (user:password, tokens) and any query/fragment.
  function stripCredentials(url) {
    return text(url).replace(/^([a-z][a-z0-9+.-]*:\/\/)[^/\s]*@/i, "$1").replace(/[?#].*$/, "");
  }

  function pickLang() {
    const requested = text(setup && setup.lang);
    if (requested === "ko" || requested === "en") return requested;
    return (navigator.language || "").toLowerCase().startsWith("ko") ? "ko" : "en";
  }

  function t(key) {
    const value = dig(I18N[lang], key);
    return typeof value === "string" ? value : key;
  }

  function make(tag, props, children) {
    const node = document.createElement(tag);
    Object.entries(props || {}).forEach(([key, value]) => {
      if (key === "text") node.textContent = value;
      else if (key in node && key !== "list") node[key] = value;
      else node.setAttribute(key, value);
    });
    (children || []).forEach((child) => node.appendChild(child));
    return node;
  }

  function labelOf(key, value) {
    return asList(value).map((item) => t("enum." + key + "." + item)).join(", ");
  }

  function detectedRole() {
    return allowed(dig(detected, "system.role"), "role") || "other";
  }

  function osTarget() {
    if (detectedRole() === "dev-pc") return "pc";
    return text(dig(detected, "system.os")) === "windows" ? "windows" : "unix";
  }

  function detectedEnv(key) {
    return list(dig(detected, "environment." + key));
  }

  function effectiveEnv(entry, key) {
    return entry.mode === "auto" ? detectedEnv(key) : list(entry.selected.concat(entry.extra.split(",")));
  }

  function recommendedFor(key) {
    const raw = dig(detected, "recommended." + key);
    if (MULTI_KEYS.includes(key)) {
      const values = allowedList(raw, key);
      if (values.length > 0) return values;
      return key === "ciiTargets" ? [osTarget()] : FALLBACK[key];
    }
    return allowed(raw, key) || FALLBACK[key];
  }

  function initialState() {
    const prevOr = (path, fallback) => (previous ? dig(previous, path) : undefined) ?? fallback;
    const prevSource = isPlainObject(dig(previous, "assessment.source")) ? previous.assessment.source : {};
    const choices = {};
    const custom = {};
    CHOICE_KEYS.forEach((key) => {
      const restored = prevSource[key] === "selected";
      const raw = dig(previous, "assessment." + key);
      choices[key] = MULTI_KEYS.includes(key) ? (restored ? allowedList(raw, key) : []) : (restored ? allowed(raw, key) : "");
      custom[key] = text(dig(previous, "assessment.custom." + key)).slice(0, MAX_CUSTOM);
    });
    const prevEnvSource = isPlainObject(dig(previous, "environmentSource")) ? previous.environmentSource : {};
    const environment = {};
    ENV_KEYS.forEach((key) => {
      const manual = prevEnvSource[key] === "manual";
      environment[key] = { mode: manual ? "manual" : "auto", selected: manual ? list(dig(previous, "environment." + key)) : [], extra: "" };
    });
    const notes = {};
    NOTE_KEYS.forEach((key) => { notes[key] = text(prevOr("notes." + key, "")).slice(0, MAX_NOTE); });
    const memory = dig(detected, "system.memoryGb") ?? prevOr("system.memoryGb", "");
    const roleEdited = dig(previous, "system.roleEdited") === true;
    const remoteEdited = dig(previous, "project.gitRemoteEdited") === true;
    return {
      project: {
        path: text(dig(detected, "project.path")),
        gitRemote: remoteEdited ? stripCredentials(dig(previous, "project.gitRemote")) : text(dig(detected, "project.gitRemote"))
      },
      system: {
        osVersion: text(dig(detected, "system.osVersion") ?? prevOr("system.osVersion", "")),
        cpu: text(dig(detected, "system.cpu") ?? prevOr("system.cpu", "")),
        memoryGb: typeof memory === "number" && Number.isFinite(memory) ? String(Math.max(0, Math.round(memory))) : text(memory),
        role: roleEdited ? allowed(dig(previous, "system.role"), "role") : ""
      },
      environment: environment,
      choices: choices,
      custom: custom,
      notes: notes
    };
  }

  function renderStaticText() {
    document.documentElement.lang = lang;
    document.title = t("title");
    document.querySelectorAll("[data-i18n]").forEach((node) => { node.textContent = t(node.dataset.i18n); });
    document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => { node.placeholder = t(node.dataset.i18nPlaceholder); });
    CHOICE_KEYS.forEach((key) => { document.getElementById("custom-" + key).placeholder = t("customPlaceholder." + key); });
    document.getElementById("lang-toggle").textContent = t("langToggle");
  }

  function renderFacts(container, rows) {
    container.replaceChildren();
    rows.forEach(([label, value, changed]) => {
      const dd = make("dd", { text: value });
      if (changed) dd.appendChild(make("span", { className: "changed", text: t("changed") }));
      container.appendChild(make("dt", { text: label }));
      container.appendChild(dd);
    });
  }

  function factValue(value) {
    if (value === true) return t("yes");
    if (value === false) return t("no");
    if (Array.isArray(value)) return value.length ? list(value).join(", ") : t("none");
    return text(value) || t("unknown");
  }

  function renderReasons() {
    const reasons = Array.isArray(setup && setup.reasons) ? setup.reasons.filter(isPlainObject) : [];
    const listNode = document.getElementById("reason-list");
    listNode.replaceChildren();
    reasons.forEach((reason) => {
      const item = make("li", {}, [make("strong", { text: t("reason." + text(reason.code)) })]);
      const detail = text(reason.detail);
      if (detail) item.appendChild(document.createTextNode(" " + detail));
      listNode.appendChild(item);
    });
    document.getElementById("reasons").hidden = reasons.length === 0;
    document.getElementById("load-error").hidden = setup !== null;
    ["copy-btn", "download-btn"].forEach((id) => { document.getElementById(id).disabled = setup === null; });
  }

  function renderDetectErrors() {
    const errors = list(detected.errors);
    const box = document.getElementById("detect-errors");
    box.querySelector("ul").replaceChildren(...errors.map((item) => make("li", { text: item })));
    box.hidden = errors.length === 0;
  }

  function renderRole(selected) {
    const select = document.getElementById("role");
    select.replaceChildren(make("option", { value: "", text: t("auto.recommended") + " (" + t("enum.role." + detectedRole()) + ")" }));
    ENUMS.role.forEach((value) => select.appendChild(make("option", { value: value, text: t("enum.role." + value) })));
    select.value = selected || "";
  }

  function renderChoices(key, selected) {
    const container = document.querySelector("#fs-" + key + " .options");
    const multi = MULTI_KEYS.includes(key);
    const chosen = new Set(multi ? selected : [selected]);
    const suggested = new Set(asList(recommendedFor(key)));
    const option = (value, label, extraClass, isSuggested) => {
      const input = make("input", { type: multi ? "checkbox" : "radio", name: key, value: value, checked: chosen.has(value) });
      const children = [input, make("span", { text: label })];
      if (isSuggested) children.push(make("span", { className: "badge", text: t("recommended") }));
      return make("label", { className: "option" + extraClass }, children);
    };
    container.replaceChildren();
    if (!multi) {
      const auto = key === "organizationType" ? t("auto.none") : t("auto.recommended") + " (" + labelOf(key, recommendedFor(key)) + ")";
      container.appendChild(option("", auto, " auto", false));
    }
    ENUMS[key].forEach((value) => container.appendChild(option(value, t("enum." + key + "." + value), "", suggested.has(value))));
  }

  // Each environment list is a multi-select dropdown. "auto" uses the detected values;
  // touching any checkbox or the extra field switches it to "manual".
  function renderEnvFields(environment) {
    const container = document.getElementById("env-fields");
    container.replaceChildren();
    ENV_KEYS.forEach((key) => {
      const entry = environment[key];
      const found = detectedEnv(key);
      const checked = new Set(entry.mode === "auto" ? found : entry.selected);
      const menu = make("div", { className: "menu" }, [
        make("div", {}, [make("button", { type: "button", className: "ghost", text: t("envResetAuto"), "data-env-auto": key })])
      ]);
      list(DETECT.envOptions[key].concat(found, entry.selected)).forEach((value) => {
        const children = [make("input", { type: "checkbox", value: value, checked: checked.has(value) }), make("span", { text: value })];
        if (found.includes(value)) children.push(make("span", { className: "badge", text: t("envDetected") }));
        menu.appendChild(make("label", { className: "check" }, children));
      });
      const extra = make("input", { className: "env-extra", value: entry.extra, placeholder: t("envExtraPlaceholder"), maxLength: MAX_CUSTOM, autocomplete: "off" });
      menu.appendChild(make("label", { className: "custom-row" }, [make("span", { text: t("envExtra") }), extra]));
      const details = make("details", { className: "multi", id: "env-" + key }, [make("summary"), menu]);
      details.dataset.mode = entry.mode;
      container.appendChild(make("div", { className: "field", id: "f-env-" + key }, [make("span", { text: t("env." + key) }), details]));
    });
  }

  function renderEnvSummaries(state) {
    const pathChanged = projectChanged(state).path;
    ENV_KEYS.forEach((key) => {
      const entry = state.environment[key];
      const auto = entry.mode === "auto";
      const values = effectiveEnv(entry, key);
      const label = auto && pathChanged ? t("envPending") : (values.length ? values.join(", ") : t("none"));
      document.querySelector("#env-" + key + " > summary").replaceChildren(
        make("span", { className: auto ? "mode" : "mode manual", text: t(auto ? "envAuto" : "envManual") }),
        document.createTextNode(label));
    });
  }

  function resetEnvToAuto(key) {
    const details = document.getElementById("env-" + key);
    const found = new Set(detectedEnv(key));
    details.dataset.mode = "auto";
    details.querySelectorAll(".check input").forEach((input) => { input.checked = found.has(input.value); });
    details.querySelector(".env-extra").value = "";
    refresh();
  }

  function renderNotes(notes) {
    const container = document.getElementById("notes-fields");
    container.replaceChildren();
    NOTE_KEYS.forEach((key) => {
      const [label, placeholder] = I18N[lang].note[key];
      const area = make("textarea", { id: "note-" + key, maxLength: MAX_NOTE, placeholder: placeholder, value: notes[key], rows: 2 });
      container.appendChild(make("label", { className: "field" }, [make("span", { text: label }), area]));
    });
  }

  function setProjectPanel(open) {
    projectPanelOpen = open;
    document.getElementById("project-edit").hidden = !open;
    const button = document.getElementById("project-edit-btn");
    button.textContent = t(open ? "projectEditClose" : "projectEdit");
    button.setAttribute("aria-expanded", open ? "true" : "false");
  }

  function render(state) {
    renderStaticText();
    renderReasons();
    renderDetectErrors();
    renderFacts(document.getElementById("system-facts"), ["os", "hostname", "arch", "remoteSession"].map(
      (key) => [t("fact." + key), factValue(dig(detected, "system." + key)), false]));
    document.getElementById("osVersion").value = state.system.osVersion;
    document.getElementById("cpu").value = state.system.cpu;
    document.getElementById("memoryGb").value = state.system.memoryGb;
    document.getElementById("projectPath").value = state.project.path;
    document.getElementById("gitRemote").value = state.project.gitRemote;
    renderRole(state.system.role);
    renderEnvFields(state.environment);
    CHOICE_KEYS.forEach((key) => {
      renderChoices(key, state.choices[key]);
      document.getElementById("custom-" + key).value = state.custom[key];
    });
    renderNotes(state.notes);
    renderPickStatus();
    const changed = projectChanged(state);
    setProjectPanel(projectPanelOpen || changed.path || changed.gitRemote);
    refresh();
  }

  function checkedValues(key) {
    return Array.from(document.querySelectorAll("#fs-" + key + " .options input:checked")).map((input) => input.value);
  }

  function collect() {
    const environment = {};
    ENV_KEYS.forEach((key) => {
      const details = document.getElementById("env-" + key);
      environment[key] = {
        mode: details.dataset.mode === "manual" ? "manual" : "auto",
        selected: Array.from(details.querySelectorAll(".check input:checked")).map((input) => input.value),
        extra: details.querySelector(".env-extra").value.trim()
      };
    });
    const projectPath = document.getElementById("projectPath").value.trim();
    const notes = {};
    NOTE_KEYS.forEach((key) => { notes[key] = document.getElementById("note-" + key).value.trim(); });
    const choices = {};
    const custom = {};
    CHOICE_KEYS.forEach((key) => {
      const values = checkedValues(key);
      choices[key] = MULTI_KEYS.includes(key) ? values : (values[0] || "");
      custom[key] = document.getElementById("custom-" + key).value.trim();
    });
    return {
      project: {
        path: projectPath,
        gitRemote: document.getElementById("gitRemote").value.trim(),
        picked: picked !== null && projectPath === picked.name ? picked : null
      },
      system: {
        osVersion: document.getElementById("osVersion").value.trim(),
        cpu: document.getElementById("cpu").value.trim(),
        memoryGb: document.getElementById("memoryGb").value.trim(),
        role: document.getElementById("role").value
      },
      environment: environment,
      choices: choices,
      custom: custom,
      notes: notes
    };
  }

  function projectChanged(state) {
    return {
      path: state.project.path !== text(dig(detected, "project.path")),
      gitRemote: stripCredentials(state.project.gitRemote) !== stripCredentials(dig(detected, "project.gitRemote"))
    };
  }

  // Order of precedence: checked options, then free text (Claude maps it), then the suggestion.
  function resolve(state) {
    const values = {};
    const source = {};
    CHOICE_KEYS.forEach((key) => {
      const chosen = state.choices[key];
      if (asList(chosen).length > 0) {
        values[key] = chosen;
        source[key] = "selected";
      } else if (state.custom[key]) {
        values[key] = null;
        source[key] = "custom";
      } else {
        const suggestion = recommendedFor(key);
        values[key] = asList(suggestion).length > 0 ? suggestion : null;
        source[key] = values[key] === null ? null : "recommended";
      }
    });
    const domains = values.domains;
    if (Array.isArray(domains) && !domains.includes("cii")) { values.ciiTargets = []; source.ciiTargets = null; }
    if (Array.isArray(domains) && !domains.includes("zero-trust")) { values.ztTargetMaturity = null; source.ztTargetMaturity = null; }
    return { values: values, source: source };
  }

  function renderProjectFacts(state) {
    const changed = projectChanged(state);
    const chosen = state.project.picked;
    const pathLabel = chosen ? chosen.name + " (" + t("pick.nameOnly") + ")" : state.project.path;
    let manifests = factValue(dig(detected, "project.manifests"));
    if (chosen) manifests = factValue(chosen.manifests);
    else if (changed.path) manifests = t("manifestsPending");
    renderFacts(document.getElementById("project-facts"), [
      [t("fact.path"), pathLabel || t("unknown"), changed.path],
      [t("fact.gitRemote"), stripCredentials(state.project.gitRemote) || t("none"), changed.gitRemote],
      [t("fact.manifests"), manifests, false]
    ]);
  }

  function renderPreviews(state, resolved) {
    CHOICE_KEYS.forEach((key) => {
      const value = resolved.values[key];
      const origin = resolved.source[key];
      let message;
      if (origin === "custom") message = t("preview.custom");
      else if (origin === null || asList(value).length === 0) message = t("preview.none");
      else if (origin === "recommended") message = labelOf(key, value) + " " + t("preview.recommended");
      else message = labelOf(key, value) + (state.custom[key] ? " " + t("preview.withCustom") : "");
      document.getElementById("preview-" + key).replaceChildren(make("strong", { text: t("preview.prefix") }), document.createTextNode(message));
    });
    const domains = resolved.values.domains;
    document.getElementById("fs-ciiTargets").hidden = Array.isArray(domains) && !domains.includes("cii");
    document.getElementById("fs-ztTargetMaturity").hidden = Array.isArray(domains) && !domains.includes("zero-trust");
  }

  function validate(state) {
    const errors = [];
    const add = (target, message) => errors.push({ target: target, message: message });
    const tooLong = (label, max) => t("err.tooLong").replace("{field}", label).replace("{max}", max);
    const path = state.project.path;
    const pickedName = state.project.picked !== null;
    if (pickedName ? UNSAFE_NAME.test(path) : UNSAFE_PATH.test(path)) add("f-projectPath", t("err.pathChars"));
    else if (!pickedName && !ABSOLUTE_PATH.test(path)) add("f-projectPath", t("err.projectPath"));
    else if (path.length > MAX_PATH) add("f-projectPath", tooLong(t("field.projectPath"), MAX_PATH));
    const remote = state.project.gitRemote;
    if (remote && (remote.length > MAX_REMOTE || !REMOTE_URL.test(remote))) add("f-gitRemote", t("err.gitRemote"));
    if (state.system.memoryGb !== "" && !/^\d{1,6}$/.test(state.system.memoryGb)) add("f-memoryGb", t("err.memoryGb"));
    ["osVersion", "cpu"].forEach((key) => {
      if (state.system[key].length > MAX_TEXT) add("f-" + key, tooLong(t("field." + key), MAX_TEXT));
    });
    CHOICE_KEYS.forEach((key) => {
      if (state.custom[key].length > MAX_CUSTOM) add("fs-" + key, tooLong(t("legend." + key), MAX_CUSTOM));
    });
    NOTE_KEYS.forEach((key) => {
      if (state.notes[key].length > MAX_NOTE) add("notes-fields", tooLong(I18N[lang].note[key][0], MAX_NOTE));
    });
    return errors;
  }

  function buildPayload(state) {
    const resolved = resolve(state);
    return {
      meta: {
        projectPath: text(dig(detected, "project.path")) || null,
        generatedAt: text(setup && setup.generatedAt) || null,
        lang: lang
      },
      project: {
        path: state.project.path,
        gitRemote: stripCredentials(state.project.gitRemote) || null,
        gitRemoteEdited: projectChanged(state).gitRemote,
        picked: state.project.picked ? { name: state.project.picked.name, manifests: state.project.picked.manifests } : null
      },
      system: {
        osVersion: state.system.osVersion || null,
        cpu: state.system.cpu || null,
        memoryGb: state.system.memoryGb === "" ? null : Number(state.system.memoryGb),
        role: state.system.role || detectedRole(),
        roleEdited: state.system.role !== ""
      },
      environment: Object.fromEntries(ENV_KEYS.map((key) => [key, effectiveEnv(state.environment[key], key)])),
      environmentSource: Object.fromEntries(ENV_KEYS.map((key) => [key, state.environment[key].mode])),
      assessment: Object.assign({}, resolved.values, { source: resolved.source, custom: state.custom }),
      notes: state.notes
    };
  }

  function buildBlock(state) {
    return BEGIN_MARKER + "\n" + JSON.stringify(buildPayload(state), null, 2) + "\n" + END_MARKER;
  }

  function markNeeds(errors) {
    const targets = new Set(errors.map((error) => error.target));
    document.querySelectorAll("fieldset[id], .field[id]").forEach((node) => {
      const needs = targets.has(node.id);
      node.dataset.needs = needs ? "true" : "false";
      node.setAttribute("aria-invalid", needs ? "true" : "false");
      if (node.firstElementChild) node.firstElementChild.dataset.needsLabel = t("needsInput");
    });
  }

  function renderErrors(errors) {
    const box = document.getElementById("errors");
    box.replaceChildren(...errors.map((error) => make("li", { text: error.message })));
    box.hidden = !showErrors || errors.length === 0;
  }

  function refresh() {
    const state = collect();
    renderProjectFacts(state);
    renderEnvSummaries(state);
    renderPreviews(state, resolve(state));
    const errors = validate(state);
    markNeeds(errors);
    renderErrors(errors);
    document.getElementById("output").value = errors.length === 0 && setup !== null ? buildBlock(state) : "";
    return { state: state, errors: errors };
  }

  function setStatus(message, tone) {
    const node = document.getElementById("status");
    node.textContent = message;
    node.dataset.tone = tone;
  }

  function readyBlock() {
    if (setup === null) return null;
    showErrors = true;
    const result = refresh();
    if (result.errors.length > 0) {
      setStatus("", "");
      const target = result.errors[0].target;
      if (target === "f-projectPath" || target === "f-gitRemote") setProjectPanel(true);
      const first = document.getElementById(target);
      if (first) first.scrollIntoView({ behavior: "smooth", block: "center" });
      return null;
    }
    return buildBlock(result.state);
  }

  async function copyBlock() {
    const block = readyBlock();
    if (!block) return;
    try {
      await navigator.clipboard.writeText(block);
      setStatus(t("copied"), "ok");
    } catch (clipboardError) {
      const output = document.getElementById("output");
      output.focus();
      output.select();
      let copied = false;
      try { copied = document.execCommand("copy"); } catch (execError) { copied = false; }
      setStatus(copied ? t("copied") : t("copyFailed"), copied ? "ok" : "warn");
    }
  }

  function downloadBlock() {
    const block = readyBlock();
    if (!block) return;
    const url = URL.createObjectURL(new Blob([block + "\n"], { type: "text/plain;charset=utf-8" }));
    const link = make("a", { href: url, download: DOWNLOAD_NAME });
    document.body.appendChild(link);
    link.click();
    link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setStatus(t("downloaded"), "ok");
  }

  function renderPickStatus() {
    const node = document.getElementById("pick-status");
    node.textContent = pickStatus.key ? t(pickStatus.key).replace("{name}", pickStatus.name) : "";
    node.dataset.tone = pickStatus.tone;
  }

  function setPickStatus(key, tone, name) {
    pickStatus = { key: key, tone: tone, name: name || "" };
    renderPickStatus();
  }

  function isManifest(name) {
    return MANIFEST_NAMES.has(name) || MANIFEST_SUFFIXES.some((suffix) => name.endsWith(suffix));
  }

  // Reads entry names only (root and one level down), mirroring the manifest rule in detection.md.
  async function scanManifests(root) {
    const found = [];
    let partial = false;
    const visit = async (dir, prefix, depth) => {
      try {
        for await (const [name, entry] of dir.entries()) {
          if (found.length >= MAX_ITEMS) return;
          if (entry.kind === "file" && isManifest(name)) found.push(prefix + name);
          else if (entry.kind === "directory" && depth === 0 && !DETECT.excludedDirs.includes(name)) await visit(entry, name + "/", 1);
        }
      } catch (readError) {
        partial = true;
      }
    };
    await visit(root, "", 0);
    return { manifests: found.sort(), partial: partial };
  }

  // The browser exposes only the folder name, never its absolute path; Claude resolves the path later.
  async function pickFolder() {
    if (typeof window.showDirectoryPicker !== "function") {
      setPickStatus("pick.unsupported", "warn");
      return;
    }
    let handle;
    try {
      handle = await window.showDirectoryPicker({ id: "kesekit-project", mode: "read" });
    } catch (pickError) {
      if (!pickError || pickError.name !== "AbortError") setPickStatus("pick.failed", "warn");
      return;
    }
    const scan = await scanManifests(handle);
    picked = { name: handle.name, manifests: scan.manifests };
    document.getElementById("projectPath").value = handle.name;
    setPickStatus(scan.partial ? "pick.partial" : "pick.done", scan.partial ? "warn" : "ok", handle.name);
    refresh();
  }

  function resetProject() {
    picked = null;
    setPickStatus("", "");
    document.getElementById("projectPath").value = text(dig(detected, "project.path"));
    document.getElementById("gitRemote").value = text(dig(detected, "project.gitRemote"));
    refresh();
  }

  function onFormEdit(event) {
    const details = event.target.closest ? event.target.closest("details.multi") : null;
    if (details) details.dataset.mode = "manual";
    if (event.target.id === "projectPath" && picked !== null && event.target.value.trim() !== picked.name) {
      picked = null;
      setPickStatus("", "");
    }
    refresh();
  }

  const form = document.getElementById("setup-form");
  form.addEventListener("input", onFormEdit);
  form.addEventListener("change", onFormEdit);
  form.addEventListener("submit", (event) => event.preventDefault());
  document.getElementById("pick-folder-btn").addEventListener("click", pickFolder);
  document.getElementById("env-fields").addEventListener("click", (event) => {
    const button = event.target.closest("[data-env-auto]");
    if (button) resetEnvToAuto(button.dataset.envAuto);
  });
  document.addEventListener("click", (event) => {
    document.querySelectorAll("details.multi[open]").forEach((node) => { if (!node.contains(event.target)) node.open = false; });
  });
  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") return;
    document.querySelectorAll("details.multi[open]").forEach((node) => {
      node.open = false;
      node.querySelector("summary").focus();
    });
  });
  document.getElementById("copy-btn").addEventListener("click", copyBlock);
  document.getElementById("download-btn").addEventListener("click", downloadBlock);
  document.getElementById("project-edit-btn").addEventListener("click", () => setProjectPanel(!projectPanelOpen));
  document.getElementById("project-reset-btn").addEventListener("click", resetProject);
  document.getElementById("lang-toggle").addEventListener("click", () => {
    const state = collect();
    lang = lang === "ko" ? "en" : "ko";
    render(state);
  });

  render(initialState());
})();
