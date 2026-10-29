"""Outcome-first lesson layout; existing fixtures and downloads stay reusable."""
import hashlib
import json
from html import escape as esc
from pathlib import Path
from visual_guides import chat_guide, connection_guide, figure, note, zoom_dialog

ROOT = Path(__file__).resolve().parents[1]
LABELS = {
    'zh-Hant': {
        'home':'所有課程', 'menu':'選擇課程', 'title':'用 AI，完成生活中的一件小事',
        'intro':'整理一封信、比較一份帳單，或做出自己的小工具。選一件想做的事，跟著操作就能開始。',
        'start':'開始第一個練習', 'browse':'我想自己選課', 'first':'不知道選哪課？',
        'firstnote':'第一次使用，從第 1 課「把活動通知變成待辦」開始。已經用過 AI，可以直接選 Gmail、帳單分析或製作網頁。',
        'how':'怎麼使用這份教材', 'howsteps':['在這裡看步驟，在自己的 AI 工具操作。','先用提供的範例完成一次，再換成自己的需求。','完成後保存成果；下次直接接著選課。'],
        'ready':'準備好一台電腦，以及能登入的 AI 工具（例如 ChatGPT）。基本練習不需要連接 Gmail、Drive 或 Notion。',
        'groups':['把想法說清楚','整理信件、文件與數字','做自己的工具','表達與自己的應用'],
        'mapnote':'不用按順序上完。點選想做的事；會的內容可以帶過，需要時再看進一步練習。',
        'outcome':'做完，你會得到', 'sample':'成果示意', 'samplehint':'這是預先寫好的範例；你的 AI 用詞可以不同。',
        'follow':'跟著做', 'where':'操作位置：自己的 AI 工具', 'source':'練習資料',
        'prompt':'給 AI 的要求', 'copy':'複製資料與要求', 'open':'開啟 ChatGPT ↗',
        'copynote':'複製後，切到 AI 的新對話，貼上並送出。保留教材分頁，方便回來看下一步。',
        'reference':'做完再看：結果可以長這樣', 'check':'看結果時，注意這幾件事',
        'change':'接著，改成你要的樣子', 'own':'換個情境，自己試一次',
        'ownhint':'沿用剛才的方法，把下方情境交給 AI。', 'advanced':'還想多學一點？',
        'quick':'我已經會了，直接練習', 'challenge':'試試更進一步的任務',
        'finish':'保存成果，下次繼續', 'finishnote':'把 AI 回答存進自己的筆記，並留下一句「我改了什麼」。想用本站整理，可展開下方紀錄。',
        'record':'寫下與下載這次成果（選用）', 'selfcheck':'想確認自己理解了嗎？（選用）',
        'more':'需要哪些基礎？', 'trouble':'結果不一樣，怎麼辦？',
        'troubletext':'用詞不必一模一樣。先檢查有沒有漏掉資料；若有錯，直接對 AI 說「這裡應該是……，請修正」。有問題時連同原文一起問。',
        'connection':'想讓 AI 直接讀取帳號中的資料？', 'connectcopy':'複製連線練習要求',
        'connectnote':'前面的貼文字練習不需要連線。這一段才會使用你允許 AI 存取的教學資料。',
        'setup':'連接 Gmail、Google Drive 或 Notion', 'setupintro':'連接器讓 AI 讀取你允許的服務資料，省去逐段複製。連線在你的 AI 工具完成，這個教材網站不會連接帳號。',
        'setupsteps':['在 ChatGPT 中尋找 Plugins（外掛）或連接應用程式的入口，搜尋 Gmail、Google Drive 或 Notion。畫面不同時，可參考下方官方說明。','依畫面提示連接，確認登入的是你要用的帳號，並閱讀要求的存取範圍。','回到對話選用該服務，指定要讀的信件或文件。完成後，開啟原始資料確認內容。'],
        'unavailable':'可用功能依方案與工作區而異。找不到服務或無法連接時，先完成貼文字練習，之後再試連線。',
        'official':'查看官方操作說明 ↗', 'continue':'課後繼續',
        'continuedesc':'完成一個練習後，換一份資料再做一次。遇到新需求時，回來選對應的課程。',
        'savehint':'本頁不會自動保存。關閉或切換語言前，先下載已填的紀錄；下載的教材本身不包含你的答案。',
        'nextideas':['整理資料之後 → 試 Gmail、Drive 或 Notion。','看懂每月差異之後 → 換自己的去識別化資料再比較。','做出小網頁之後 → 改一個功能，再回來學怎麼修正錯誤。'],
        'minutes':'分鐘，含延伸練習', 'lesson':'第 {n} 課', 'next':'下一課', 'previous':'上一課',
    },
    'en': {
        'home':'All lessons', 'menu':'Choose a lesson', 'title':'Use AI to finish one useful everyday task',
        'intro':'Organize an email, compare a bill, or build a small tool. Pick something you want to do and follow the steps.',
        'start':'Start the first exercise', 'browse':'Choose my own lesson', 'first':'Not sure where to start?',
        'firstnote':'New to AI? Start with turning a message into a to-do list. Already using it? Jump to Gmail, spending analysis, or building a webpage.',
        'how':'How to use these lessons', 'howsteps':['Read the steps here; do the work in your own AI tool.','Try the provided example, then adapt it to your needs.','Save your result and return for another lesson whenever you like.'],
        'ready':'Bring a computer and an AI tool you can sign in to, such as ChatGPT. Basic exercises do not require Gmail, Drive, or Notion connections.',
        'groups':['Explain what you want','Organize emails, documents, and numbers','Build your own tools','Communicate and apply'],
        'mapnote':'You do not need to finish every lesson or follow this order. Pick a useful task, skip what you know, and explore further when ready.',
        'outcome':'What you will make', 'sample':'Example result', 'samplehint':'This is a prepared example. Your AI may use different wording.',
        'follow':'Follow along', 'where':'Work in your own AI tool', 'source':'Practice material',
        'prompt':'Request for AI', 'copy':'Copy material and request', 'open':'Open ChatGPT ↗',
        'copynote':'After copying, paste and send in a new AI conversation. Keep this lesson tab open so you can return for the next step.',
        'reference':'After trying: compare a possible result', 'check':'Check these parts of your result',
        'change':'Now make it work for you', 'own':'Try a different situation yourself',
        'ownhint':'Use the same method with the situation below.', 'advanced':'Want to go further?',
        'quick':'I know this — let me practise', 'challenge':'Try a more involved task',
        'finish':'Save your work and continue later', 'finishnote':'Save the AI response in your own notes and add one sentence about what you changed. You can also use the optional record below.',
        'record':'Write and download my result (optional)', 'selfcheck':'Check your understanding (optional)',
        'more':'What should I know first?', 'trouble':'My result looks different. What now?',
        'troubletext':'The wording does not have to match. Check for missing information first. If something is wrong, tell AI what it should be and ask for a correction, including the original material.',
        'connection':'Want AI to read directly from your account?', 'connectcopy':'Copy the connection exercise request',
        'connectnote':'The text exercise above needs no connection. This section uses teaching material you allow AI to access.',
        'setup':'Connect Gmail, Google Drive, or Notion', 'setupintro':'A connector lets AI read material from a service you authorize, saving manual copying. Connect inside your AI tool; this lesson website does not connect your accounts.',
        'setupsteps':['In ChatGPT, look for Plugins or the connected-apps entry and search for Gmail, Google Drive, or Notion. If your screen differs, consult the official walkthrough below.','Follow the connection prompts, check which account you are signing in to, and review the requested access.','Select the service in your conversation and specify the email or document to read. Open the original to check the result.'],
        'unavailable':'Availability depends on your plan and workspace. If you cannot find or connect the service, complete the text exercise first and return to connections later.',
        'official':'Read the official walkthrough ↗', 'continue':'Continue after class',
        'continuedesc':'After completing an exercise, try it again with different material. Come back and pick a lesson when you have a new task.',
        'savehint':'This page does not save automatically. Download your filled-in records before closing or changing language. The lesson download does not include your own answers.',
        'nextideas':['After organizing text → try Gmail, Drive, or Notion.','After comparing months → repeat with your own anonymized data.','After building a webpage → change one feature, then learn to fix errors.'],
        'minutes':'min, including further practice', 'lesson':'Lesson {n}', 'next':'Next lesson', 'previous':'Previous lesson',
    }
}

def render_module(module, lang, modules, prefix):
    from build_curriculum import UI, p, pre, listing, button, workspace
    t=UI[lang]; l=LABELS[lang]; c=module['locales'][lang]; key=module['id']; idx=modules.index(module)
    def copy(kind, label=None):
        return button(label or l['copy'],f'data-copy-module="{key}" data-copy-kind="{kind}"')+f'<p id="copy-{key}-{kind}" role="status"></p>'
    out=f'<article id="{module["anchor"]}" class="module wrap section" data-module="{key}">'
    out+=p(l['lesson'].format(n=idx+1)+' · '+str(module['minutes'])+' '+l['minutes'],'eyebrow')+'<h1 tabindex="-1">'+esc(c['title'])+'</h1>'+p(c.get('why',c['goal']),'lead')
    if c.get('connection'):
        out+='<p class="lesson-mode">'+('Start with the sample text; no account connection is needed. ' if lang=='en' else '先貼上範例文字練習，不需要連接帳號。')+'<a href="#connection-'+key+'">'+('Want to connect your account? →' if lang=='en' else '想連接自己的帳號？→')+'</a></p>'
    out+='<div class="outcome"><strong>'+l['outcome']+'</strong>'+p(c['goal'])+'<div class="example-result"><span>'+l['sample']+'</span>'+p(c.get('outcome',c['expected']))+'</div>'+p(l['samplehint'],'small-text')+'</div>'
    out+='<div class="lesson-shortcuts"><a class="button" href="#do-'+key+'">'+l['follow']+'</a>'+button(l['quick'],f'data-jump-independent="{key}"')+'</div>'
    out+=f'<section class="guided learning-step" id="do-{key}"><h2>1. {l["follow"]}</h2>'+p(l['where'],'eyebrow')+listing(c['steps'],'ol')
    out+='<div class="exercise-material"><h3>'+l['source']+'</h3>'+pre(c['source'])+'<h3>'+l['prompt']+'</h3>'+pre(c['prompt'])+'</div>'
    out+='<div class="actions">'+copy('guided')+'<a class="button outline" href="https://chatgpt.com/" target="_blank" rel="noopener">'+l['open']+'</a></div>'+p(l['copynote'],'small-text')
    out+=chat_guide(lang,prefix,key)
    out+='<details class="reference"><summary>'+l['reference']+'</summary>'+pre(c['expected'])+'</details><h3>'+l['check']+'</h3>'+listing(c['checks'])
    out+='<details><summary>'+l['trouble']+'</summary>'+p(l['troubletext'])+'</details></section>'
    if key in ('M08','M09'):
        out+='<details class="preview-guide"><summary>'+('Where do I paste code and test it?' if lang=='en' else '程式碼要貼哪裡？怎麼看預覽？')+'</summary>'+figure('preview',lang,prefix)+note(lang)+'</details>'
    out+=workspace(module,lang,prefix,t)
    out+='<section class="learning-step"><h2>2. '+l['change']+'</h2>'
    if c.get('followup'):
        f=c['followup'];out+=pre(f['source'])+pre(f['prompt'])+copy('followup')+'<details><summary>'+l['reference']+'</summary>'+pre(f['expected'])+'</details>'
    out+=f'<details class="independent" id="independent-{key}"><summary>{l["own"]}</summary>'+p(l['ownhint'])+pre(c['independent']['task'])
    if key=='M09':
        out+='<p><a download href="'+prefix+'downloads/curriculum/reset-bug-'+lang+'.html">'+('Download the reset exercise' if lang=='en' else '下載這題的練習檔')+'</a></p>'
    out+=copy('independent',t['copytask'])+'<details><summary>'+l['reference']+'</summary>'+pre(c['independent']['expected'])+'</details></details></section>'
    out+='<section class="learning-step"><h2>3. '+l['finish']+'</h2>'+p(l['finishnote'])+'<details class="module-record"><summary>'+l['record']+'</summary>'+p(l['savehint'],'small-text')
    out+=f'<label for="exercise-{key}">{t["exercise"]}</label><select id="exercise-{key}">'+''.join(f'<option value="{v}">{label}</option>' for v,label in zip(('guided','independent','challenge','connection') if c.get('connection') else ('guided','independent','challenge'),t['exercise_types']+['Connected account' if lang=='en' else '連線練習']))+'</select>'
    out+=f'<label for="mode-{key}">{t["mode"]}</label><select id="mode-{key}">'+''.join(f'<option value="{i}">{label}</option>' for i,label in enumerate(t['modes']))+'</select>'
    out+=f'<label for="question-{key}">{t["question"]}</label><textarea id="question-{key}" rows="3" maxlength="12000"></textarea><label for="result-{key}">{t["result"]}</label><textarea id="result-{key}" rows="4" maxlength="30000" placeholder="{t["placeholder"]}"></textarea>'
    for kind in ('guided','independent','challenge','connection'):
        checks=c['checks'] if kind=='guided' else t['other_checks']
        out+=f'<div data-evidence-kind="{kind}"'+(' hidden' if kind!='guided' else '')+'>'+''.join(f'<label class="check-line"><input type="checkbox" data-evidence="{i}"><span>{esc(check)}</span></label>' for i,check in enumerate(checks))+'</div>'
    out+=button(t['download'],f'data-download-record="{key}"')+f'<p id="record-{key}-status" role="status"></p></details><a download href="{prefix}downloads/curriculum/{key.lower()}-{lang}.txt">{t["material"]}</a></section>'
    out+='<section class="learning-step further"><h2>'+l['advanced']+'</h2>'
    if c.get('connection'):
        f=c['connection'];out+=f'<details class="connection" id="connection-{key}"><summary>'+esc(f['title'])+'</summary>'+p(l['connectnote'])+'<a href="#connection-guide">'+l['setup']+'</a>'+connection_guide(lang,prefix,key)+listing(f['steps'],'ol')+pre(f['source'])+pre(f['prompt'])+copy('connection',l['connectcopy'])+'<details><summary>'+l['reference']+'</summary>'+pre(f['expected'])+'</details></details>'
    out+=f'<details class="challenge" id="challenge-{key}"><summary>{l["challenge"]}</summary>'+p(c['challenge']['task'])+pre(c['challenge']['source'])+pre(c['challenge']['prompt'])
    if key=='M09':
        out+='<p><a download href="'+prefix+'downloads/curriculum/search-reset-bug-'+lang+'.html">'+('Download the search exercise' if lang=='en' else '下載搜尋功能練習檔')+'</a></p>'
    out+=copy('challenge')+'<details><summary>'+l['reference']+'</summary>'+pre(c['challenge']['expected'])+'</details></details>'
    if key=='M07':
        out+='<details><summary>'+t['lab7']+'</summary><a download href="'+prefix+'downloads/curriculum/monthly-spending.csv">'+('Download sample CSV' if lang=='en' else '下載範例表格 CSV')+'</a><div class="actions">'+button(t['strict'],'data-threshold="strict" aria-pressed="true"')+button(t['inclusive'],'data-threshold="inclusive" aria-pressed="false"')+'</div><p id="threshold-result" role="status"></p></details>'
    if key=='M10':
        out+='<details><summary>'+t['lab10']+'</summary><label for="sensor-reading">'+t['sensor']+'</label><select id="sensor-reading">'+''.join('<option value="'+v+'">'+label+'</option>' for v,label in zip(('27','28','29','missing'),t['temps']))+'</select><div class="actions">'+button(t['simulate'],'id="simulate-rule"')+button(t['repeat'],'id="repeat-rule" disabled')+button(t['reset'],'id="reset-rule"')+'</div><p id="rule-result" role="status"></p><p id="rule-count" role="status"></p></details>'
    q=c['quiz'];out+='<details><summary>'+l['selfcheck']+'</summary><fieldset class="lesson-question"><legend>'+esc(q['question'])+'</legend>'+''.join(f'<label><input type="radio" name="quiz-{key}" value="{i}"><span>{esc(choice)}</span></label>' for i,choice in enumerate(q['choices']))+button(t['answer'],f'data-check-quiz="{key}"')+f'<p id="quiz-{key}-feedback" role="status"></p></fieldset></details>'
    needs=[m for m in modules if m['id'] in module['needs']]
    if needs:out+='<details><summary>'+l['more']+'</summary>'+p(c['skip'])+'<ul>'+''.join('<li><a href="#'+m['anchor']+'">'+esc(m['locales'][lang]['title'])+'</a></li>' for m in needs)+'</ul></details>'
    out+='</section><nav class="module-pager" aria-label="'+l['menu']+'">'
    if idx:out+='<a href="#'+modules[idx-1]['anchor']+'">← '+l['previous']+'</a>'
    out+='<a href="#course-map">'+l['home']+'</a>'
    if idx+1<len(modules):out+='<a href="#'+modules[idx+1]['anchor']+'">'+l['next']+' →</a>'
    return out+'</nav></article>'

def render(lang):
    from build_curriculum import UI, p, listing, button
    t=UI[lang]; l=LABELS[lang]; en=lang=='en'; prefix='../' if en else ''
    modules=json.loads((ROOT/'curriculum-content.json').read_text(encoding='utf-8'))['modules']
    html=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(l["intro"],quote=True)}"><title>{t["title"]} · AI Life Lab</title>'
    for filename in ('styles.css','curriculum.css','curriculum.js','language.js'):
        url=prefix+filename+'?v='+hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()[:12]
        html+=f'<link rel="stylesheet" href="{url}">' if filename.endswith('.css') else f'<script src="{url}" defer></script>'
    html+='</head><body class="curriculum-page"><a class="skip" href="#main">'+('Skip to content' if en else '跳到主要內容')+'</a><header class="site-header"><a class="brand" href="#top">AI Life Lab</a><nav><a href="#course-map">'+l['home']+'</a><a href="#continue">'+l['continue']+'</a></nav><div class="language-switch" role="group" aria-label="Language"><a href="'+('../' if en else '')+'index.html" data-language-switch="zh-Hant" lang="zh-Hant">繁體中文</a><a href="'+('' if en else 'en/')+'index.html" data-language-switch="en" lang="en">English</a></div></header>'
    nav=''.join(f'<a href="#{m["anchor"]}"><span>{i+1:02}</span>{esc(m["locales"][lang]["title"])}</a>' for i,m in enumerate(modules))
    html+='<aside class="lesson-sidebar"><p>'+l['menu']+'</p><nav aria-label="'+l['menu']+'">'+nav+'</nav></aside><details class="mobile-lessons"><summary>'+l['menu']+'</summary><nav aria-label="'+l['menu']+'">'+nav+'</nav></details><main id="main">'
    html+='<section class="wrap section intro" id="top" data-view="home"><p class="eyebrow">'+('12 practical lessons · Learn at your pace' if en else '12 個實用練習 · 按自己的步調學')+'</p><h1>'+l['title']+'</h1>'+p(l['intro'],'lead')+'<div class="actions"><a class="button" href="#lesson-start">'+l['start']+'</a><a href="#course-map">'+l['browse']+'</a></div><h2>'+l['how']+'</h2>'+listing(l['howsteps'],'ol')+p(l['ready'],'small-text')+'</section>'
    html+='<section class="wrap section" id="course-map" data-view="home"><h2>'+l['menu']+'</h2>'+p(l['mapnote'])+'<p class="start-note"><strong>'+l['first']+'</strong> '+l['firstnote']+'</p>'
    for group,(start,end) in zip(l['groups'],((0,3),(3,7),(7,10),(10,12))):
        html+='<h3>'+group+'</h3><ol class="module-list">'
        for idx in range(start,end):
            m=modules[idx];c=m['locales'][lang]
            html+='<li><a href="#'+m['anchor']+'"><span class="module-number">'+f'{idx+1:02}'+'</span><span><strong>'+esc(c['title'])+'</strong><span class="module-summary">'+esc(c['goal'])+'</span></span><span aria-hidden="true">→</span></a></li>'
        html+='</ol>'
    html+='</section><section class="wrap section" id="connection-guide" data-view="setup"><h1 tabindex="-1">'+l['setup']+'</h1>'+p(l['setupintro'])+connection_guide(lang,prefix)+listing(l['setupsteps'],'ol')+p(l['unavailable'])+'<a href="https://developers.openai.com/training/walkthroughs/plugins-and-skills" target="_blank" rel="noopener">'+l['official']+'</a><div class="actions"><a href="#lesson-gmail">Gmail</a><a href="#lesson-drive">Google Drive</a><a href="#lesson-notion">Notion</a><button id="return-to-connection" type="button">'+('Back to my exercise' if en else '返回剛才的練習')+'</button></div></section>'
    html+=''.join(render_module(m,lang,modules,prefix) for m in modules)
    html+='<section class="wrap section" id="continue" data-view="continue"><span id="takeaway"></span><h1 tabindex="-1">'+l['continue']+'</h1>'+p(l['continuedesc'])+listing(l['nextideas'])+p(l['savehint'])+button(t['saveall'],'id="download-all-records"')+'<p id="all-record-status" role="status"></p><a href="#course-map">'+l['home']+'</a></section><noscript>'+p(t['noscript'])+'</noscript></main>'
    html+='<section class="copy-fallback wrap" id="copy-fallback" hidden><label for="manual-copy">'+t['manual']+'</label><textarea id="manual-copy" rows="8" readonly></textarea>'+button(t['copyreturn'],'id="copy-return"')+'</section><footer class="learning-footer">'+('Fictional practice material · Do the exercises in your own AI tool.' if en else '練習採用虛構資料 · 請在自己的 AI 工具操作')+'</footer>'
    payload={'modules':[{**{k:m[k] for k in ('id','anchor','minutes','needs')},**m['locales'][lang]} for m in modules], 'ui':t}
    return html+zoom_dialog(lang)+'<script id="curriculum-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')+'</script></body></html>\n'
