"use strict";

// Run after generating the lesson downloads:
//   node scripts/test_fixtures.cjs
// Executes the actual inline scripts with a small DOM stub. This checks fixture
// behavior, including pageshow restoration, but does not replace browser QA.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const vm = require("node:vm");

const names = [
  "broken-checklist", "correct-checklist", "reset-bug", "correct-reset",
  "search-reset-bug", "correct-search-reset",
];

function eventTarget(properties = {}) {
  const listeners = new Map();
  return Object.assign({
    addEventListener(type, listener) {
      if (!listeners.has(type)) listeners.set(type, []);
      listeners.get(type).push(listener);
    },
    dispatch(type, extra = {}) {
      for (const listener of listeners.get(type) || []) {
        listener({type, target: this, ...extra});
      }
    },
    hasListener(type) { return Boolean(listeners.get(type)?.length); },
  }, properties);
}

function loadFixture(html, filename) {
  const labels = [...html.matchAll(
    /<label>\s*<input type="checkbox">\s*<span>([^<]*)<\/span>\s*<\/label>/g,
  )].map(match => match[1]);
  const scripts = [...html.matchAll(/<script\b[^>]*>([\s\S]*?)<\/script>/gi)];
  assert.equal(scripts.length, 1, "fixture must have one inline script");
  const initialCount = html.match(/id="count">([^<]*)<\/strong>/);
  assert.ok(initialCount, "fixture must contain its completed-count display");
  const boxes = labels.map(text => eventTarget({
    checked: false,
    parentElement: {hidden: false, textContent: text},
  }));
  const count = {textContent: initialCount[1]};
  const reset = eventTarget();
  const search = /id="search"/.test(html) ? eventTarget({value: ""}) : null;
  const window = eventTarget();
  const document = {
    querySelectorAll(selector) {
      assert.equal(selector.replace(/["'\s]/g, ""), "input[type=checkbox]",
        "extend the DOM stub explicitly if fixture selectors change");
      return boxes;
    },
    getElementById(id) {
      const element = {count, reset, search}[id];
      assert.ok(element, `fixture requested unknown element: ${id}`);
      return element;
    },
  };
  new vm.Script(scripts[0][1], {filename}).runInNewContext(
    {document, window}, {timeout: 1000},
  );
  assert.ok(window.hasListener("pageshow"), "restored pages must reset progress");
  assert.ok(reset.hasListener("click"), "reset control must be wired");
  boxes.forEach(box => assert.ok(box.hasListener("change"),
    "every checkbox must update the completed count"));
  return {
    boxes, count, search,
    check(index, checked) {
      boxes[index].checked = checked;
      boxes[index].dispatch("change");
    },
    reset() { reset.dispatch("click"); },
    filter(text) {
      assert.ok(search, "search control is required for this case");
      search.value = text;
      search.dispatch("input");
    },
    restore() { window.dispatch("pageshow", {persisted: true}); },
  };
}

function verifyFixture(name, lang, html) {
  const h = loadFixture(html, `${name}-${lang}.html`);
  const resetOnly = name === "reset-bug" || name === "correct-reset";
  const size = resetOnly ? 2 : 3;
  const omittedFirst = name === "broken-checklist";
  const staleReset = name === "reset-bug";
  const searchBug = name === "search-reset-bug";
  const countIs = (expected, step) => assert.equal(
    String(h.count.textContent), String(expected), `${step}: completed count`,
  );
  const checksAre = (expected, step) => assert.deepEqual(
    h.boxes.map(box => box.checked), expected, `${step}: checkbox state`,
  );
  const visibleCount = () => h.boxes.filter(box => !box.parentElement.hidden).length;

  assert.equal(h.boxes.length, size, "task count");
  countIs(0, "initial load");
  checksAre(Array(size).fill(false), "initial load");
  h.check(0, true);
  countIs(omittedFirst ? 0 : 1, "check first item");
  h.check(1, true);
  countIs(omittedFirst ? 1 : 2, "check first two items");
  h.check(0, false);
  countIs(1, "uncheck first item");
  h.check(0, true);
  h.reset();
  checksAre(Array(size).fill(false), "reset clears checkboxes");
  countIs(staleReset ? 2 : 0, "reset preserves only the intended teaching bug");

  if (name.includes("search")) {
    assert.ok(h.search, "search fixture must have a search control");
    h.check(0, true);
    h.check(2, true);
    countIs(2, "check first and third items");
    h.filter(lang === "en" ? "PROPS" : "道具");
    assert.equal(visibleCount(), 1, "search shows only the matching item");
    countIs(2, "search does not change counting scope");
    h.check(0, false);
    countIs(1, "hidden checked item is still counted");
    h.check(0, true);
    h.reset();
    countIs(searchBug ? 1 : 0, "reset with a hidden checked item");
    checksAre([false, false, searchBug], "hidden-item reset behavior");
    assert.equal(h.search.value, "", "reset clears search");
    assert.equal(visibleCount(), size, "reset reveals all items");
  }

  // Regression: making reset intentionally faulty must not also break init().
  // A BFCache return calls pageshow with existing checked items and a stale count.
  h.boxes.forEach((_box, index) => h.check(index, true));
  if (h.search) h.filter("no matching lesson item");
  h.restore();
  checksAre(Array(size).fill(false), "pageshow clears restored checkboxes");
  countIs(0, "pageshow updates the cleared count, even in reset-bug");
  assert.equal(visibleCount(), size, "pageshow reveals all items");
  if (h.search) assert.equal(h.search.value, "", "pageshow clears search");
}

function main() {
  const directory = process.argv[2]
    ? path.resolve(process.argv[2])
    : path.resolve(__dirname, "..", "downloads", "curriculum");
  let passed = 0;
  let failed = 0;
  for (const lang of ["zh-Hant", "en"]) {
    for (const name of names) {
      const filename = `${name}-${lang}.html`;
      try {
        verifyFixture(name, lang, fs.readFileSync(path.join(directory, filename), "utf8"));
        console.log(`PASS ${filename}`);
        passed++;
      } catch (error) {
        console.error(`FAIL ${filename}\n${error.message}`);
        failed++;
      }
    }
  }
  console.log(`${passed} passed; ${failed} failed (${passed + failed} fixtures).`);
  if (failed) process.exitCode = 1;
}

module.exports = {verifyFixture};
if (require.main === module) main();
