(() => {
"use strict";
const $ = (s, root = document) => root.querySelector(s);
const $$ = (s, root = document) => [...root.querySelectorAll(s)];
const storageKey = "ai-life-lab-progress-v1";
let progress = {};
try { progress = JSON.parse(localStorage.getItem(storageKey) || "{}") || {}; } catch { progress = {}; }
function save() { try { localStorage.setItem(storageKey, JSON.stringify(progress)); } catch {} }
let toastTimer;
function toast(message) { const node = $("#toast"); node.textContent = message; node.classList.add("visible"); clearTimeout(toastTimer); toastTimer = setTimeout(() => node.classList.remove("visible"), 4500); }
function route(name) {
 const chosen = name === "computer" ? "computer" : "phone";
 $$("[data-route]").forEach(b => { const on = b.dataset.route === chosen; b.setAttribute("aria-selected", String(on)); b.tabIndex = on ? 0 : -1; });
 $("#phone-panel").hidden = chosen !== "phone"; $("#computer-panel").hidden = chosen !== "computer";progress.route = chosen;save();
}
$$("[data-route]").forEach(b => b.addEventListener("click", () => route(b.dataset.route)));
$$("[data-select-route]").forEach(b => b.addEventListener("click", () => route(b.dataset.selectRoute)));
route(new URLSearchParams(location.search).get("route") || progress.route);
$$('[role="tablist"]').forEach(list => list.addEventListener("keydown", event => {
 const tabs = $$('[role="tab"]', list), i = tabs.indexOf(document.activeElement);if (i < 0) return;
 const next = event.key === "ArrowRight" ? (i + 1) % tabs.length : event.key === "ArrowLeft" ? (i - 1 + tabs.length) % tabs.length : event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : -1;
 if (next >= 0) { event.preventDefault(); tabs[next].focus(); tabs[next].click(); }
}));
const stories = {
 market: {
  name:"TickForge Community",title:"對股票有興趣？先看研究工具怎麼把關。",problem:"研究資訊散在不同地方，想知道每一步依據，以及資料不明時該不該繼續。",
  method:"公開交易研究框架把資料、規則、選用的 AI 複核與風險檢查分開；內建模式只做模擬。",
  boundary:"這裡重現研究框架的部分概念，沒有行情、券商、私人策略或交易紀錄；不能當買賣依據，也不展示報酬承諾。",start:"先做自己的股票資料核對清單：來源、資料時間、單位、缺漏。喜歡其他題材也能沿用。",
  demo:'<span class="demo-label">固定教學重現 · 虛構情境，非私人截圖</span><div class="demo-window"><h4>AI 回覆後，還有哪些事要確認？</h4><p>資料 → 規則 → AI 複核 → 風險檢查 → 模擬紀錄</p><div class="demo-choices"><button data-market-state="ready" aria-pressed="true">AI 正常回覆</button><button data-market-state="timeout" aria-pressed="false">AI 沒有回覆</button><button data-market-state="unknown" aria-pressed="false">先前狀態不明</button></div><p id="market-result" class="demo-result" aria-live="polite">AI 有回覆仍須確認規則與風險檢查；回覆本身不是執行依據。</p><a class="text-link" href="https://github.com/k1everwann/tickforge-community" target="_blank" rel="noopener">查看公開研究框架 ↗</a></div><p class="demo-note">沒有呼叫 AI、即時行情或券商。這是研究流程示意，不是投資建議。</p>'
 },
 outfit: {
  name:"Forge Outfit",title:"每天穿什麼，變成有依據的建議。",problem:"把天氣、已擁有的衣物與每日提醒整理在一起。",
  method:"取得天氣資料，以規則選衣，再生成 AI 實穿示意圖，透過排程通知。",
  boundary:"選衣與文字理由包含規則引擎；AI 圖像是示意，不是實拍，也不保證衣物效果。",start:"先做一份「下雨天出門準備清單」，就是小小的第一步。",
  demo:'<span class="demo-label">功能教學重現 · 虛構衣物與天氣</span><div class="demo-window"><h4>今天出門，怎麼準備？</h4><div class="weather-row"><button data-weather="rain" aria-pressed="true">18°C 下雨</button><button data-weather="sun" aria-pressed="false">30°C 晴天</button></div><div class="outfit-items"><div class="garment" id="garment-one">防水外套</div><div class="garment" id="garment-two">長褲</div><div class="garment" id="garment-three">雨具</div></div><p id="weather-result" class="rule-output">示意規則：下雨加入防水裝備；天涼增加外層。</p></div><p class="demo-note">這裡是固定規則互動，沒有呼叫天氣 API 或 AI 產圖。</p>'
 },
 study: {
  name:"Forge Japanese N1",title:"把自己的學習方法，做成網站。",problem:"需要課程整理、每日練習，以及作答後看得懂的解析。",
  method:"教材、題庫、作答紀錄與來源證據，組成可以持續練習的網站。",
  boundary:"這是學習工具案例，不是即時 AI 家教；站內分數也不是官方考試成績。",start:"先做三題自己的練習，回答後顯示解析，就能開始。",
  demo:'<span class="demo-label">互動方式重現 · 原創生活題，非 N1 教材</span><div class="demo-window"><span class="tiny-tag">先作答，再看依據</span><h4 style="margin-top:18px">通知寫「11/05 18:00 報名截止，11/08 活動」，哪一天要完成報名？</h4><div class="demo-choices"><button data-study-answer="correct">11/05 18:00 前</button><button data-study-answer="wrong">11/08 當天</button></div><p id="study-result" class="demo-result" aria-live="polite">選一個答案，看看如何回到原文。</p></div><p class="demo-note">原文證據比「AI 說答案是這個」更能幫你判斷。</p>'
 },
 collection: {
  name:"Forge Glow",title:"把看過與想看的作品，整理成自己的收藏。",problem:"書籍、電影與影集紀錄散在不同來源，很難一起查找。",
  method:"用資料庫保存作品與目前狀態，透過書目 API 補充資訊，提供瀏覽與搜尋。",
  boundary:"這裡展示資料整理與網站功能；不把一般資料庫或 API 查詢說成內建 AI。",start:"先做一個三本書的閱讀清單，加入「想讀／讀完」狀態。",
  demo:'<span class="demo-label">收藏介面教學重現 · 書名為虛構</span><div class="demo-window"><h4>我的週末書架</h4><div class="collection-shelf"><div class="book-cover">山裡<br>的一天</div><div class="book-cover">慢慢<br>散步</div><div class="book-cover">窗邊<br>的小事</div></div><div class="demo-choices" style="margin-top:20px"><button id="collection-toggle" aria-pressed="false">把第一本標為讀完</button></div><p id="collection-result" class="demo-result" aria-live="polite">目前 0 / 3 本已讀完。狀態只在這個展示中使用。</p></div>'
 },
 guide: {
  name:"Codex / Claude 工程入門指南",title:"把做過的事，整理成下一個人能學的教材。",problem:"第一次接觸 AI 程式工具，容易被 Git、API 與工程名詞卡住。",
  method:"公開網站搭配原始碼，從工程概念走到瀏覽器 Python／SQL 與 Google Workspace 實作。",
  boundary:"今天先完成一個小任務；較深入的工程內容留到課後依需要學習。",start:"保留你的需求、修改過程與驗收結果，下一次就有自己的教材。",
  demo:'<span class="demo-label">既有公開教材 · 延伸入口</span><div class="demo-window"><h4>下一步，依你的興趣走。</h4><div class="guide-lines"><span>Git / GitHub：保存修改與協作</span><span>Python / SQL：練習資料處理</span><span>API / 連接器：接上資料與工具</span></div><a class="button small" href="https://k1everwann.github.io/codex-starter-guide/" target="_blank" rel="noopener">開啟既有教學站 ↗</a></div>'
 }
};
function showcase(key) {
 const s=stories[key]||stories.outfit,panel=$("#showcase-panel");panel.setAttribute("aria-labelledby","show-"+key);
 panel.innerHTML='<article class="project-story"><p class="project-name"></p><h3></h3><dl></dl></article><div class="project-demo"></div>';
 $(".project-name",panel).textContent=s.name;$("h3",panel).textContent=s.title;const dl=$("dl",panel);
 [["原本的小問題",s.problem],["怎麼做出來",s.method],["看懂分工與限制",s.boundary],["你可以從這裡開始",s.start]].forEach(([a,b])=>{const dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=a;dd.textContent=b;dl.append(dt,dd);});
 $(".project-demo",panel).innerHTML=s.demo; // authored static markup only
 $$("[data-showcase]").forEach(b=>{const on=b.dataset.showcase===key;b.setAttribute("aria-selected",String(on));b.tabIndex=on?0:-1;});
}
$$("[data-showcase]").forEach(b=>b.addEventListener("click",()=>showcase(b.dataset.showcase)));
$("#showcase-panel").addEventListener("click",event=>{
 const b=event.target.closest("button");if(!b)return;
 if(b.dataset.marketState){const states={ready:"AI 有回覆仍須確認規則與風險檢查；回覆本身不是執行依據。",timeout:"AI 逾時或回覆格式不符，拒絕這次候選進場；風險退出不等待 AI，不能把沒有回覆補成通過。",unknown:"先前委託狀態不明，先查清楚，封鎖後續進場；不能假設上一筆沒有發生。"};$("#market-result").textContent=states[b.dataset.marketState];$$("[data-market-state]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)));}
 if(b.dataset.weather){const rain=b.dataset.weather==="rain";$$("[data-weather]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)));$("#garment-one").textContent=rain?"防水外套":"透氣上衣";$("#garment-two").textContent=rain?"長褲":"輕薄下身";$("#garment-three").textContent=rain?"雨具":"水壺";$("#weather-result").textContent=rain?"示意規則：下雨加入防水裝備；天涼增加外層。":"示意規則：炎熱時優先透氣，並準備飲水。";}
 if(b.dataset.studyAnswer){$("#study-result").textContent=b.dataset.studyAnswer==="correct"?"答對了。原文依據：「11/05 18:00 報名截止」。活動日不是報名截止日。":"再核對原文：「11/05 18:00 報名截止」。11/08 是活動日期。";}
 if(b.id==="collection-toggle"){const on=b.getAttribute("aria-pressed")!=="true";b.setAttribute("aria-pressed",String(on));b.textContent=on?"把第一本改回想讀":"把第一本標為讀完";$("#collection-result").textContent="目前 "+(on?1:0)+" / 3 本已讀完。狀態只在這個展示中使用。";}
});showcase("market");
const contexts={picnic:["野餐墊、水和垃圾袋","背景能幫助產生合適建議；實際規定仍要看活動通知。"],library:["借閱證、筆記本與想讀的書","同一問題換了背景，合適的建議也會改變。"],unknown:["先問：去哪裡、做什麼、有哪些規定？","缺少關鍵資訊時，先釐清需求比直接補出答案更有用。"]};
$$("[data-context]").forEach(b=>b.addEventListener("click",()=>{const[a,n]=contexts[b.dataset.context];$("#context-answer").textContent=a;$("#context-note").textContent=n;$$("[data-context]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));}));
const notices="教學虛構資料。情境日期：2026-11-02，所有日期與時間皆採 Asia/Taipei。\n通知 A（11/02）：社區自然觀察活動於 11/08（日）09:00–12:00 舉辦，報名截止為 11/05（四）18:00。透過社區表單報名；成功與否需等確認信。\n通知 B（11/01 舊通知）：手作課原訂 11/07（六）10:00，在一樓教室。\n通知 C（11/02 更正）：更新 B，改為 11/07（六）14:00，在二樓教室。請於 11/04（三）20:00 前回覆能否出席。\n通知 D（11/02）：包裹請於 11/06（五）前到指定門市領取。沒有提供營業時間或最後取貨時刻。";
const phoneTask="請只根據通知 A–D 整理待辦草稿，列出「要做什麼、處理期限、活動時間、來源、待確認資訊」。更正通知優先於舊通知；區分活動日與報名截止日。未寫明的時間或狀態標示待確認，不自行補齊。只整理，不代為報名、回信或付款。";
const prompts={
 notices,"phone-short":notices+"\n\n請把通知 A–D 整理成待辦清單。","phone-full":notices+"\n\n"+phoneTask,
 gmail:"請透過 Gmail 查找最近七天本次可取得的信件，整理需要我回覆或處理的事項，附原信來源、期限與本次搜尋範圍。已讀不代表完成；沒有明確期限請標待確認。不宣稱涵蓋全部待辦。僅讀取與整理。",
 drive:"請透過 Google Drive，只讀取我指定的方案文件（請先向我要文件連結）。先確認日期、人數、幣別與每人／整團計價，再比較總額與包含項目。附文件來源，標記缺漏；沒有資料就不要猜。找到檔名但未讀到內容時請明說。僅讀取與整理。",
 budget:"虛構旅遊預算：同一天、四位成人的一日行程，全部以新台幣計價。方案 A 每人 800 元，另加整團交通 1,200 元，午餐費未提供。方案 B 整團 4,000 元，已含交通與午餐。請列出兩方案已知費用的計算式、比較條件與尚缺資訊；不要將未知費用當成零。",
 revision:"我勾選兩個項目後，畫面仍顯示完成 0 項。請檢查計數更新，修正後列出勾選、取消、全部重設三種測試步驟。保留我的標題與清單文字。"
};
async function copyText(text,message="已複製，可以貼到你的 AI 對話。") {
 try{await navigator.clipboard.writeText(text);toast(message);}
 catch{const dialog=document.createElement("dialog"),title=document.createElement("h3"),area=document.createElement("textarea"),close=document.createElement("button");title.textContent="請手動選取並複製";area.value=text;area.rows=10;area.setAttribute("aria-label","待複製的練習內容");close.textContent="關閉";close.className="button small";dialog.style.cssText="max-width:650px;width:90%;border:1px solid #cfd4dc;border-radius:16px;padding:25px";dialog.append(title,area,close);document.body.append(dialog);close.addEventListener("click",()=>dialog.close());dialog.addEventListener("close",()=>dialog.remove());dialog.showModal();area.focus();area.select();}
}
$$("[data-copy]").forEach(b=>b.addEventListener("click",()=>copyText(b.dataset.copy==="build"?$("#build-prompt").value:prompts[b.dataset.copy]||"")));
$("#copy-followup").addEventListener("click",()=>{const value=$("#phone-followup").value.trim();if(!value){toast("先寫下你想補充的一個要求。");return;}copyText(value,"已複製補充要求；回到同一個 AI 對話貼上，再核對修改結果。");});
$("#share-route").addEventListener("click",()=>copyText("https://k1everwann.github.io/ai-life-lab/?route="+(progress.route==="computer"?"computer":"phone")+"#classroom","已複製這條路線的公開分享連結。"));
const correct={q1:"contradicted",q2:"supported",q3:"unknown"};
const explanations={q1:"① 與原文矛盾：A 寫明 11/05 18:00 報名截止；11/08 是活動日。",q2:"② 有依據：C 更正為 11/07 14:00、二樓，應更新舊通知 B。",q3:"③ 目前無法判斷：D 沒有門市營業時間，22:00 是無依據的補充。"};
if(progress.audit)for(const[name,value]of Object.entries(progress.audit)){const el=$('input[name="'+name+'"][value="'+value+'"]');if(el)el.checked=true;}
$("#audit-form").addEventListener("submit",event=>{
 event.preventDefault();const data=new FormData(event.currentTarget);let score=0;progress.audit={};const box=$("#audit-feedback");box.replaceChildren();
 for(const name of Object.keys(correct)){const value=data.get(name);progress.audit[name]=value;if(value===correct[name])score++;}
 const title=document.createElement("strong");title.textContent="本次判斷 "+score+" / 3 題符合參考答案。";box.append(title);
 for(const[name,ex]of Object.entries(explanations)){const p=document.createElement("p");p.textContent=(progress.audit[name]===correct[name]?"✓ ":"再想想：")+ex;box.append(p);}save();
});
$("#check-budget").addEventListener("click",()=>{const raw=$("#budget-answer").value.trim(),n=Number(raw);$("#budget-feedback").textContent=!raw?"先輸入你計算的金額。":n===4400?"正確：800 × 4 ＋ 1,200 ＝ 4,400 元。這只是 A 的已知費用，午餐另計；不能把缺漏費用當零。":"再檢查：先算四人的費用，再加一次整團交通。午餐費目前未知。";});
function makeBrief(){
 const title=$("#project-title").value.trim()||"我的生活清單",purpose=$("#project-purpose").value.trim()||"整理自己的生活事項",items=$("#project-items").value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean).slice(0,20);
 if(items.length<3){toast("請至少填入三個清單項目。");return;}
 $("#build-prompt").value="請在新的練習資料夾製作一個單檔 index.html，名稱為「"+title+"」。\n用途："+purpose+"。\n清單項目："+items.join("、")+"。\n\n需求：\n1. 繁體中文，包含標題、用途與上述清單。\n2. 可勾選與取消，完成數即時更新。\n3. 提供「全部重設」按鈕，同步清除勾選與數量。\n4. 390px 手機寬度也可閱讀操作，按鈕與勾選區域容易點選。\n5. HTML、CSS、JavaScript 全放同一檔，不使用外部套件、網路字型、API 或登入。\n6. 第一版重新整理後可重設，請在畫面說明，不宣稱會保存。\n7. 只處理這個練習資料夾，不修改其他檔案，不部署上網。\n\n請提供完整程式，說明如何儲存、開啟，並列出勾選、取消、全部重設與窄螢幕四種親自測試的步驟。";
}
$("#brief-form").addEventListener("submit",e=>{e.preventDefault();makeBrief();});makeBrief();
function download(name,content,type="text/plain;charset=utf-8"){const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
$("#load-sample").addEventListener("click",async()=>{try{const r=await fetch("examples/my-checklist.html");if(!r.ok)throw new Error();$("#html-code").value=await r.text();$("#preview-status").textContent="已載入完成品範例。按「預覽我的網頁」查看並測試。";}catch{$("#preview-status").textContent="範例載入失敗，請開啟上方完成品連結，或貼入你的完整 HTML。";}});
$("#run-preview").addEventListener("click",()=>{
 const code=$("#html-code").value.trim();if(!code){$("#preview-status").textContent="請先貼上 HTML 或載入完成品範例。";return;}
 const policy='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; img-src data:; connect-src \'none\'; frame-src \'none\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'">';
 const safeCode=/<head(?:\s[^>]*)?>/i.test(code)?code.replace(/<head(?:\s[^>]*)?>/i,m=>m+policy):policy+code;
 $("#code-preview").srcdoc=safeCode;$("#preview-status").textContent="已更新隔離預覽。請實際勾選、取消及重設，確認數量一致。";
});
$("#download-code").addEventListener("click",()=>{const code=$("#html-code").value.trim();if(!code){toast("請先貼上 HTML 或載入範例。");return;}download("my-webpage.html",code,"text/html;charset=utf-8");toast("已送出下載；請確認檔案保存成功。");});
$$("[data-check]").forEach(b=>{b.checked=Boolean(progress[b.dataset.check]);b.addEventListener("change",()=>{progress[b.dataset.check]=b.checked;save();});});
function makeCard(){
 const checks=$$("[data-check]").map(b=>(b.checked?"[已親自確認] ":"[尚未確認] ")+b.parentElement.textContent.trim()).join("\n");
 return "AI 生活實驗室｜我的帶走卡\n路線："+(progress.route==="computer"?"電腦做網頁":"手機生活應用")+"\n\n我今天核對後的成果：\n"+($("#my-completed").value.trim()||"尚未填寫")+"\n\n我下次想做的事：\n"+($("#my-next-task").value.trim()||"尚未填寫")+"\n\n我會如何核對：\n"+($("#my-check").value.trim()||"尚未填寫")+"\n\n"+(progress.route==="computer"?checks+"\n\n":"")+"方法：說明需求 → 提供材料 → 取得草稿 → 核對與修改。\n提醒：整理不等於執行；搜尋不保證完整。對得上原文，仍要確認原始消息可信。\n";
}
$("#copy-card").addEventListener("click",async()=>{await copyText(makeCard(),"帶走卡已複製，請貼到自己的備忘錄並確認保存。");$("#card-status").textContent="完成複製後，請到備忘錄貼上；再重新開啟筆記確認。";});
$("#download-card").addEventListener("click",()=>{
 download("ai-life-takeaway.txt",makeCard());$("#card-status").textContent="已送出下載。請到瀏覽器下載清單或手機檔案中，開啟 ai-life-takeaway.txt 確認內容；未成功時改用複製。";toast("已送出下載；請確認帶走卡保存成功。");
});
$("#present-toggle").addEventListener("click",e=>{const on=document.body.classList.toggle("present-mode");e.currentTarget.setAttribute("aria-pressed",String(on));e.currentTarget.textContent=on?"還原字級":"放大字級";});
$("#reset-progress").addEventListener("click",()=>{progress={};save();$$('input[type="radio"],[data-check]').forEach(x=>x.checked=false);$("#audit-feedback").replaceChildren();toast("已清除此網站在本裝置的練習進度。");});
})();
