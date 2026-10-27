(() => {
  "use strict";
  const english = document.documentElement.lang === "en";
  let edited = false;
  const track = event => {
    const el = event.target;
    if (el.matches('textarea:not([readonly]), input[type="text"], input:not([type])')) edited = true;
  };
  document.addEventListener("input", track);
  document.querySelectorAll("[data-language-switch]").forEach(link => {
    const current = link.dataset.languageSwitch === document.documentElement.lang;
    if (current) link.setAttribute("aria-current", "page");
    const url = new URL(link.getAttribute("href"), location.href);
    const route = new URLSearchParams(location.search).get("route");
    if (route === "phone" || route === "computer") url.searchParams.set("route", route);
    url.hash = location.hash;
    link.href = url.href;
    link.addEventListener("click", event => {
      // Read the current anchor at activation time, including in-page navigation.
      const target = new URL(link.href);
      target.hash = location.hash;
      const activeRoute = new URLSearchParams(location.search).get("route");
      if (activeRoute === "phone" || activeRoute === "computer") target.searchParams.set("route", activeRoute);
      link.href = target.href;
      if (current) { event.preventDefault(); return; }
      if (!edited || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      const dialog = document.createElement("dialog");
      const title = document.createElement("h2");
      const message = document.createElement("p");
      const stay = document.createElement("button");
      const proceed = document.createElement("button");
      title.id = "language-warning-title";
      title.textContent = english ? "Save your work before switching" : "切換語言前，先保存作品";
      message.textContent = english
        ? "Switching opens a new page. Your edited text and code will be cleared."
        : "切換會開啟另一個頁面，你修改的文字與程式碼會清除。";
      stay.textContent = english ? "Stay and save first" : "先保存，留在本頁";
      proceed.textContent = english ? "Switch language" : "仍要切換";
      stay.className = "button";
      proceed.className = "button outline";
      dialog.className = "language-warning";
      dialog.setAttribute("aria-labelledby", title.id);
      dialog.append(title, message, stay, proceed);
      stay.addEventListener("click", () => dialog.close());
      proceed.addEventListener("click", () => { dialog.close(); location.assign(target.href); });
      dialog.addEventListener("close", () => { dialog.remove(); link.focus(); });
      document.body.append(dialog);
      dialog.showModal();
      stay.focus();
    });
  });
})();
