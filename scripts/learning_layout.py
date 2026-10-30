"""Outcome-first lesson layout; existing fixtures and downloads stay reusable."""
import hashlib
import json
from html import escape as esc
from pathlib import Path
from lesson_tools import debug_links, resume_help
from visual_guides import chat_guide, connection_guide, figure, note, zoom_dialog

ROOT = Path(__file__).resolve().parents[1]
LABELS = {'zh-Hant': {'home': '所有課程',
             'menu': '選擇課程',
             'title': '用 AI，把你的點子做出來',
             'intro': '選一個題目，用 AI 做出第一版，再改成自己的作品。',
             'start': '開始第一個練習',
             'browse': '我想自己選課',
             'first': '不知道選哪課？',
             'firstnote': '第一次接觸？從第 1 課的校園解謎任務卡開始。想做東西？直接選第 8 課的小工具；會的部分可以跳過。',
             'how': '怎麼使用這份教材',
             'howsteps': ['複製資料，貼到 AI。', '改一處，再核對結果。', '保存作品，有興趣再挑戰。'],
             'ready': '課程預設已備妥 AI 帳號。',
             'groups': ['組隊、改計畫、判讀消息', '合作、創作與活動預算', '製作與測試小工具', '介紹作品與自由創作'],
             'mapnote': '選你想做的題目。會的部分直接跳過。',
             'outcome': '做完，你會得到',
             'sample': '成果示意（預先準備）',
             'samplehint': '這是預先寫好的範例；你的 AI 用詞可以不同。',
             'follow': '做出第一版',
             'where': '在 ChatGPT 或你慣用的 AI 工具操作',
             'source': '練習資料',
             'prompt': '給 AI 的要求',
             'copy': '複製資料與要求',
             'open': '開啟 ChatGPT ↗',
             'copynote': '複製後貼到 AI 對話送出，再回來核對。',
             'reference': '看參考答案',
             'check': '檢查這幾點',
             'change': '改一處，再檢查',
             'own': '換個題目，自己試試',
             'ownhint': '這一題可以另開 AI 對話。資料已備好，試著先自己寫要求。',
             'advanced': '還想試別的？',
             'quick': '已經會了，換一題試試',
             'challenge': '試試更進一步的任務',
             'finish': '保存這次作品',
             'finishnote': '把最後的回答存進自己的筆記，留一句「我改了什麼、怎麼確認」。',
             'record': '記下我的要求與結果',
             'selfcheck': '想確認自己理解了嗎？（選用）',
             'more': '需要哪些基礎？',
             'trouble': '結果不一樣，怎麼辦？',
             'troubletext': '用詞不必一模一樣。先檢查有沒有漏掉資料；若有錯，直接對 AI 說「這裡應該是……，請修正」。有問題時連同原文一起問。',
             'connection': '看看連接器還能做什麼（選做）',
             'connectcopy': '複製連線練習要求',
             'connectnote': '先看講師示範，或用已獲授權的教學帳號練習。',
             'setup': '連接帳號：Gmail、Google Drive、Notion',
             'setupintro': '連接後，AI 可以讀取你指定的信件、文件或筆記。請在自己的 AI 工具操作。',
             'setupsteps': ['在 ChatGPT 開啟「設定 → 外掛程式（Plugins）」，搜尋要用的服務。',
                            '按畫面提示安裝或連接，確認帳號與允許讀取的資料。',
                            '回到對話，用 @ 或 + 選服務，貼上練習要求。'],
             'unavailable': '可用功能依方案與工作區而異。找不到服務或無法連接時，先完成貼文字練習，之後再試連線。',
             'official': '查看官方操作說明 ↗',
             'continue': '課後繼續',
             'continuedesc': '完成一個練習後，換一份資料再做一次。遇到新需求時，回來選對應的課程。',
             'savehint': '這裡不會自動保存。關閉或切換語言前，先下載紀錄。',
             'nextideas': ['換個題目，再做一版。', '替小工具加一個功能，找同學試用。'],
             'minutes': '分鐘，含延伸練習',
             'lesson': '第 {n} 課',
             'next': '下一課',
             'previous': '上一課',
             'classroom': '不用 AI，先用預備材料練習',
             'classhint': '下方是事先準備的材料，沒有替你呼叫 AI。',
             'classrecord': '記下我的結果',
             'classanswer': '做完再看：核對重點',
             'classnext': '做完後，保存你的修改與檢查結果。',
             'prepared': '載入預備程式，開始測試',
             'policy': 'ChatGPT：未滿 13 歲由成人實際操作；13–17 歲使用需家長或監護人同意。其他工具依各自規則。',
             'changehint': '在剛才的 AI 對話接著說。可用下面這句，也可以換成你想改的地方。',
             'copychange': '複製修改要求',
             'savecode': '下載網頁檔，從下載清單開啟，再測一次。'},
 'en': {'home': 'All lessons',
        'menu': 'Choose a lesson',
        'title': 'Use AI to make your ideas real',
        'intro': 'Pick a task, make a first version with AI, then make it your own.',
        'start': 'Start the first exercise',
        'browse': 'Choose my own lesson',
        'first': 'Not sure where to start?',
        'firstnote': 'New here? Start with the campus puzzle mission in lesson 1. Want to build something? Jump to lesson 8. Skip what you '
                     'already know.',
        'how': 'How to use these lessons',
        'howsteps': ['Copy the material into AI.', 'Make one change and check it.', 'Save your work; try a challenge if you like.'],
        'ready': 'An AI account is assumed to be ready.',
        'groups': ['Team up, revise plans, check messages',
                   'Collaborate, create, and budget',
                   'Build and test small tools',
                   'Present your work and create freely'],
        'mapnote': 'Choose something you want to make. Skip what you already know.',
        'outcome': 'What you will make',
        'sample': 'Prepared example result',
        'samplehint': 'This is a prepared example. Your AI may use different wording.',
        'follow': 'Make a first version',
        'where': 'Use ChatGPT or your usual AI tool',
        'source': 'Practice material',
        'prompt': 'Request for AI',
        'copy': 'Copy material and request',
        'open': 'Open ChatGPT ↗',
        'copynote': 'Paste and send in your AI conversation, then return to check the result.',
        'reference': 'See a reference answer',
        'check': 'Check these points',
        'change': 'Change one thing and check',
        'own': 'Try a different task',
        'ownhint': 'Start a new AI conversation for this task. The material is ready; try writing your own request first.',
        'advanced': 'Want to try more?',
        'quick': 'I know this — try another task',
        'challenge': 'Try a more involved task',
        'finish': 'Save your work',
        'finishnote': 'Save the final response in your notes. Add what you changed and how you checked it.',
        'record': 'Record my request and result',
        'selfcheck': 'Check your understanding (optional)',
        'more': 'What should I know first?',
        'trouble': 'My result looks different. What now?',
        'troubletext': 'The wording does not have to match. Check for missing information first. If something is wrong, tell AI what it '
                       'should be and ask for a correction, including the original material.',
        'connection': 'Explore what connectors can do (optional)',
        'connectcopy': 'Copy the connection exercise request',
        'connectnote': 'Watch the instructor demonstrate, or use an authorized teaching account.',
        'setup': 'Connect an account: Gmail, Google Drive, Notion',
        'setupintro': 'Once connected, AI can read the emails, documents, or notes you specify. Connect inside your own AI tool.',
        'setupsteps': ['In ChatGPT, open Settings → Plugins and search for the service.',
                       'Follow the install or connect prompts. Check the account and which data it can access.',
                       'Return to your conversation. Use @ or + to select the service, then paste the exercise request.'],
        'unavailable': 'Availability depends on your plan and workspace. If you cannot find or connect the service, complete the text '
                       'exercise first and return to connections later.',
        'official': 'Read the official walkthrough ↗',
        'continue': 'Continue after class',
        'continuedesc': 'After completing an exercise, try it again with different material. Come back and pick a lesson when you have a '
                        'new task.',
        'savehint': 'This page does not save automatically. Download your records before closing or changing language.',
        'nextideas': ['Try another topic and make a new version.', 'Add one feature to your tool and ask a classmate to try it.'],
        'minutes': 'min, including further practice',
        'lesson': 'Lesson {n}',
        'next': 'Next lesson',
        'previous': 'Previous lesson',
        'classroom': 'Practise with prepared material, without AI',
        'classhint': 'This material is prepared in advance; no AI is called for you.',
        'classrecord': 'Record my result',
        'classanswer': 'After trying: what to check',
        'classnext': 'Save your changes and checks when you finish.',
        'prepared': 'Load prepared code and test it',
        'policy': 'ChatGPT: an adult must operate it for under-13s; ages 13–17 need parent or guardian permission. Other tools have their '
                  'own rules.',
        'changehint': 'Continue the same AI conversation. Use the request below or choose a change of your own.',
        'copychange': 'Copy the change request',
        'savecode': 'Download the webpage. Open the downloaded file and test it again.'}}

def account_note(lang):
    l=LABELS[lang]
    return '<p class="small-text">'+l['policy']+' <a href="https://help.openai.com/en/articles/8313401-is-chatgpt-safe-for-all-ages" target="_blank" rel="noopener">'+('Official guidance' if lang=='en' else '官方說明')+'</a></p>'

def render_module(module, lang, modules, prefix):
    from build_curriculum import UI, p, pre, listing, button, workspace
    t=UI[lang]; l=LABELS[lang]; c=module['locales'][lang]; key=module['id']; idx=modules.index(module)
    def copy(kind, label=None):
        return button(('Copy broken code and request' if lang=='en' else '複製故障程式碼與要求') if key=='M09' and kind in ('guided','independent','challenge') else (label or l['copy']),f'data-copy-module="{key}" data-copy-kind="{kind}"')+f'<p id="copy-{key}-{kind}" role="status"></p>'
    out=f'<article id="{module["anchor"]}" class="module wrap section" data-module="{key}">'
    out+=p(l['lesson'].format(n=idx+1),'eyebrow')+'<h1 tabindex="-1">'+esc(c['title'])+'</h1>'+p(c['goal'],'lead')
    out+='<div class="example-result"><span>'+l['sample']+'</span>'+p(c.get('outcome',c['expected']))+'</div>'
    out+='<div class="lesson-shortcuts"><a class="button" href="#do-'+key+'">'+l['follow']+'</a>'+button(l['quick'],f'data-jump-independent="{key}"')+'</div>'
    alternative=f'<details class="classroom-path" id="classroom-{key}"><summary>'+l['classroom']+'</summary>'+p(l['classhint'])+pre(c['classroom']['task'])
    if key not in ('M08','M09'):
        alternative+='<details><summary>'+('Material and prepared result' if lang=='en' else '本課資料與預備結果')+'</summary><h3>'+l['source']+'</h3>'+pre(c['source'])+'<h3>'+l['sample']+'</h3>'+pre(c['expected'])+'</details>'
    if key in ('M08','M09'):
        alternative+=button(l['prepared'],f'data-load-prepared="{key}"')+p(('Prepared teaching code; not generated on this website. Loading replaces existing code only after confirmation.' if lang=='en' else '這是預備教學程式，不是本站生成；已有程式碼時，會先確認才替換。'),'small-text')
    if key=='M09':
        alternative+='<details><summary>'+('After finding the bug: try the reference fix' if lang=='en' else '找出錯誤後：試試參考修正版')+'</summary>'+button(('Load the reference fix' if lang=='en' else '載入參考修正版'),f'data-load-prepared="{key}" data-prepared-fixed="true"')+p(('This replaces the workspace with prepared corrected code. Preview, test, then download this version.' if lang=='en' else '將工作區換成預備的參考修正版；請更新預覽、測試，再下載此版本。'))+'</details>'
    alternative+='<details><summary>'+l['classanswer']+'</summary>'+pre(c['classroom']['expected'])+'</details>'+p(l['classnext'])+button(l['classrecord'],f'data-classroom-record="{key}"')+'</details>'
    out+=f'<section class="guided learning-step" id="do-{key}"><h2>1. {l["follow"]}</h2>'+p(l['where'],'eyebrow')+listing(c['steps'],'ol')
    if key=='M09':out+=debug_links(lang,prefix,'guided')
    out+='<div class="exercise-material"><h3>'+l['source']+'</h3>'+pre(c['source'])+'<h3>'+l['prompt']+'</h3>'+pre(c['prompt'])+'</div>'
    out+='<div class="actions">'+copy('guided')+'<a class="button outline" href="https://chatgpt.com/" target="_blank" rel="noopener">'+l['open']+'</a></div>'+p(l['copynote'],'small-text')
    if key in ('M08','M09'):out+='<p><a href="#workspace-'+key+'">'+('I have the code — go to the preview workspace ↓' if lang=='en' else '已拿到程式碼？前往貼上與預覽 ↓')+'</a></p>'
    out+=chat_guide(lang,prefix,key)
    out+='<details class="reference"><summary>'+l['reference']+'</summary>'+pre(c['expected'])+'</details><h3>'+l['check']+'</h3>'+listing(c['checks'])
    out+='<details><summary>'+l['trouble']+'</summary>'+p(l['troubletext'])+'</details></section>'
    if key in ('M08','M09'):
        out+='<details class="preview-guide"><summary>'+('Where do I paste code and test it?' if lang=='en' else '程式碼要貼哪裡？怎麼看預覽？')+'</summary>'+figure('preview',lang,prefix)+note(lang,'preview')+'</details>'
    out+=workspace(module,lang,prefix,t)
    out+='<section class="learning-step" id="change-'+key+'"><h2>2. '+l['change']+'</h2>'+p(l['changehint'])
    if c.get('followup'):
        f=c['followup'];out+=(pre(f['source']) if f['source'] else '')+pre(f['prompt'])+copy('followup',l['copychange'])+p(f['expected'],'revision-check')
    if key in ('M08','M09'):out+='<a href="#workspace-'+key+'">'+('Return to the code and preview ↑' if lang=='en' else '回上方貼上新版程式碼並預覽 ↑')+'</a>'
    out+='</section>'
    out+='<section class="learning-step" id="save-'+key+'"><h2>3. '+l['finish']+'</h2>'+p(l['finishnote'])
    if key in ('M08','M09'):out+=p(l['savecode'])+button(t['codedownload'],f'data-code-download="{key}"')+f'<p id="code-download-status-{key}" role="status"></p>'
    out+=resume_help(lang)+'<details class="module-record"><summary>'+l['record']+'</summary>'+p(l['savehint'],'small-text')
    out+=f'<label for="exercise-{key}">{t["exercise"]}</label><select id="exercise-{key}">'+''.join(f'<option value="{v}">{label}</option>' for v,label in zip(('guided','independent','challenge','connection') if c.get('connection') else ('guided','independent','challenge'),t['exercise_types']+['Connected account' if lang=='en' else '連線練習']))+'</select>'
    out+=f'<label for="mode-{key}">{t["mode"]}</label><select id="mode-{key}">'+''.join(f'<option value="{i}">{label}</option>' for i,label in enumerate(t['modes']))+'</select>'
    out+=f'<label for="question-{key}">{t["question"]}</label><textarea id="question-{key}" rows="3" maxlength="12000"></textarea><label for="result-{key}">{t["result"]}</label><textarea id="result-{key}" rows="4" maxlength="30000" placeholder="{t["placeholder"]}"></textarea>'
    for kind in ('guided','independent','challenge','connection','classroom'):
        checks=c['checks'] if kind=='guided' else t['other_checks']
        out+=f'<div data-evidence-kind="{kind}"'+(' hidden' if kind!='guided' else '')+'>'+''.join(f'<label class="check-line"><input type="checkbox" data-evidence="{i}"><span>{esc(check)}</span></label>' for i,check in enumerate(checks))+'</div>'
    out+=button(t['download'],f'data-download-record="{key}"')+f'<p id="record-{key}-status" role="status"></p></details><a download href="{prefix}downloads/curriculum/{key.lower()}-{lang}.txt">{t["material"]}</a></section>'
    out+='<section class="learning-step further"><h2>'+l['advanced']+'</h2>'
    out+=f'<details class="independent" id="independent-{key}"><summary>{l["own"]}</summary>'+p(l['ownhint'])+pre(c['independent']['source'])+pre(c['independent']['task'])
    if key=='M09':out+=debug_links(lang,prefix,'independent')
    out+=copy('independent',t['copytask'])
    if key in ('M08','M09'):out+='<a href="#workspace-'+key+'">'+('Paste and preview the code ↑' if lang=='en' else '貼上程式碼並預覽 ↑')+'</a>'
    out+='<details><summary>'+l['reference']+'</summary>'+pre(c['independent']['expected'])+'</details></details>'
    if c.get('connection'):
        f=c['connection'];out+=f'<details class="connection" id="connection-{key}"><summary>'+esc(f['title'])+'</summary>'+p(l['connectnote'])+pre(f['source'])+'<a href="#connection-guide">'+l['setup']+'</a>'+listing(f['steps'],'ol')+pre(f['prompt'])+copy('connection',l['connectcopy'])+'<details><summary>'+('See the connection screen' if lang=='en' else '看連接帳號的畫面')+'</summary>'+connection_guide(lang,prefix,key)+'</details><details><summary>'+l['reference']+'</summary>'+pre(f['expected'])+'</details></details>'
    out+=f'<details class="challenge" id="challenge-{key}"><summary>{l["challenge"]}</summary>'+p(c['challenge']['task'])+pre(c['challenge']['source'])+pre(c['challenge']['prompt'])
    if key=='M09':out+=debug_links(lang,prefix,'challenge')
    out+=copy('challenge')
    if key in ('M08','M09'):out+='<a href="#workspace-'+key+'">'+('Paste and preview the code ↑' if lang=='en' else '貼上程式碼並預覽 ↑')+'</a>'
    out+='<details><summary>'+l['reference']+'</summary>'+pre(c['challenge']['expected'])+'</details></details>'
    if key=='M07':
        out+='<details><summary>'+t['lab7']+'</summary><a download href="'+prefix+'downloads/curriculum/monthly-spending.csv">'+('Download sample CSV' if lang=='en' else '下載範例表格 CSV')+'</a><div class="actions">'+button(t['strict'],'data-threshold="strict" aria-pressed="true"')+button(t['inclusive'],'data-threshold="inclusive" aria-pressed="false"')+'</div><p id="threshold-result" role="status"></p></details>'
    if key=='M10':
        out+='<details><summary>'+t['lab10']+'</summary><label for="sensor-reading">'+t['sensor']+'</label><select id="sensor-reading">'+''.join('<option value="'+v+'">'+label+'</option>' for v,label in zip(('27','28','29','missing'),t['temps']))+'</select><div class="actions">'+button(t['simulate'],'id="simulate-rule"')+button(t['repeat'],'id="repeat-rule" disabled')+button(t['reset'],'id="reset-rule"')+'</div><p id="rule-result" role="status"></p><p id="rule-count" role="status"></p></details>'
    q=c['quiz'];out+='<details><summary>'+l['selfcheck']+'</summary><fieldset class="lesson-question"><legend>'+esc(q['question'])+'</legend>'+''.join(f'<label><input type="radio" name="quiz-{key}" value="{i}"><span>{esc(choice)}</span></label>' for i,choice in enumerate(q['choices']))+button(t['answer'],f'data-check-quiz="{key}"')+f'<p id="quiz-{key}-feedback" role="status"></p></fieldset></details>'
    needs=[m for m in modules if m['id'] in module['needs']]
    if needs:out+='<details><summary>'+l['more']+'</summary><ul>'+''.join('<li><a href="#'+m['anchor']+'">'+esc(m['locales'][lang]['title'])+'</a></li>' for m in needs)+'</ul></details>'
    out+=alternative+'</section><nav class="module-pager" aria-label="'+l['menu']+'">'
    if idx:out+='<a href="#'+modules[idx-1]['anchor']+'">← '+l['previous']+'</a>'
    out+='<a href="#course-map">'+l['home']+'</a>'
    if idx+1<len(modules):out+='<a href="#'+modules[idx+1]['anchor']+'">'+l['next']+' →</a>'
    return out+'</nav></article>'

def render(lang):
    from build_curriculum import UI, p, listing, button, checklist_fixture, reset_fixture, search_fixture
    t=UI[lang]; l=LABELS[lang]; en=lang=='en'; prefix='../' if en else ''
    modules=json.loads((ROOT/'curriculum-content.json').read_text(encoding='utf-8'))['modules']
    html=f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{esc(l["intro"],quote=True)}"><title>{t["title"]} · AI Life Lab</title>'
    for filename in ('styles.css','curriculum.css','curriculum.js','language.js'):
        url=prefix+filename+'?v='+hashlib.sha256((ROOT/filename).read_bytes()).hexdigest()[:12]
        html+=f'<link rel="stylesheet" href="{url}">' if filename.endswith('.css') else f'<script src="{url}" defer></script>'
    html+='</head><body class="curriculum-page"><a class="skip" href="#main">'+('Skip to content' if en else '跳到主要內容')+'</a><header class="site-header"><a class="brand" href="#top">AI Life Lab</a><nav><a href="#course-map">'+l['home']+'</a><a href="#continue">'+l['continue']+'</a></nav><div class="language-switch" role="group" aria-label="Language"><a href="'+('../' if en else '')+'index.html" data-language-switch="zh-Hant" lang="zh-Hant">繁體中文</a><a href="'+('' if en else 'en/')+'index.html" data-language-switch="en" lang="en">English</a></div></header>'
    nav=''.join(f'<a href="#{m["anchor"]}"><span>{i+1:02}</span>{esc(m["locales"][lang]["title"])}</a>' for i,m in enumerate(modules))
    html+='<aside class="lesson-sidebar"><p>'+l['menu']+'</p><nav aria-label="'+l['menu']+'">'+nav+'</nav></aside><details class="mobile-lessons"><summary>'+l['menu']+'</summary><nav aria-label="'+l['menu']+'">'+nav+'</nav></details><main id="main">'
    html+='<section class="wrap section intro" id="top" data-view="home"><p class="eyebrow">'+('12 creative tasks · Choose your challenge' if en else '12 個動手做的題目 · 自選挑戰')+'</p><h1>'+l['title']+'</h1>'+p(l['intro'],'lead')+'<div class="actions"><a class="button" href="#lesson-start">'+l['start']+'</a><a href="#course-map">'+l['browse']+'</a></div>'+p(' → '.join(l['howsteps']),'small-text')+'<details><summary>'+('Class preparation (optional)' if en else '課前準備（選看）')+'</summary>'+p(l['ready'])+account_note(lang)+'</details></section>'
    html+='<section class="wrap section" id="course-map" data-view="home"><h2>'+l['menu']+'</h2>'+p(l['mapnote'])
    for group,(start,end) in zip(l['groups'],((0,3),(3,7),(7,10),(10,12))):
        html+='<h3>'+group+'</h3><ol class="module-list">'
        for idx in range(start,end):
            m=modules[idx];c=m['locales'][lang]
            html+='<li><a href="#'+m['anchor']+'"><span class="module-number">'+f'{idx+1:02}'+'</span><span><strong>'+esc(c['title'])+'</strong><span class="module-summary">'+esc(c['goal'])+'</span></span><span aria-hidden="true">→</span></a></li>'
        html+='</ol>'
    html+='</section><section class="wrap section" id="connection-guide" data-view="setup"><h1 tabindex="-1">'+l['setup']+'</h1>'+p(l['setupintro'])+listing(l['setupsteps'],'ol')+p(l['unavailable'])+'<a href="https://help.openai.com/en/articles/11487775-connected-apps-in-chatgpt" target="_blank" rel="noopener">'+l['official']+'</a>'+connection_guide(lang,prefix)+'<div class="actions"><a href="#lesson-gmail">Gmail</a><a href="#lesson-drive">Google Drive</a><a href="#lesson-notion">Notion</a><button id="return-to-connection" type="button">'+('Back to my exercise' if en else '返回剛才的練習')+'</button></div></section>'
    html+=''.join(render_module(m,lang,modules,prefix) for m in modules)
    html+='<section class="wrap section" id="continue" data-view="continue"><span id="takeaway"></span><h1 tabindex="-1">'+l['continue']+'</h1>'+p(l['continuedesc'])+resume_help(lang)+listing(l['nextideas'])+p(l['savehint'])+button(t['saveall'],'id="download-all-records"')+'<p id="all-record-status" role="status"></p><a href="#course-map">'+l['home']+'</a></section><noscript>'+p(t['noscript'])+'</noscript></main>'
    html+='<section class="copy-fallback wrap" id="copy-fallback" hidden><label for="manual-copy">'+t['manual']+'</label><textarea id="manual-copy" rows="8" readonly></textarea>'+button(t['copyreturn'],'id="copy-return"')+'</section><footer class="learning-footer">'+('Fictional material · Make one change, show one check, save your work.' if en else '練習採用虛構資料 · 自己改一處、核對一次、保存作品')+'</footer>'
    payload={'modules':[{**{k:m[k] for k in ('id','anchor','minutes','needs')},**m['locales'][lang]} for m in modules], 'ui':t,'preparedFixtures':{'M08':checklist_fixture(lang,False),'M09':checklist_fixture(lang,True),'M09fixed':checklist_fixture(lang,False)},'debugFixtures':{'guided':checklist_fixture(lang,True),'independent':reset_fixture(lang,True),'challenge':search_fixture(lang,True)}}
    html+='<dialog id="prepared-confirm" aria-labelledby="prepared-title"><h2 id="prepared-title">'+('Replace the guided exercise code?' if en else '取代主練習的程式碼？')+'</h2>'+p(('Your guided exercise already has code. Cancel and download it first if you want to keep it. Other exercises will be preserved.' if en else '主練習已有程式碼。要保留時，請先取消並下載；其他練習的內容會保留。'))+'<div class="actions">'+button(('Cancel, keep my code' if en else '取消，保留原碼'),'id="prepared-cancel" autofocus')+button(('Replace with prepared code' if en else '確認載入預備程式'),'id="prepared-replace"')+'</div></dialog>'
    return html+zoom_dialog(lang)+'<script id="curriculum-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')+'</script></body></html>\n'
