(() => {
  "use strict";
  const courseNode = document.getElementById("course-data");
  if (!courseNode) return;
  const lang = document.documentElement.lang;
  const course = JSON.parse(courseNode.textContent).locales[lang];
  const ui = JSON.parse(document.getElementById("course-ui").textContent)[lang];
  const base = JSON.parse(document.getElementById("seminar-data").textContent).locales[lang];
  const $ = id => document.getElementById(id);
  const all = selector => [...document.querySelectorAll(selector)];
  const say = (id, text) => { $(id).textContent = text; };
  async function copy(text, status) {
    $("copy-fallback").hidden = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(text);
      say(status, ui.copied);
    } catch {
      $("manual-copy").value = text;
      $("copy-fallback").hidden = false;
      say(status, base.copyManual);
      $("manual-copy").focus();
      $("manual-copy").select();
    }
  }
  all("[data-copy-lesson]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.copyLesson;
    const lesson = course.lessons.find(item => item.key === key);
    const sources = Object.fromEntries(base.sources.map(source => [source.key, source]));
    const pack = key === "gmail" ? [sources.A] : key === "drive" ? [course.sourceD, sources.B] : [sources.C];
    copy(pack.map(source => `${source.label}\n${source.text}`).join("\n\n") + "\n\n" + lesson.prompt, `copy-${key}-status`);
  }));
  all("[data-check-lesson]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.checkLesson;
    const answer = document.querySelector(`input[name="lesson-${key}"]:checked`);
    const lesson = course.lessons.find(item => item.key === key);
    if (!answer) { say(`question-${key}-feedback`, ui.choose_first); return; }
    const correct = Number(answer.value) === lesson.practiceAnswer;
    say(`question-${key}-feedback`, `${correct ? ui.correct : ui.incorrect} ${lesson.practiceExplanation}`);
  }));
  $("check-mistakes").addEventListener("click", () => {
    const correct = course.mistakeExercise.choices.every(choice => document.querySelector(`[data-mistake="${choice.key}"]`).checked === choice.correct);
    say("mistake-feedback", `${correct ? ui.mistake_correct : ui.mistake_retry} ${course.mistakeExercise.explanation}`);
  });
  all("[data-copy-next]").forEach(button => button.addEventListener("click", () => {
    const index = Number(button.dataset.copyNext);
    copy(course.continueSteps[index].prompt, `next-${index}-status`);
  }));
  const safe = value => String(value).replace(/[&<>"']/g, character => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}[character]));
  let built = null;
  function dirty() {
    built = null;
    $("download-tool").disabled = true;
    say("tool-status", ui.tool_dirty);
  }
  $("tool-title").addEventListener("input", dirty);
  $("tool-items").addEventListener("input", dirty);
  function lines(value) {
    return value.split(/\r?\n/).map(line => line.replace(/^\s*(?:[-*]\s+|•\s*|\d+[.)]\s+|\d+、\s*)/, "").trim()).filter(Boolean);
  }
  $("use-result").addEventListener("click", () => {
    if ($("tool-items").value.trim()) { say("tool-status", ui.tool_has_items); return; }
    const result = $("learner-result").value.trim();
    if (!result) { say("tool-status", ui.tool_no_result); return; }
    $("tool-items").value = lines(result).join("\n");
    dirty();
    say("tool-status", ui.tool_imported);
  });
  $("load-tool-example").addEventListener("click", () => {
    if ($("tool-items").value.trim()) { say("tool-status", ui.tool_has_items); return; }
    $("tool-items").value = lang === "en"
      ? "Reply with party size by 11/18 at 18:00 (A)\nDownload tickets by 11/19 at 20:00 (B)\nPack rain gear and charging cables by 11/20 at 21:00 (C)\nAsk the inn about check-in time before departure (A, C; exact deadline to confirm)"
      : "11/18 18:00 前回覆抵達人數（A）\n11/19 20:00 前下載車票（B）\n11/20 21:00 前整理雨具與充電線（C）\n出發前向旅店詢問入住時間（A、C；確切期限待確認）";
    dirty();
    say("tool-status", ui.sample_note);
  });
  function artifact(title, tasks) {
    const labels = tasks.map((task, i) => `<li><label><input type="checkbox" id="task-${i}"><span>${safe(task)}</span></label></li>`).join("");
    const script = '(()=>{const boxes=[...document.querySelectorAll("input[type=checkbox]")];const count=document.getElementById("count");function update(){count.textContent=boxes.filter(box=>box.checked).length;}boxes.forEach(box=>box.addEventListener("change",update));document.getElementById("reset").addEventListener("click",()=>{boxes.forEach(box=>{box.checked=false;});update();});update();})();';
    return `<!doctype html><html lang="${lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; form-action 'none'; base-uri 'none'"><title>${safe(title)}</title><style>*{box-sizing:border-box}body{font:16px/1.7 system-ui,sans-serif;color:#202124;max-width:760px;margin:auto;padding:24px;background:#fff}h1{font-size:26px;line-height:1.5;overflow-wrap:anywhere}ul{list-style:none;margin:20px 0;padding:0}li{border-bottom:1px solid #dfe3e8}label{display:flex;gap:12px;align-items:flex-start;padding:14px 0;cursor:pointer}input{width:22px;height:22px;margin-top:3px;flex-shrink:0;accent-color:#2458a6}span{overflow-wrap:anywhere}button{font:inherit;border:1px solid #2458a6;background:#fff;color:#2458a6;padding:10px 16px;min-height:44px;cursor:pointer}button:focus-visible,input:focus-visible{outline:2px solid #2458a6;outline-offset:3px}.note{font-size:13px;color:#68707b}</style></head><body><h1>${safe(title)}</h1><p role="status" aria-live="polite">${safe(ui.artifact_count)} <strong id="count">0</strong> / ${tasks.length}</p><ul>${labels}</ul><button id="reset" type="button">${safe(ui.artifact_reset)}</button><p class="note">${safe(ui.artifact_note)}</p><p class="note">${safe(ui.artifact_source)}</p><script>${script}</script></body></html>`;
  }
  $("build-checklist").addEventListener("click", () => {
    const title = $("tool-title").value.trim();
    const tasks = lines($("tool-items").value);
    if (!title || !tasks.length) { say("tool-status", ui.tool_empty); return; }
    if (tasks.length > 30) { say("tool-status", ui.tool_many); return; }
    built = artifact(title, tasks);
    $("checklist-preview").srcdoc = built;
    $("checklist-preview").hidden = false;
    $("download-tool").disabled = false;
    say("tool-status", ui.tool_built);
  });
  $("download-tool").addEventListener("click", () => {
    if (!built) return;
    const url = URL.createObjectURL(new Blob(["\uFEFF", built], {type:"text/html;charset=utf-8"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = `my-checklist-${lang}.html`;
    document.body.append(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    say("tool-status", ui.tool_reopen);
  });
})();
