(() => {
  "use strict";
  const node = document.getElementById("curriculum-data");
  if (!node) return;
  const {modules, ui, debugFixtures, preparedFixtures} = JSON.parse(node.textContent);
  const lang = document.documentElement.lang;
  const en = lang === "en";
  const $ = id => document.getElementById(id);
  const all = selector => [...document.querySelectorAll(selector)];
  const say = (id, text) => { $(id).textContent = text; };
  const byKey = key => modules.find(module => module.id === key);
  const article = key => $(byKey(key).anchor);
  all(".visual-step > summary").forEach(summary => summary.addEventListener("click", () => {
    requestAnimationFrame(() => {
      if (summary.parentElement.open) summary.parentElement.scrollIntoView({block:"start", behavior:"instant"});
    });
  }));
  const imageDialog = $("screenshot-dialog");
  let imageTrigger = null;
  all("[data-screenshot]").forEach(link => link.addEventListener("click", event => {
    if (!imageDialog || typeof imageDialog.showModal !== "function") return;
    event.preventDefault();
    imageTrigger = link;
    const image = link.querySelector("img");
    $("screenshot-large").src = image.src;
    $("screenshot-large").alt = image.alt;
    $("screenshot-caption").textContent = image.alt;
    imageDialog.showModal();
  }));
  imageDialog?.addEventListener("close", () => imageTrigger?.focus());
  const drafts = new Map();
  function capture(key) {
    return {request:$("question-"+key).value,result:$("result-"+key).value,mode:$("mode-"+key).value,code:$("code-"+key)?.value || ""};
  }
  function evidenceKind(key,kind) {
    return kind==='guided' && $('mode-'+key).value==='1' ? 'classroom' : kind;
  }
  function updateEvidence(key) {
    const active=evidenceKind(key,article(key).dataset.exercise || 'guided');
    article(key).querySelectorAll('[data-evidence-kind]').forEach(group=>{group.hidden=group.dataset.evidenceKind!==active;});
  }
  function setExercise(key,kind) {
    const current=article(key).dataset.exercise || "guided";
    if(current!==kind){
      drafts.set(key+":"+current,capture(key));
      const saved=drafts.get(key+":"+kind) || {request:"",result:"",mode:"0",code:""};
      $("question-"+key).value=saved.request;
      $("result-"+key).value=saved.result;
      $("mode-"+key).value=saved.mode;
      if($("code-"+key)){
        $("code-"+key).value=saved.code;
        $("preview-"+key).hidden=true;
        $("preview-"+key).removeAttribute("srcdoc");
        say("code-status-"+key,en?"Exercise changed. Update the preview to test this code.":"已切換練習，請更新預覽再測試這份程式碼。");
      }
    }
    article(key).dataset.exercise=kind;
    $("exercise-"+key).value=kind;
    updateEvidence(key);
  }
  modules.forEach(m=>$("exercise-"+m.id).addEventListener("change",event=>setExercise(m.id,event.target.value)));
  modules.forEach(m=>$('mode-'+m.id).addEventListener('change',()=>updateEvidence(m.id)));
  all('[data-classroom-record]').forEach(button=>button.addEventListener('click',()=>{
    const key=button.dataset.classroomRecord;
    setExercise(key,'guided');
    $('mode-'+key).value='1';
    updateEvidence(key);
    article(key).querySelector('.module-record').open=true;
    $('question-'+key).focus();
    $('question-'+key).scrollIntoView({block:'center'});
  }));
  let pendingPrepared=null;
  const preparedDialog=$('prepared-confirm');
  function loadPrepared(button) {
    const key=button.dataset.loadPrepared;
    setExercise(key,'guided');
    const fixed=button.dataset.preparedFixed==='true';
    $('code-'+key).value=preparedFixtures[key+(fixed?'fixed':'')];
    $('mode-'+key).value='1';
    updateEvidence(key);
    $('code-'+key).dispatchEvent(new Event('input',{bubbles:true}));
    $('workspace-'+key).scrollIntoView({block:'start'});
    article(key).querySelector('[data-preview]').focus({preventScroll:true});
    say('code-status-'+key,fixed ? (en?'Prepared reference fix loaded. Update the preview, test, and download this corrected version.':'已載入預備的參考修正版。請更新預覽、測試並下載這份修正版。') : (en?'Prepared code loaded. Update the preview and test it; record your own change separately.':'已載入預備程式。請更新預覽並實測，再記下自己想改的地方。'));
  }
  all('[data-load-prepared]').forEach(button=>button.addEventListener('click',()=>{
    const key=button.dataset.loadPrepared;
    const targetCode=(article(key).dataset.exercise || 'guided')==='guided' ? $('code-'+key).value : (drafts.get(key+':guided')?.code || '');
    if(targetCode.trim()) {
      pendingPrepared=button;
      preparedDialog.showModal();
    } else loadPrepared(button);
  }));
  $('prepared-cancel').addEventListener('click',()=>preparedDialog.close());
  $('prepared-replace').addEventListener('click',()=>{
    const button=pendingPrepared;
    pendingPrepared=null;
    preparedDialog.close();
    if(button)loadPrepared(button);
  });
  preparedDialog.addEventListener('close',()=>{pendingPrepared?.focus();pendingPrepared=null;});
  const aliases = {"classroom":"lesson-start", "tool":"lesson-build", "principles":"course-map", "showcase":"course-map", "takeaway":"continue"};
  let lastLesson = "lesson-gmail";
  all('.connection a[href="#connection-guide"]').forEach(link=>link.addEventListener("click",()=>{lastLesson=link.closest("details").id;}));
  $("return-to-connection").addEventListener("click",()=>{location.hash=lastLesson;});

  function route(focus = false) {
    let hash=location.hash.slice(1);
    try { hash=decodeURIComponent(hash); } catch { /* Invalid external bookmark: keep the course usable. */ }
    const target = aliases[hash] || hash;
    let chosen = modules.find(m => m.anchor === target);
    const element = $(target);
    if (element?.tagName === "DETAILS") element.open=true;
    if (!chosen && element) {
      const parent = element.closest("[data-module]");
      if (parent) chosen = byKey(parent.dataset.module);
    }
    all("[data-module]").forEach(el => { el.hidden = !chosen || el.dataset.module !== chosen.id; });
    const view = chosen ? "lesson" : target === "connection-guide" ? "setup" : target === "continue" ? "continue" : "home";
    all("#main > [data-view]").forEach(el=>{el.hidden=el.dataset.view!==view;});
    document.body.dataset.view=view;
    document.querySelector(".skip").href=chosen ? "#"+chosen.anchor : view==="setup" ? "#connection-guide" : view==="continue" ? "#continue" : "#top";
    if(chosen) lastLesson = target.startsWith("connection-") ? target : chosen.anchor;
    all(".module-list a, .lesson-sidebar a, .mobile-lessons a").forEach(link => {
      if (chosen && link.hash === `#${chosen.anchor}`) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
    if (chosen && /^(challenge|independent|connection)-/.test(target)) $(target).open = true;
    document.querySelector(".mobile-lessons").open=false;
    if (chosen && focus) {
      const heading = element===article(chosen.id) ? element.querySelector("h1") : element?.querySelector("summary,h2,h3") || article(chosen.id).querySelector("h1");
      heading.setAttribute("tabindex","-1");
      heading.focus({preventScroll:true});
      (element || article(chosen.id)).scrollIntoView();
    } else if (focus && element) {
      const heading=element.querySelector("h1,h2,h3,summary");
      if (heading) { heading.setAttribute("tabindex","-1"); heading.focus({preventScroll:true}); }
      element.scrollIntoView();
    } else if (focus) $("top").scrollIntoView();
  }
  window.addEventListener("hashchange", () => route(true));
  route(Boolean(location.hash));
  document.querySelector(".skip").addEventListener("click", event => {
    event.preventDefault();
    const target = document.querySelector(document.querySelector(".skip").getAttribute("href"));
    const heading = target.querySelector("h1,h2");
    heading.setAttribute("tabindex","-1");
    heading.focus({preventScroll:true});
    target.scrollIntoView();
  });
  all("[data-jump-challenge]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.jumpChallenge;
    $("challenge-"+key).open = true;
    setExercise(key,"challenge");
    $("challenge-"+key).querySelector("summary").focus();
    $("challenge-"+key).scrollIntoView();
  }));
  all("[data-jump-independent]").forEach(button => button.addEventListener("click", () => {
    const key=button.dataset.jumpIndependent;
    $("independent-"+key).open=true;
    setExercise(key,"independent");
    $("independent-"+key).querySelector("summary").focus();
    $("independent-"+key).scrollIntoView();
  }));

  let copyTrigger=null;
  async function copy(text, status) {
    copyTrigger=document.activeElement;
    $("copy-fallback").hidden = true;
    try {
      if (!navigator.clipboard || !window.isSecureContext) throw new Error("manual");
      await navigator.clipboard.writeText(text);
      say(status, ui.copied);
    } catch {
      $("manual-copy").value = text;
      $("copy-fallback").hidden = false;
      say(status, ui.manual);
      $("manual-copy").focus();
      $("manual-copy").select();
    }
  }
  $("copy-return").addEventListener("click",()=>{
    $("copy-fallback").hidden=true;
    if(copyTrigger)copyTrigger.focus();
  });
  all("[data-copy-module]").forEach(button => button.addEventListener("click", () => {
    const m = byKey(button.dataset.copyModule);
    const kind = button.dataset.copyKind;
    setExercise(m.id,kind === "followup" ? "guided" : kind);
    let text = kind === "connection" ? m.connection.prompt : kind === "followup" ? [m.followup.source,m.followup.prompt].join("\n\n") : kind === "independent" ? m.independent.task : kind === "challenge"
      ? [m.challenge.task, m.challenge.source, m.challenge.prompt].join("\n\n")
      : [m.source, m.prompt].join("\n\n");
    if (m.id === "M09" && debugFixtures[kind]) {
      text += "\n\n" + (en ? "Complete broken HTML source:\n" : "故障 HTML（完整原始碼）：\n") + debugFixtures[kind];
    }
    copy(text, `copy-${m.id}-${kind}`);
  }));
  all("[data-check-quiz]").forEach(button => button.addEventListener("click", () => {
    const m = byKey(button.dataset.checkQuiz);
    const answer = document.querySelector(`input[name="quiz-${m.id}"]:checked`);
    if (!answer) { say(`quiz-${m.id}-feedback`, ui.choose); return; }
    say(`quiz-${m.id}-feedback`, `${Number(answer.value) === m.quiz.answer ? ui.right : ui.retry} ${m.quiz.explanation}`);
  }));

  function download(text, name, type) {
    const url = URL.createObjectURL(new Blob(["\uFEFF", text], {type}));
    const link = document.createElement("a");
    link.href = url; link.download = name;
    document.body.append(link); link.click(); link.remove();
    window.setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  function record(m, kind=$("exercise-"+m.id).value) {
    const saved=kind===$("exercise-"+m.id).value?capture(m.id):drafts.get(m.id+":"+kind);
    if(!saved) return null;
    const request = saved.request.trim();
    const result = saved.result.trim();
    const mode = Number(saved.mode);
    const evidence=kind==='guided' && mode===1 ? 'classroom' : kind;
    const boxes = [...article(m.id).querySelectorAll(`[data-evidence-kind="${evidence}"] [data-evidence]`)];
    const code = saved.code.trim();
    if (!request && !result && !code && !mode && !boxes.some(box => box.checked)) return null;
    const typeIndex=["guided","independent","challenge","connection"].indexOf(kind);
    const source=kind==="connection"?m.connection?.source:kind==="independent"?m.independent.task:kind==="challenge"?m.challenge.source:m.source;
    const prompt=kind==="connection"?m.connection?.prompt:kind==="independent"?m.independent.task:kind==="challenge"?m.challenge.prompt:[m.prompt,m.followup?[m.followup.source,m.followup.prompt].join("\n\n"):""].filter(Boolean).join("\n\n");
    return [
      `${m.id} ${m.title}`, `${ui.exercise}\n${ui.exercise_types[typeIndex] || (en?"Connected account":"連線練習")}`, `${ui.mode}\n${ui.modes[mode]}`, `${ui.source}\n${source || "—"}`,
      `${ui.prompt}\n${prompt}`, mode===1 && kind==='guided' ? `${en?'Prepared-material task':'預備材料練習'}\n${m.classroom.task}` : '', `${ui.question}\n${request || "—"}`,
      `${ui.result}\n${result || "—"}`, kind!=="guided"&&m[kind]?`${ui.expected}\n${m[kind].expected}`:"", `${ui.checks}\n${boxes.map(box => `${box.checked?"[x]":"[ ]"} ${(evidence==="guided"?m.checks:ui.other_checks)[Number(box.dataset.evidence)]}`).join("\n")}`,
      code ? `${ui.codeinput}\n${code}` : "", ui.self
    ].filter(Boolean).join("\n\n");
  }
  all("[data-download-record]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.downloadRecord;
    const text = record(byKey(key));
    if (!text) { say(`record-${key}-status`, ui.emptyrecord); return; }
    download(text, `${key.toLowerCase()}-my-record-${lang}.txt`, "text/plain;charset=utf-8");
    say(`record-${key}-status`, ui.recordsaved);
  }));
  $("download-all-records").addEventListener("click", () => {
    const texts = modules.flatMap(m=>["guided","independent","challenge","connection"].map(kind=>record(m,kind))).filter(Boolean);
    if (!texts.length) { say("all-record-status", ui.emptyrecord); return; }
    download(texts.join("\n\n====================\n\n"), `ai-life-lab-my-records-${lang}.txt`, "text/plain;charset=utf-8");
    say("all-record-status", ui.recordsaved);
  });

  const csp = '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\'; style-src \'unsafe-inline\'; img-src data:; connect-src \'none\'; form-action \'none\'; base-uri \'none\'">';
  all("[data-preview]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.preview;
    const code = $(`code-${key}`).value.trim();
    if (!code) { say(`code-status-${key}`, ui.emptycode); return; }
    $(`preview-${key}`).srcdoc = `<!doctype html>${csp}${code}`;
    $(`preview-${key}`).hidden = false;
    say(`code-status-${key}`, ui.previewready);
  }));
  all("[data-code-download]").forEach(button => button.addEventListener("click", () => {
    const key = button.dataset.codeDownload;
    const code = $(`code-${key}`).value.trim();
    if (!code) { say(`code-status-${key}`, ui.emptycode); return; }
    download(code, `my-tool-${key.toLowerCase()}.html`, "text/html;charset=utf-8");
    say(`code-status-${key}`, ui.downloadready);
  }));
  all("[data-code]").forEach(field => field.addEventListener("input", () => {
    const key = field.id.replace("code-", "");
    $(`preview-${key}`).hidden = true;
    $(`preview-${key}`).removeAttribute("srcdoc");
    say(`code-status-${key}`, en ? "Code changed. Update the preview to test this version." : "程式碼已修改，請更新預覽再測這個版本。");
  }));

  function threshold(inclusive) {
    const rows = [{label:en?"Meals":"餐食",before:1200,after:1350},{label:en?"Transport":"交通",before:400,after:450},{label:en?"Services":"服務",before:500,after:550}];
    const matched = rows.filter(r => inclusive ? r.after-r.before >= 50 : r.after-r.before > 50);
    say("threshold-result", en
      ? `${inclusive?"At least":"Greater than"} 50: ${matched.map(r=>r.label).join(", ")} (${matched.length} categories). All data: TWD 2,100 → 2,350; +250 / +11.9%. The overall total does not change.`
      : `${inclusive?"至少":"超過"}50：${matched.map(r=>r.label).join("、")}，共${matched.length}類。全體資料仍為2,100→2,350元，增加250／11.9%；總額不隨篩選改變。`);
  }
  all("[data-threshold]").forEach(button => button.addEventListener("click", () => {
    all("[data-threshold]").forEach(b=>b.setAttribute("aria-pressed",String(b===button)));
    threshold(button.dataset.threshold === "inclusive");
  }));
  threshold(false);
  let latest = null; let counter = 0; let notifications = 0;
  const seen = new Set();
  const ruleCount = () => say("rule-count", en ? `Simulated alerts: ${notifications}. Threshold: temperature ≥ 28°C. Each event alerts at most once.` : `模擬提醒：${notifications}次。規則：溫度達28°C；同一事件最多提醒一次。`);
  function runEvent(event) {
    if (seen.has(event.id)) {
      say("rule-result", en ? `${event.id}: duplicate event; no new alert.` : `${event.id}：重複事件，不再提醒。`);
    } else {
      seen.add(event.id);
      if (event.reading === "missing") say("rule-result", en ? `${event.id}: missing reading; mark to confirm. Do not treat it as 0°C.` : `${event.id}：缺少讀值，標待確認，不當成0°C。`);
      else if (Number(event.reading) >= 28) {
        notifications++;
        say("rule-result", en ? `${event.id}: ${event.reading}°C; simulated alert. No device action.` : `${event.id}：${event.reading}°C，產生模擬提醒；沒有控制設備。`);
      } else say("rule-result", en ? `${event.id}: ${event.reading}°C; below threshold, no alert.` : `${event.id}：${event.reading}°C，未達門檻，不提醒。`);
    }
    ruleCount();
  }
  $("simulate-rule").addEventListener("click", () => {
    latest = {id:`E${++counter}`, reading:$("sensor-reading").value};
    $("repeat-rule").disabled = false; runEvent(latest);
  });
  $("repeat-rule").addEventListener("click", () => { if(latest) runEvent(latest); });
  $("reset-rule").addEventListener("click", () => {
    latest=null; counter=0; notifications=0; seen.clear();
    $("repeat-rule").disabled=true; $("sensor-reading").value="27";
    say("rule-result", en?"Simulation reset. Test a new reading.":"模擬已重設，請選一筆讀值測試。"); ruleCount();
  });
  ruleCount();


})();
