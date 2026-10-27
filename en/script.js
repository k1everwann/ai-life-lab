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
 $("#phone-panel").hidden = chosen !== "phone"; $("#computer-panel").hidden = chosen !== "computer"; progress.route = chosen; save();
 const url=new URL(location.href);url.searchParams.set("route",chosen);history.replaceState(null,"",url);
}
$$("[data-route]").forEach(b => b.addEventListener("click", () => route(b.dataset.route)));
$$("[data-select-route]").forEach(b => b.addEventListener("click", () => route(b.dataset.selectRoute)));
route(new URLSearchParams(location.search).get("route") || progress.route);
$$('[role="tablist"]').forEach(list => list.addEventListener("keydown", event => {
 const tabs = $$('[role="tab"]', list), i = tabs.indexOf(document.activeElement); if (i < 0) return;
 const next = event.key === "ArrowRight" ? (i + 1) % tabs.length : event.key === "ArrowLeft" ? (i - 1 + tabs.length) % tabs.length : event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : -1;
 if (next >= 0) { event.preventDefault(); tabs[next].focus(); tabs[next].click(); }
}));
const stories = {
 market: {
  name:"TickForge Community", title:"Interested in stocks? See how a research tool checks its work.", problem:"Research information is scattered. You want to know the evidence for each step and whether to continue when data is unclear.",
  method:"The public trading research framework separates data, rules, optional AI review, and risk checks. Its built-in mode uses simulation only.",
  boundary:"This reconstructs a few framework concepts. It has no market feed, broker, private strategy, or trading records. It is not a basis for trading and makes no return promises.", start:"Make your own stock-data checking list: source, timestamp, units, and missing information. You can reuse the method for other topics.",
  demo:'<span class="demo-label">Fixed teaching reconstruction · Fictional scenario, not a private screenshot</span><div class="demo-window"><h4>What needs checking after AI replies?</h4><p>Data → Rules → AI review → Risk checks → Simulation record</p><div class="demo-choices"><button data-market-state="ready" aria-pressed="true">AI replies normally</button><button data-market-state="timeout" aria-pressed="false">AI does not reply</button><button data-market-state="unknown" aria-pressed="false">Previous status unknown</button></div><p id="market-result" class="demo-result" aria-live="polite">Even with an AI reply, rules and risk checks must pass. A reply alone does not authorize execution.</p><a class="text-link" href="https://github.com/k1everwann/tickforge-community" target="_blank" rel="noopener">View the public research framework ↗</a></div><p class="demo-note">No AI calls, live market data, or broker connection. This is a research workflow illustration, not investment advice.</p>'
 },
 outfit: {
  name:"Forge Outfit", title:"Turn “what should I wear?” into a suggestion with reasons.", problem:"Bring together weather, clothes already owned, and daily reminders.",
  method:"Get weather data, select clothing using rules, generate an AI illustration, and send scheduled notifications.",
  boundary:"Clothing selection and written reasons include a rule engine. AI images are illustrations, not photographs or guarantees of how clothes will look.", start:"A rainy-day departure checklist is a small first step.",
  demo:'<span class="demo-label">Feature reconstruction · Fictional clothes and weather</span><div class="demo-window"><h4>How should I prepare to go out?</h4><div class="weather-row"><button data-weather="rain" aria-pressed="true">18°C Rain</button><button data-weather="sun" aria-pressed="false">30°C Sun</button></div><div class="outfit-items"><div class="garment" id="garment-one">Waterproof jacket</div><div class="garment" id="garment-two">Long trousers</div><div class="garment" id="garment-three">Rain gear</div></div><p id="weather-result" class="rule-output">Example rule: add waterproof gear for rain and an outer layer for cool weather.</p></div><p class="demo-note">This interaction uses fixed rules. It does not call a weather API or generate AI images.</p>'
 },
 study: {
  name:"Forge Japanese N1", title:"Make a website around the way you learn.", problem:"Organize lessons, daily practice, and explanations you can understand after answering.",
  method:"Materials, questions, answer records, and source evidence form a website for continued practice.",
  boundary:"This is a learning-tool example, not a live AI tutor. Its scores are not official exam results.", start:"Begin with three questions of your own and show an explanation after each answer.",
  demo:'<span class="demo-label">Interaction reconstruction · Original everyday question, not N1 material</span><div class="demo-window"><span class="tiny-tag">Answer first, then check the evidence</span><h4 style="margin-top:18px">The notice says “registration closes Nov 5, 18:00; activity Nov 8.” When must you register?</h4><div class="demo-choices"><button data-study-answer="correct">By Nov 5, 18:00</button><button data-study-answer="wrong">On Nov 8</button></div><p id="study-result" class="demo-result" aria-live="polite">Choose an answer to see how to return to the original.</p></div><p class="demo-note">Original evidence helps you judge more than “AI said this is the answer.”</p>'
 },
 collection: {
  name:"Forge Glow", title:"Organize stories you have enjoyed and want to explore.", problem:"Book, movie, and series records are scattered across sources and hard to search together.",
  method:"A database stores titles and current status, bibliographic APIs add information, and the website provides browsing and search.",
  boundary:"This demonstrates data organization and website features. A normal database or API lookup is not described as built-in AI.", start:"Make a three-book reading list with “want to read” and “finished” statuses.",
  demo:'<span class="demo-label">Collection interface reconstruction · Fictional book titles</span><div class="demo-window"><h4>My weekend bookshelf</h4><div class="collection-shelf"><div class="book-cover">A Day<br>in the Hills</div><div class="book-cover">A Slow<br>Walk</div><div class="book-cover">By the<br>Window</div></div><div class="demo-choices" style="margin-top:20px"><button id="collection-toggle" aria-pressed="false">Mark the first book finished</button></div><p id="collection-result" class="demo-result" aria-live="polite">0 / 3 books finished. This status is used only inside this demonstration.</p></div>'
 },
 guide: {
  name:"Codex / Claude engineering starter guide", title:"Turn your own work into material someone else can learn from.", problem:"Git, APIs, and engineering terms can block a first encounter with AI coding tools.",
  method:"A public website and source code connect engineering ideas with browser-based Python / SQL and Google Workspace practice.",
  boundary:"Complete one small task today. Explore deeper engineering topics after class as needed.", start:"Keep your Build request, revisions, and Check your work results as material for next time.",
  demo:'<span class="demo-label">Existing public material · Further learning</span><div class="demo-window"><h4>Choose your next step by interest.</h4><div class="guide-lines"><span>Git / GitHub: save changes and collaborate</span><span>Python / SQL: practice data processing</span><span>APIs / connectors: connect data and tools</span></div><a class="button small" href="web-project.html">Open After-class practice →</a><a class="text-link" href="https://k1everwann.github.io/codex-starter-guide/" target="_blank" rel="noopener">Existing engineering guide (Traditional Chinese) ↗</a></div>'
 }
};
function showcase(key) {
 const s=stories[key]||stories.outfit,panel=$("#showcase-panel"); panel.setAttribute("aria-labelledby","show-"+key);
 panel.innerHTML='<article class="project-story"><p class="project-name"></p><h3></h3><dl></dl></article><div class="project-demo"></div>';
 $(".project-name",panel).textContent=s.name; $("h3",panel).textContent=s.title; const dl=$("dl",panel);
 [["The original small problem",s.problem],["How it was made",s.method],["Roles and limits",s.boundary],["A place for you to start",s.start]].forEach(([a,b])=>{const dt=document.createElement("dt"),dd=document.createElement("dd");dt.textContent=a;dd.textContent=b;dl.append(dt,dd);});
 $(".project-demo",panel).innerHTML=s.demo; // Authored static markup only.
 $$("[data-showcase]").forEach(b=>{const on=b.dataset.showcase===key;b.setAttribute("aria-selected",String(on));b.tabIndex=on?0:-1;});
}
$$("[data-showcase]").forEach(b=>b.addEventListener("click",()=>showcase(b.dataset.showcase)));
$("#showcase-panel").addEventListener("click",event=>{
 const b=event.target.closest("button");if(!b)return;
 if(b.dataset.marketState){const states={ready:"Even with an AI reply, rules and risk checks must pass. A reply alone does not authorize execution.",timeout:"An AI timeout or invalid reply format rejects this entry candidate. Risk exits do not wait for AI. No reply must not be treated as approval.",unknown:"If the previous order status is unknown, clarify it first and block further entries. Do not assume the previous action never happened."};$("#market-result").textContent=states[b.dataset.marketState];$$("[data-market-state]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)));}
 if(b.dataset.weather){const rain=b.dataset.weather==="rain";$$("[data-weather]").forEach(n=>n.setAttribute("aria-pressed",String(n===b)));$("#garment-one").textContent=rain?"Waterproof jacket":"Breathable top";$("#garment-two").textContent=rain?"Long trousers":"Lightweight bottoms";$("#garment-three").textContent=rain?"Rain gear":"Water bottle";$("#weather-result").textContent=rain?"Example rule: add waterproof gear for rain and an outer layer for cool weather.":"Example rule: choose breathable clothes in hot weather and bring water.";}
 if(b.dataset.studyAnswer){$("#study-result").textContent=b.dataset.studyAnswer==="correct"?"Correct. The original says “registration closes Nov 5, 18:00.” The activity date is not the registration deadline.":"Check the original again: “registration closes Nov 5, 18:00.” Nov 8 is the activity date.";}
 if(b.id==="collection-toggle"){const on=b.getAttribute("aria-pressed")!=="true";b.setAttribute("aria-pressed",String(on));b.textContent=on?"Mark the first book want to read":"Mark the first book finished";$("#collection-result").textContent=(on?1:0)+" / 3 books finished. This status is used only inside this demonstration.";}
});showcase("market");
const contexts={picnic:["A picnic mat, water, and trash bags","Context helps produce suitable suggestions. Check the activity notice for the actual rules."],library:["A library card, notebook, and books to read","The same question can need a different suggestion when the context changes."],unknown:["Ask first: where, what activity, and which rules?","When key information is missing, clarifying the request is more useful than inventing an answer."]};
$$("[data-context]").forEach(b=>b.addEventListener("click",()=>{const[a,n]=contexts[b.dataset.context];$("#context-answer").textContent=a;$("#context-note").textContent=n;$$("[data-context]").forEach(x=>x.setAttribute("aria-pressed",String(x===b)));}));
const notices="Fictional teaching data. Scenario date: 2026-11-02. All dates and times use Asia/Taipei.\nNotice A (Nov 2): Community nature observation is on Nov 8 (Sun), 09:00–12:00. Registration closes Nov 5 (Thu), 18:00. Register through the community form; success requires a confirmation email.\nNotice B (Nov 1, old): The craft class was originally Nov 7 (Sat), 10:00, in the first-floor classroom.\nNotice C (Nov 2, correction): Updates B to Nov 7 (Sat), 14:00, in the second-floor classroom. Reply by Nov 4 (Wed), 20:00, to say whether you can attend.\nNotice D (Nov 2): Collect the parcel at the designated store before Nov 6 (Fri), as stated in the notice. Opening hours and an exact final pickup time are not provided.";
const phoneTask="Use only notices A–D to draft tasks. Include what to do, the action deadline, activity time, source, and information to confirm. Corrections take priority over old notices. Separate activity dates from registration deadlines. Mark unspecified times or statuses as “to confirm”; do not invent them. Organize only: do not register, send replies, or pay.";
const prompts={
 notices,"phone-short":notices+"\n\nPlease organize notices A–D into a task list.","phone-full":notices+"\n\n"+phoneTask,
 gmail:"Use Gmail to find emails accessible in this search from the last seven days. List matters needing my reply or action, with original email sources, deadlines, and search scope. Read does not mean completed. Mark unclear deadlines “to confirm.” Do not claim to cover every task. Read and organize only.",
 drive:"Use Google Drive to read only the plan documents I specify (ask me for the document links first). Confirm dates, headcount, currency, and per-person or whole-group pricing before comparing totals and included items. Cite document sources and mark gaps; do not guess. Say clearly if you find a filename but cannot read its contents. Read and organize only.",
 budget:"Fictional travel budget: day trips for four adults on the same day, all in New Taiwan dollars (TWD). Plan A costs NT$800 per person plus NT$1,200 transport for the whole group; lunch cost is missing. Plan B costs NT$4,000 for the whole group, including transport and lunch. Show calculations for known costs, comparison conditions, and missing information. Do not treat unknown costs as zero.",
 revision:"Use this only if the issue actually occurs: After I check two items, the display still says 0 completed. Please fix the count update and list tests for checking, unchecking, and resetting everything. Keep my title and checklist text.",
 feature:"Please add “Bring a small towel” to my checklist. Keep the existing items and interactions. Then explain how I should check the new total and reset. Change only this practice project; do not deploy it."
};
async function copyText(text,message="Copied. You can paste this into your AI conversation.") {
 try{await navigator.clipboard.writeText(text);toast(message);}
 catch{const dialog=document.createElement("dialog"),title=document.createElement("h3"),area=document.createElement("textarea"),close=document.createElement("button");title.textContent="Select and copy this text manually";area.value=text;area.rows=10;area.setAttribute("aria-label","Practice content to copy");close.textContent="Close";close.className="button small";dialog.style.cssText="max-width:650px;width:90%;border:1px solid #cfd4dc;border-radius:16px;padding:25px";dialog.append(title,area,close);document.body.append(dialog);close.addEventListener("click",()=>dialog.close());dialog.addEventListener("close",()=>dialog.remove());dialog.showModal();area.focus();area.select();}
}
$$("[data-copy]").forEach(b=>b.addEventListener("click",()=>{const content=b.dataset.copy==="build"?$("#build-prompt").value:prompts[b.dataset.copy]||"";if(!content){toast("Enter at least three items and create your build request first.");return;}copyText(content);}));
$("#copy-followup").addEventListener("click",()=>{const value=$("#phone-followup").value.trim();if(!value){toast("Write one follow-up requirement first.");return;}copyText(value,"Follow-up copied. Paste it into the same AI conversation, then check the revised result.");});
$("#share-route").addEventListener("click",()=>copyText("https://k1everwann.github.io/ai-life-lab/en/practice.html?route="+(progress.route==="computer"?"computer":"phone")+"#classroom","Copied this route's public English share link."));
const correct={q1:"contradicted",q2:"supported",q3:"unknown"};
const explanations={q1:"① Contradicted: A says registration closes Nov 5, 18:00. Nov 8 is the activity date.",q2:"② Supported: C corrects the class to Nov 7, 14:00, second floor, replacing old notice B.",q3:"③ Cannot determine yet: D gives no store opening hours. The 22:00 claim has no source."};
if(progress.audit)for(const[name,value]of Object.entries(progress.audit)){const el=$('input[name="'+name+'"][value="'+value+'"]');if(el)el.checked=true;}
$("#audit-form").addEventListener("submit",event=>{
 event.preventDefault();const data=new FormData(event.currentTarget);let score=0;progress.audit={};const box=$("#audit-feedback");box.replaceChildren();
 for(const name of Object.keys(correct)){const value=data.get(name);progress.audit[name]=value;if(value===correct[name])score++;}
 const title=document.createElement("strong");title.textContent=score+" / 3 judgments match the reference answers.";box.append(title);
 for(const[name,ex]of Object.entries(explanations)){const p=document.createElement("p");p.textContent=(progress.audit[name]===correct[name]?"✓ ":"Think again: ")+ex;box.append(p);}save();
});
$("#check-budget").addEventListener("click",()=>{const raw=$("#budget-answer").value.trim(),n=Number(raw);$("#budget-feedback").textContent=!raw?"Enter your calculated amount first.":n===4400?"Correct: 800 × 4 + 1,200 = NT$4,400. These are only Plan A's known costs; lunch is extra. Missing costs are not zero.":"Check again: calculate four people's fees, then add whole-group transport once. Lunch cost is still unknown.";});
function makeBrief(){
 const title=$("#project-title").value.trim()||"My everyday checklist",purpose=$("#project-purpose").value.trim()||"Organize my everyday tasks",items=$("#project-items").value.split(/\r?\n/).map(x=>x.trim()).filter(Boolean).slice(0,20);
 if(items.length<3){$("#build-prompt").value="";toast("Enter at least three checklist items.");return;}
 $("#build-prompt").value="In a new practice folder, create a single index.html file titled “"+title+"”.\nPurpose: "+purpose+"\nChecklist items: "+items.join("; ")+"\n\nRequirements:\n1. Use English and include the title, purpose, and checklist above.\n2. Allow checking and unchecking, updating the completed count immediately.\n3. Include a Reset all button that clears both checks and count.\n4. Keep it readable and usable at a 390px phone width, with easy-to-tap buttons and checkboxes.\n5. Keep HTML, CSS, and JavaScript in one file. No external packages, web fonts, APIs, or login.\n6. The first version does not keep checked progress after refreshing or closing. Explain this on screen.\n7. Work only in this practice folder. Do not change other files or publish online.\n\nProvide the complete code, explain how to save the file as UTF-8 index.html and open it, and list hands-on tests for checking, unchecking, Reset all, and a narrow screen.";
}
$("#brief-form").addEventListener("submit",e=>{e.preventDefault();makeBrief();});makeBrief();
function download(name,content,type="text/plain;charset=utf-8"){const blob=new Blob([content],{type}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),10000);}
$("#load-sample").addEventListener("click",async()=>{try{const r=await fetch("examples/my-checklist.html");if(!r.ok)throw new Error();const sample=new DOMParser().parseFromString(await r.text(),"text/html");sample.querySelector(".example-languages")?.remove();$("#html-code").value="<!doctype html>\n"+sample.documentElement.outerHTML;$("#preview-status").textContent="Finished example loaded. Choose “Preview my webpage” to view and test it.";}catch{$("#preview-status").textContent="Could not load the example. Open the finished-example link above, or paste your complete HTML code.";}});
$("#run-preview").addEventListener("click",()=>{
 const code=$("#html-code").value.trim();if(!code){$("#preview-status").textContent="Paste HTML code or load the finished example first.";return;}
 const policy='<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; img-src data:; connect-src \'none\'; frame-src \'none\'; object-src \'none\'; base-uri \'none\'; form-action \'none\'">';
 const safecode=/<head(?:\s[^>]*)?>/i.test(code)?code.replace(/<head(?:\s[^>]*)?>/i,m=>m+policy):policy+code;
 $("#code-preview").srcdoc=safecode;$("#preview-status").textContent="Isolated preview updated. Try checking, unchecking, and reset to confirm the count stays correct.";
});
$("#download-code").addEventListener("click",()=>{const code=$("#html-code").value.trim();if(!code){toast("Paste HTML code or load an example first.");return;}download("index.html",code,"text/html;charset=utf-8");toast("Download requested. Confirm that the HTML file was saved successfully.");});
$$("[data-check]").forEach(b=>{b.checked=Boolean(progress[b.dataset.check]);b.addEventListener("change",()=>{progress[b.dataset.check]=b.checked;save();});});
function makeCard(){
 const checks=$$("[data-check]").map(b=>(b.checked?"[Personally checked] ":"[Not checked yet] ")+b.parentElement.textContent.trim()).join("\n");
 return "AI Life Lab | My takeaway card\nRoute: "+(progress.route==="computer"?"Computer: build a webpage":"Phone: everyday tasks")+"\n\nMy checked result today:\n"+($("#my-completed").value.trim()||"Not filled in yet")+"\n\nWhat I want to do next:\n"+($("#my-next-task").value.trim()||"Not filled in yet")+"\n\nHow I will check:\n"+($("#my-check").value.trim()||"Not filled in yet")+"\n\n"+(progress.route==="computer"?checks+"\n\n":"")+"Method: Explain the request → Provide material → Get a draft → Check and revise.\nRemember: organizing does not execute tasks; searches are not guaranteed complete. A faithful summary still needs a trustworthy original source.\n";
}
$("#copy-card").addEventListener("click",async()=>{await copyText(makeCard(),"Takeaway card copied. Paste it into your notes and confirm it has saved.");$("#card-status").textContent="After copying, paste into your notes app, then reopen the note to confirm.";});
$("#download-card").addEventListener("click",()=>{download("ai-life-takeaway.txt",makeCard());$("#card-status").textContent="Download requested. Find ai-life-takeaway.txt in your browser downloads or phone files and open it to check the content. If it did not save, use copying instead.";toast("Download requested. Confirm that your takeaway card was saved successfully.");});
$("#reset-progress").addEventListener("click",()=>{progress={};save();$$('input[type="radio"],[data-check]').forEach(x=>x.checked=false);$("#audit-feedback").replaceChildren();toast("This page's checking answers and checkboxes have been cleared on this device. Clear After-class practice progress on its own page.");});
})();
