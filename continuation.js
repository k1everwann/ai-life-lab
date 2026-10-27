'use strict';
(() => {
  const english = document.documentElement.lang === 'en';
  const checks = [...document.querySelectorAll('[data-milestone]')];
  const consent = document.getElementById('save-learning-progress');
  const status = document.getElementById('learning-progress-status');
  const reset = document.getElementById('clear-learning-progress');
  const key = 'ai-life-lab.continuation.v1';
  if (!consent || !status || !reset) return;
  const say = (zh, en) => english ? en : zh;
  document.querySelectorAll('pre').forEach((request, index) => {
    request.id = `practice-request-${index + 1}`;
    const row = document.createElement('div');
    row.className = 'copy-row';
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'button outline';
    button.textContent = say('複製需求', 'Copy request');
    button.setAttribute('aria-controls', request.id);
    const feedback = document.createElement('span');
    feedback.setAttribute('role', 'status');
    feedback.setAttribute('aria-live', 'polite');
    row.append(button, feedback);
    request.after(row);
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(request.textContent);
        feedback.textContent = say('已複製需求。請貼到你可用的 AI 工具。', 'Request copied. Paste it into your available AI tool.');
      } catch (_) {
        const selection = window.getSelection();
        if (selection) {
          const range = document.createRange();
          range.selectNodeContents(request);
          selection.removeAllRanges();
          selection.addRange(range);
        }
        feedback.textContent = say('無法自動複製。請選取上方需求，使用複製選單或 Ctrl+C／⌘C 手動複製。', 'Automatic copying is unavailable. Select the request above and use Copy or Ctrl+C / ⌘C.');
      }
    });
  });
  let storageProblem = false;
  function report() {
    const count = checks.filter(check => check.checked).length;
    const mode = storageProblem
      ? say('無法存取瀏覽器儲存空間；目前僅記錄本頁勾選，請另存學習紀錄。', 'Browser storage is unavailable. Checks are only kept on this page; save a learning log separately.')
      : consent.checked
        ? say('已啟用本機記錄；只保存這些勾選。', 'Local recording is on; only these checks are saved.')
        : say('本機記錄未啟用；離開頁面後不保留。', 'Local recording is off; checks will not be kept after leaving this page.');
    status.textContent = say(`自行確認 ${count} / ${checks.length} 關。`, `Self-reported: ${count} / ${checks.length} stages. `) + mode + say(' 這不是作品的自動測試結果。', ' This is not an automated test of your work.');
  }
  function persist() {
    storageProblem = false;
    try {
      if (consent.checked) {
        const completed = checks.filter(check => check.checked).map(check => check.dataset.milestone);
        localStorage.setItem(key, JSON.stringify({ version: 1, completed }));
      } else {
        localStorage.removeItem(key);
      }
    } catch (_) { storageProblem = true; }
    report();
  }
  try {
    const raw = localStorage.getItem(key);
    if (raw !== null) {
      const saved = JSON.parse(raw);
      if (saved && saved.version === 1 && Array.isArray(saved.completed)) {
        consent.checked = true;
        checks.forEach(check => { check.checked = saved.completed.includes(check.dataset.milestone); });
      }
    }
  } catch (_) { storageProblem = true; }
  checks.forEach(check => check.addEventListener('change', () => {
    if (consent.checked) persist();
    else report();
  }));
  consent.addEventListener('change', persist);
  reset.addEventListener('click', () => {
    checks.forEach(check => { check.checked = false; });
    consent.checked = false;
    persist();
  });
  report();
})();
