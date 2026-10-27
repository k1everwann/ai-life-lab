(() => {
  "use strict";
  const node = document.getElementById("seminar-data");
  if (!node) return;
  const data = JSON.parse(node.textContent);
  const lang = document.documentElement.lang;
  const t = data.locales[lang];
  const course = document.getElementById("course-data");
  const question = course ? JSON.parse(course.textContent).locales[lang].promptLesson.strong : t.firstPrompt;
  const $ = id => document.getElementById(id);
  const all = selector => [...document.querySelectorAll(selector)];
  const announce = (id, value) => { $(id).textContent = value; };
  const showDemo = key => {
    all("[data-demo]").forEach(button => button.setAttribute("aria-pressed", String(button.dataset.demo === key)));
    all(".demo-panel").forEach(panel => { panel.hidden = panel.id !== `demo-${key}`; });
  };
  all("[data-demo]").forEach(button => button.addEventListener("click", () => showDemo(button.dataset.demo)));
  showDemo("travel");
  all("[data-stop]").forEach(button => button.addEventListener("click", () => {
    const stop = t.stops[Number(button.dataset.stop)];
    all("[data-stop]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    const strong = document.createElement("strong");
    strong.textContent = `${stop.time} ${stop.name}`;
    $("travel-detail").replaceChildren(strong, document.createElement("br"), document.createTextNode(stop.detail));
  }));
  all("[data-answer]").forEach(button => button.addEventListener("click", () => {
    all("[data-answer]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    announce("quiz-feedback", `${button.dataset.answer === data.quiz.answer ? t.quizCorrect : t.quizIncorrect} ${t.quizExplanation}`);
  }));
  $("review-add").addEventListener("click", () => {
    $("review-add").setAttribute("aria-pressed", "true");
    $("review-add").textContent = t.reviewDone;
    announce("review-feedback", t.reviewNote);
  });
  all("[data-temp]").forEach(button => button.addEventListener("click", () => {
    const temperature = Number(button.dataset.temp);
    all("[data-temp]").forEach(item => item.setAttribute("aria-pressed", String(item === button)));
    announce("home-temp", `${temperature}°C`);
    announce("home-ac", temperature >= data.home.threshold ? t.on : t.off);
  }));
  $("market-product").addEventListener("change", event => {
    const item = data.market[event.target.value];
    const unit = t.units[item.unitKey];
    item.values.forEach((value, i) => announce(`market-value-${i}`, `${value.toLocaleString("en-US")} ${unit}`));
    const change = item.values[1] - item.values[0];
    const percent = change / item.values[0] * 100;
    const sign = change > 0 ? "+" : "";
    announce("market-change", `${t.change}: ${sign}${change.toLocaleString("en-US")} ${unit} (${sign}${Number(percent.toFixed(1))}%)`);
  });
  const initial = () => `${t.sources.map(source => `${source.label}\n${source.text}`).join("\n\n")}\n\n${question}`;
  async function copy(text, feedbackId) {
    $("copy-fallback").hidden = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("Clipboard unavailable");
      await navigator.clipboard.writeText(text);
      announce(feedbackId, t.copySuccess);
    } catch {
      $("manual-copy").value = text;
      $("copy-fallback").hidden = false;
      announce(feedbackId, t.copyManual);
      $("manual-copy").focus();
      $("manual-copy").select();
    }
  }
  $("copy-initial").addEventListener("click", () => copy(initial(), "initial-feedback"));
  $("copy-followup").addEventListener("click", () => {
    const value = $("learner-followup").value.trim();
    if (!value) {
      announce("followup-feedback", t.emptyFollowup);
      $("learner-followup").focus();
      return;
    }
    copy(value, "followup-feedback");
  });
  function record() {
    const result = $("learner-result").value.trim();
    if (!result) {
      announce("record-feedback", t.emptyResult);
      $("learner-result").focus();
      return null;
    }
    const checks = all("[data-check]").map(item => `${item.checked ? "[x]" : "[ ]"} ${t.checks[Number(item.dataset.check)]}`);
    return [t.recordTitle, `${t.modeLabel}\n${t.modeOptions[$("practice-mode").value]}`, `${t.recordPrompt}\n${initial()}`, `${t.recordFollowup}\n${$("learner-followup").value.trim() || t.notWritten}`, `${t.recordChecks}\n${checks.join("\n")}`, `${t.recordResult}\n${result}`].join("\n\n");
  }
  $("copy-record").addEventListener("click", () => {
    const text = record();
    if (text) copy(text, "record-feedback");
  });
  $("download-record").addEventListener("click", () => {
    const text = record();
    if (!text) return;
    const url = URL.createObjectURL(new Blob(["\uFEFF", text], {type:"text/plain;charset=utf-8"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = `travel-practice-${lang}.txt`;
    document.body.append(link);
    link.click();
    link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
    announce("record-feedback", t.downloadSuccess);
  });
})();
