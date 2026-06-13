// ==UserScript==
// @name         design-inspect overlay (localhost)
// @namespace    https://github.com/anthropics/claude-skills/design-inspect
// @version      1.0.0
// @description  Auto-loads the design-inspect overlay on Next.js dev servers
// @match        http://localhost:*/*
// @match        http://127.0.0.1:*/*
// @run-at       document-idle
// @grant        none
// ==/UserScript==

/* design-inspect overlay — paste into DevTools Console of a Next.js dev build.
 * Adds a click-to-prompt UI for selecting one or more elements and copying
 *   <file>:<line> (Name) — <prose>                  (single reference)
 * or a References block + prose                       (multiple references)
 * to the clipboard, so you can paste it back into Claude Code.
 *
 * Requires Next.js running in development mode (uses React's __source / _debugSource
 * dev metadata, which is stripped from production builds).
 */
(() => {
  if (window.self !== window.top) return; // don't inject inside iframes (e.g. canvas embeds)
  if (window.__designInspectActive) {
    console.log("[design-inspect] already loaded; toggling inspect.");
    window.__designInspectToggle && window.__designInspectToggle();
    return;
  }
  window.__designInspectActive = true;

  const STYLE_ID = "design-inspect-style";
  const ROOT_ID = "design-inspect-root";

  const CHIP_PALETTE = [
    ["#2563eb", "rgba(37,99,235,.10)"],
    ["#9333ea", "rgba(147,51,234,.10)"],
    ["#16a34a", "rgba(22,163,74,.10)"],
    ["#ea580c", "rgba(234,88,12,.10)"],
  ];

  const BRACKET_SVG = `<svg viewBox="0 0 14 14" width="14" height="14" aria-hidden="true" style="flex:none;display:inline-block;vertical-align:-2px"><path d="M5 3H2v8h3M9 3h3v8H9" fill="none" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>`;

  const style = document.createElement("style");
  style.id = STYLE_ID;
  style.textContent = `
    #${ROOT_ID} { position: fixed; z-index: 2147483647; font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Inter", sans-serif; }
    #${ROOT_ID} .di-toggle { position: fixed; bottom: 16px; right: 16px; background: #111; color: #fff; border: 0; border-radius: 999px; padding: 10px 14px; font-size: 13px; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,.25); }
    #${ROOT_ID} .di-toggle.active { background: #2563eb; }
    #${ROOT_ID} .di-hover-outline { position: fixed; pointer-events: none; border: 2px solid #2563eb; background: rgba(37,99,235,.08); transition: all .04s ease-out; z-index: 2147483646; }
    #${ROOT_ID} .di-hover-label { position: fixed; pointer-events: none; background: #2563eb; color: #fff; padding: 2px 6px; font-size: 11px; font-family: ui-monospace, Menlo, monospace; border-radius: 3px; white-space: nowrap; z-index: 2147483647; }

    #${ROOT_ID} .di-panel { position: fixed; width: 460px; background: #fff; border-radius: 14px; box-shadow: 0 16px 40px rgba(0,0,0,.12), 0 2px 6px rgba(0,0,0,.04); padding: 18px 20px 12px; display: flex; flex-direction: column; gap: 10px; }
    #${ROOT_ID} .di-input { min-height: 84px; max-height: 360px; overflow-y: auto; font-size: 17px; line-height: 1.55; color: #111; outline: none; word-wrap: break-word; }
    #${ROOT_ID} .di-input:empty:before { content: attr(data-placeholder); color: #9ca3af; pointer-events: none; }
    #${ROOT_ID} .di-chip { display: inline-flex; align-items: center; gap: 5px; padding: 1px 8px 2px; border-radius: 6px; font-size: 16px; font-weight: 500; user-select: none; cursor: default; vertical-align: baseline; line-height: 1.5; }
    #${ROOT_ID} .di-chip .di-chip-name { letter-spacing: -0.005em; }
    #${ROOT_ID} .di-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 10px; margin-top: 2px; border-top: 1px solid #f1f1f4; }
    #${ROOT_ID} .di-clear { background: none; border: 0; padding: 4px 2px; font-size: 13px; color: #9ca3af; cursor: pointer; font-family: inherit; }
    #${ROOT_ID} .di-clear:hover { color: #111; }
    #${ROOT_ID} .di-send { height: 32px; border-radius: 999px; border: 0; background: #111; color: #fff; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; padding: 0 14px; font-size: 13px; font-weight: 500; font-family: inherit; transition: background .12s ease; }
    #${ROOT_ID} .di-send:hover { background: #2563eb; }
    #${ROOT_ID} .di-send:disabled { background: #d1d5db; cursor: not-allowed; }
    #${ROOT_ID} .di-toast { position: fixed; bottom: 70px; right: 16px; background: #16a34a; color: #fff; padding: 8px 12px; border-radius: 6px; font-size: 12px; box-shadow: 0 4px 12px rgba(0,0,0,.2); }
  `;
  document.head.appendChild(style);

  const root = document.createElement("div");
  root.id = ROOT_ID;
  document.body.appendChild(root);

  const toggle = document.createElement("button");
  toggle.className = "di-toggle";
  toggle.textContent = "◎ Inspect Mode";
  root.appendChild(toggle);

  let inspecting = false;
  let hoverEl = null;
  let outlineEl = null;
  let labelEl = null;
  let panel = null;

  function getReactFiber(el) {
    const key = Object.keys(el).find(
      (k) => k.startsWith("__reactFiber") || k.startsWith("__reactInternalInstance"),
    );
    return key ? el[key] : null;
  }

  function parseDebugStack(stackErr) {
    // React 19 dev stores a captured Error on fiber._debugStack.
    // Find the first stack frame that looks like project source (not react-dom, next, node_modules).
    if (!stackErr || !stackErr.stack) return null;
    const lines = String(stackErr.stack).split("\n");
    for (const raw of lines) {
      const line = raw.trim();
      // Match common formats:
      //   at fnName (http://localhost:3000/_next/.../file.tsx?...:line:col)
      //   at http://localhost:3000/_next/.../file.tsx:line:col
      const m = line.match(/\(?((?:https?:|file:|webpack:)?[^\s()]+?\.(?:t|j)sx?)(?:\?[^:]*)?:(\d+):(\d+)\)?$/);
      if (!m) continue;
      let url = m[1];
      // Skip framework internals
      if (/\/(react-dom|react|scheduler|next|webpack)\b/.test(url)) continue;
      if (/node_modules/.test(url)) continue;
      // Skip Next.js bundled output (Turbopack/webpack) — line numbers there
      // don't map back to source without manual sourcemap resolution.
      if (/\/_next\/static\/chunks\//.test(url)) continue;
      if (/\._\.js$/.test(url)) continue;
      if (/\/turbopack-runtime/.test(url)) continue;
      // Normalize: strip origin + /_next/ prefixes if present
      try {
        const u = new URL(url, "http://x");
        url = u.pathname;
      } catch {}
      url = url.replace(/^\/_next\/static\/chunks\/?/, "");
      url = url.replace(/^\/_next\//, "");
      return { fileName: url, lineNumber: Number(m[2]), columnNumber: Number(m[3]) };
    }
    return null;
  }

  function getDebugSource(el) {
    let fiber = getReactFiber(el);
    while (fiber) {
      // 1. Legacy React (<19) and classic JSX transform
      if (fiber._debugSource && fiber._debugSource.fileName) {
        return { source: fiber._debugSource, fiber };
      }
      const propSrc = fiber.memoizedProps && fiber.memoizedProps.__source;
      if (propSrc && propSrc.fileName) {
        return { source: propSrc, fiber };
      }
      // 2. React 19 — JSX source is captured as an Error on _debugStack
      const fromStack = parseDebugStack(fiber._debugStack);
      if (fromStack) return { source: fromStack, fiber };
      // 3. Sometimes the owner has the info instead
      if (fiber._debugOwner) {
        const ownerStack = parseDebugStack(fiber._debugOwner._debugStack);
        if (ownerStack) return { source: ownerStack, fiber };
        if (fiber._debugOwner._debugSource && fiber._debugOwner._debugSource.fileName) {
          return { source: fiber._debugOwner._debugSource, fiber };
        }
      }
      fiber = fiber.return;
    }
    return null;
  }

  function getComponentName(fiber) {
    let f = fiber;
    while (f) {
      const t = f.type;
      if (t && (t.displayName || t.name)) return t.displayName || t.name;
      f = f.return;
    }
    return null;
  }

  function shortenPath(p) {
    const markers = ["/app/", "/components/", "/src/", "/pages/", "/lib/"];
    for (const m of markers) {
      const i = p.indexOf(m);
      if (i !== -1) return p.slice(i + 1);
    }
    return p;
  }

  function setInspecting(on) {
    inspecting = on;
    toggle.classList.toggle("active", on);
    toggle.textContent = on ? "◎ Inspecting… (esc to stop)" : "◎ Inspect Mode";
    if (!on) clearHover();
  }

  function clearHover() {
    hoverEl = null;
    if (outlineEl) { outlineEl.remove(); outlineEl = null; }
    if (labelEl) { labelEl.remove(); labelEl = null; }
  }

  function drawHover(el) {
    const rect = el.getBoundingClientRect();
    if (!outlineEl) {
      outlineEl = document.createElement("div");
      outlineEl.className = "di-hover-outline";
      root.appendChild(outlineEl);
    }
    outlineEl.style.left = rect.left + "px";
    outlineEl.style.top = rect.top + "px";
    outlineEl.style.width = rect.width + "px";
    outlineEl.style.height = rect.height + "px";

    const info = getDebugSource(el);
    const fiber = (info && info.fiber) || getReactFiber(el);
    const name = fiber ? getComponentName(fiber) : null;
    const tag = el.tagName.toLowerCase();
    let labelText;
    if (info) {
      labelText = `${name ? name + "  " : ""}${shortenPath(info.source.fileName)}:${info.source.lineNumber}`;
    } else if (name) {
      labelText = `${name}  <${tag}>`;
    } else {
      labelText = `${tag} (no source)`;
    }
    if (!labelEl) {
      labelEl = document.createElement("div");
      labelEl.className = "di-hover-label";
      root.appendChild(labelEl);
    }
    labelEl.textContent = labelText;
    labelEl.style.left = rect.left + "px";
    labelEl.style.top = Math.max(0, rect.top - 18) + "px";
  }

  function onMove(e) {
    if (!inspecting) return;
    const path = e.composedPath ? e.composedPath() : [e.target];
    const target = path.find((n) => n instanceof Element && !root.contains(n));
    if (!target || target === hoverEl) return;
    hoverEl = target;
    drawHover(target);
  }

  function onClick(e) {
    if (!inspecting) return;
    if (root.contains(e.target)) return;
    e.preventDefault();
    e.stopPropagation();
    const el = hoverEl || e.target;
    const info = getDebugSource(el);
    if (panel) {
      addChip(el, info);
    } else {
      openPanel(el, info);
    }
    // Inspect mode stays on so user can keep clicking elements without
    // re-clicking the toggle. Esc or clicking the toggle turns it off.
  }

  function onKey(e) {
    if (e.key === "Escape") {
      if (panel) closePanel();
      else if (inspecting) setInspecting(false);
    }
  }

  function elementFingerprint(el) {
    const tag = el.tagName ? el.tagName.toLowerCase() : "";
    const classAttr = (el.getAttribute && el.getAttribute("class")) || "";
    // textContent flattens descendants; keep it short and single-line.
    const rawText = (el.textContent || "").replace(/\s+/g, " ").trim();
    const text = rawText.length > 140 ? rawText.slice(0, 140) + "…" : rawText;
    // Parent context — useful when the clicked element itself is generic.
    const parent = el.parentElement;
    const parentTag = parent && parent.tagName ? parent.tagName.toLowerCase() : "";
    const parentClass = (parent && parent.getAttribute && parent.getAttribute("class")) || "";
    return { tag, classAttr, text, parentTag, parentClass };
  }

  function buildChipNode(el, info, index) {
    const [color, bg] = CHIP_PALETTE[index % CHIP_PALETTE.length];
    const fiber = (info && info.fiber) || getReactFiber(el);
    const name = fiber ? getComponentName(fiber) : null;
    const file = info ? shortenPath(info.source.fileName) : null;
    const line = info ? info.source.lineNumber : null;
    const fp = elementFingerprint(el);
    const token = name || (file ? `${file}:${line}` : fp.tag || "node");
    const chip = document.createElement("span");
    chip.className = "di-chip";
    chip.contentEditable = "false";
    chip.setAttribute("data-name", name || "");
    chip.setAttribute("data-file", file || "");
    chip.setAttribute("data-line", line == null ? "" : String(line));
    chip.setAttribute("data-token", token);
    chip.setAttribute("data-tag", fp.tag);
    chip.setAttribute("data-classname", fp.classAttr);
    chip.setAttribute("data-text", fp.text);
    chip.setAttribute("data-parent-tag", fp.parentTag);
    chip.setAttribute("data-parent-classname", fp.parentClass);
    chip.style.color = color;
    chip.style.background = bg;
    chip.innerHTML = `${BRACKET_SVG}<span class="di-chip-name"></span>`;
    chip.querySelector(".di-chip-name").textContent = token;
    return chip;
  }

  function addChip(el, info) {
    if (!panel) return;
    const index = panel.chips.length;
    const chip = buildChipNode(el, info, index);

    let range = panel.savedRange;
    if (!range || !panel.input.contains(range.startContainer)) {
      range = document.createRange();
      range.selectNodeContents(panel.input);
      range.collapse(false);
    }

    panel.input.focus();
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);

    range.deleteContents();
    range.insertNode(chip);
    const space = document.createTextNode(" ");
    chip.after(space);

    const after = document.createRange();
    after.setStartAfter(space);
    after.collapse(true);
    sel.removeAllRanges();
    sel.addRange(after);

    panel.chips.push({
      file: chip.getAttribute("data-file"),
      line: chip.getAttribute("data-line"),
      name: chip.getAttribute("data-name"),
      token: chip.getAttribute("data-token"),
      tag: chip.getAttribute("data-tag"),
      classAttr: chip.getAttribute("data-classname"),
      text: chip.getAttribute("data-text"),
      parentTag: chip.getAttribute("data-parent-tag"),
      parentClass: chip.getAttribute("data-parent-classname"),
      node: chip,
    });
    panel.savedRange = after.cloneRange();
  }

  function openPanel(el, info) {
    closePanel();
    const rect = el.getBoundingClientRect();
    const panelEl = document.createElement("div");
    panelEl.className = "di-panel";
    const top = Math.min(window.innerHeight - 220, Math.max(8, rect.bottom + 8));
    const left = Math.min(window.innerWidth - 440, Math.max(8, rect.left));
    panelEl.style.top = top + "px";
    panelEl.style.left = left + "px";

    const input = document.createElement("div");
    input.className = "di-input";
    input.setAttribute("contenteditable", "true");
    input.setAttribute("data-placeholder", "Describe the change… (⏎ to copy, ⇧⏎ for newline)");
    panelEl.appendChild(input);

    const footer = document.createElement("div");
    footer.className = "di-footer";
    const clearBtn = document.createElement("button");
    clearBtn.className = "di-clear";
    clearBtn.type = "button";
    clearBtn.textContent = "Clear";
    clearBtn.title = "Clear the prompt and chips";
    clearBtn.addEventListener("click", () => {
      if (!panel) return;
      panel.input.innerHTML = "";
      panel.chips = [];
      panel.savedRange = null;
      panel.input.focus();
    });
    const send = document.createElement("button");
    send.className = "di-send";
    send.type = "button";
    send.title = "Copy to clipboard (⏎)";
    send.textContent = "Copy to clipboard";
    footer.appendChild(clearBtn);
    footer.appendChild(send);
    panelEl.appendChild(footer);

    root.appendChild(panelEl);

    panel = { el: panelEl, input, chips: [], savedRange: null };

    const saveRange = () => {
      const sel = window.getSelection();
      if (sel && sel.rangeCount && panel && panel.input.contains(sel.anchorNode)) {
        panel.savedRange = sel.getRangeAt(0).cloneRange();
      }
    };
    input.addEventListener("keyup", saveRange);
    input.addEventListener("mouseup", saveRange);
    input.addEventListener("focus", saveRange);

    input.addEventListener("keydown", (e) => {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        submit();
      }
    });
    send.addEventListener("click", submit);

    input.focus();
    const seed = document.createRange();
    seed.selectNodeContents(input);
    seed.collapse(true);
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(seed);
    panel.savedRange = seed.cloneRange();

    addChip(el, info);
    clearHover();
  }

  function serialize(node, parts) {
    if (node.nodeType === Node.TEXT_NODE) {
      parts.push(node.textContent.replace(/ /g, " "));
      return;
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return;
    if (node.classList && node.classList.contains("di-chip")) {
      // For 2+ chip payloads, put a blank line before each non-first chip so
      // each "fingerprint + instruction" block sits on its own line.
      const state = parts.__state;
      if (state && state.totalChips > 1 && state.chipsSeen > 0) {
        while (parts.length && /^\s+$/.test(parts[parts.length - 1])) parts.pop();
        parts.push("\n\n");
      } else {
        const prev = parts.length ? parts[parts.length - 1] : "";
        if (prev && !/\s$/.test(prev)) parts.push(" ");
      }
      if (state) state.chipsSeen++;
      parts.push(chipInlineFormat(node));
      parts.push(" ");
      return;
    }
    if (node.tagName === "BR") {
      parts.push("\n");
      return;
    }
    const blocks = ["DIV", "P", "LI", "BLOCKQUOTE"];
    const isBlock = blocks.includes(node.tagName);
    if (isBlock && parts.length && !parts[parts.length - 1].endsWith("\n")) {
      parts.push("\n");
    }
    node.childNodes.forEach((c) => serialize(c, parts));
    if (isBlock && parts.length && !parts[parts.length - 1].endsWith("\n")) {
      parts.push("\n");
    }
  }

  function chipInlineFormat(node) {
    const tag = node.getAttribute("data-tag") || "";
    const classAttr = node.getAttribute("data-classname") || "";
    const text = node.getAttribute("data-text") || "";
    const name = node.getAttribute("data-name") || "";
    const file = node.getAttribute("data-file") || "";
    const line = node.getAttribute("data-line") || "";
    const cls = classAttr ? ` class="${classAttr}"` : "";
    const tagStr = tag ? `<${tag}${cls}>` : "<node>";
    const textStr = text ? ` "${text}"` : "";
    const head = name
      ? file ? ` [${name} @ ${file}:${line}]` : ` [${name}]`
      : file ? ` [${file}:${line}]` : "";
    return `${tagStr}${textStr}${head}`;
  }

  function buildPayload() {
    if (!panel) return "";
    const parts = [];
    parts.__state = { chipsSeen: 0, totalChips: panel.chips.length };
    panel.input.childNodes.forEach((n) => serialize(n, parts));
    const prose = parts
      .join("")
      .replace(/\n{3,}/g, "\n\n")
      .trim();

    // Inline format: each chip is expanded inline by `serialize`, so the
    // returned prose already contains the fingerprints next to the user's
    // request text. No separate References block.
    return prose;
  }

  function proseHasContent() {
    if (!panel) return false;
    let has = false;
    function walk(node) {
      if (has) return;
      if (node.nodeType === Node.TEXT_NODE) {
        if (node.textContent.trim()) has = true;
        return;
      }
      if (node.nodeType !== Node.ELEMENT_NODE) return;
      if (node.classList && node.classList.contains("di-chip")) return;
      node.childNodes.forEach(walk);
    }
    panel.input.childNodes.forEach(walk);
    return has;
  }

  async function submit() {
    if (!panel) return;
    if (!proseHasContent()) {
      toast("Add a description first");
      return;
    }
    const payload = buildPayload();
    try {
      await navigator.clipboard.writeText(payload);
      toast("Copied — ⌘V in Claude Code");
    } catch {
      const tmp = document.createElement("textarea");
      tmp.value = payload;
      document.body.appendChild(tmp);
      tmp.select();
      try { document.execCommand("copy"); } catch {}
      tmp.remove();
      toast("Copied (fallback) — ⌘V in Claude Code");
    }
    closePanel();
  }

  function closePanel() {
    if (panel) { panel.el.remove(); panel = null; }
  }

  function toast(msg) {
    const t = document.createElement("div");
    t.className = "di-toast";
    t.textContent = msg;
    root.appendChild(t);
    setTimeout(() => t.remove(), 1600);
  }

  toggle.addEventListener("click", () => {
    // Toggle inspect mode without closing an open panel
    setInspecting(!inspecting);
  });

  document.addEventListener("mousemove", onMove, true);
  document.addEventListener("click", onClick, true);
  document.addEventListener("keydown", onKey, true);

  window.__designInspectToggle = () => setInspecting(!inspecting);

  // Diagnostic: call window.__designInspectDebug(document.querySelector("button"))
  // to see what fields are present on the fiber chain — helps when "no source".
  window.__designInspectDebug = (el) => {
    if (!el || !el.nodeType) {
      console.log("pass an element, e.g. document.querySelector('button')");
      return;
    }
    let fiber = getReactFiber(el);
    let depth = 0;
    while (fiber && depth < 12) {
      const t = fiber.type;
      const name = (t && (t.displayName || t.name)) || (typeof t === "string" ? t : String(t));
      console.log(depth, name, {
        _debugSource: fiber._debugSource,
        _debugStack: fiber._debugStack && fiber._debugStack.stack,
        memoizedProps__source: fiber.memoizedProps && fiber.memoizedProps.__source,
        _debugOwner: fiber._debugOwner && {
          name: fiber._debugOwner.type && (fiber._debugOwner.type.displayName || fiber._debugOwner.type.name),
          _debugSource: fiber._debugOwner._debugSource,
          _debugStack: fiber._debugOwner._debugStack && fiber._debugOwner._debugStack.stack,
        },
      });
      fiber = fiber.return;
      depth++;
    }
  };

  console.log(
    "[design-inspect] loaded. Click ◎ Inspect Mode (bottom-right), then click an element. " +
      "Click ◎ again to add more elements before sending.",
  );
})();
