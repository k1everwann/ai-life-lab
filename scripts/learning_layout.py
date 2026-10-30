"""Outcome-first lesson layout; existing fixtures and downloads stay reusable."""
import hashlib
import json
from html import escape as esc
from pathlib import Path
from lesson_tools import debug_links, resume_help
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

# Shared tasks, freely chosen depth: account access is not a prerequisite.
LABELS['zh-Hant'].update({
    'title':'用 AI，把你的點子做出來',
    'intro':'辦一場社團活動、整理創作分工，或做一個能用的小工具。選你有興趣的題目，做出第一版，再改成自己的版本。',
    'firstnote':'第一次接觸？從第 1 課的校園解謎任務卡開始。想做東西？直接選第 8 課的小工具；會的部分可以跳過。',
    'howsteps':['先看講師展示，再選一課做出第一版。','自己決定改一處，用資料或操作測試確認。','保存作品；還有時間就選做挑戰，不必全班同速。'],
    'ready':'帶電腦即可參與。沒有 AI 帳號也能使用每課的預備材料，親手修改、判讀和測試。',
    'groups':['組隊、改計畫、判讀消息','合作、創作與活動預算','製作與測試小工具','介紹作品與自由創作'],
    'mapnote':'混齡同班，共用題目、自由選難度。每人先交出一份作品、一項自己的修改、一個核對證據；已會就直接做挑戰。',
    'where':'AI 由符合使用條件的學員或成人講師操作',
    'copynote':'符合工具使用條件者可自行貼上；其他學員把要求交給成人講師操作，或選本課「不用 AI 帳號也能做」。',
    'ownhint':'沿用剛才的方法，自己寫要求，再自行操作、交給講師，或用預備材料判讀。',
    'finishnote':'保存作品，寫下「我決定改什麼、用什麼證明沒改錯」。註明用了 AI、講師預備材料或同伴協助；完成後開一次下載檔。',
    'connectnote':'這是成人講師示範，或符合各服務使用條件者的選做練習。只用指定教學資料，不需要連接私人帳號。',
    'connection':'看看連接器還能做什麼（選做）',
    'setupintro':'連接器讓 AI 讀取你允許的服務資料，省去逐段複製。由成人講師示範，符合各服務使用條件者才自行連接；本站不連接帳號。',
    'nextideas':['把社團任務卡換成閱讀、創作或出遊計畫。','替小工具改一個功能，請同伴用一次。','沒有 AI 帳號：先修改自己的文字成果、核對來源，留下下次想請講師測試的要求。'],
    'classroom':'不用 AI 帳號也能做', 'classhint':'使用預備材料做修改與核對；這不算親自生成 AI 回答。',
    'classrecord':'寫下我的修改與核對', 'classanswer':'做完再看：核對重點',
    'classnext':'完成後直接保存成果；AI 操作步驟可留到成人講師示範時再看。',
    'prepared':'載入預備程式，開始測試',
    'policy':'ChatGPT：未滿 13 歲由成人實際操作；13–17 歲使用需家長或監護人同意。其他工具依各自規則。',
})
LABELS['en'].update({
    'title':'Use AI to make your ideas real',
    'intro':'Plan a club activity, organize a creative team, or build a useful little tool. Pick a topic, make a first version, then make it your own.',
    'firstnote':'New here? Start with the campus puzzle mission in lesson 1. Want to build something? Jump to lesson 8. Skip what you already know.',
    'howsteps':['Watch the instructor demonstrate, then pick a lesson and make a first version.','Choose one change yourself, then check it against the material or a test.','Save your work. Try a challenge if you have time; everyone can work at a different pace.'],
    'ready':'Bring a computer. No AI account is required to take part: each lesson has prepared material you can edit, evaluate, and test.',
    'groups':['Team up, revise plans, check messages','Collaborate, create, and budget','Build and test small tools','Present your work and create freely'],
    'mapnote':'One mixed-age class, shared tasks, freely chosen depth. Make something, choose one change, and show one check. Already know how? Try a challenge.',
    'where':'AI is operated by an eligible learner or an adult instructor',
    'copynote':'Eligible users can paste the request themselves. Otherwise, give it to an adult instructor or choose this lesson’s “Try it without an AI account”.',
    'ownhint':'Write your own request. Use an eligible account, give it to the instructor, or evaluate prepared material.',
    'finishnote':'Save your work and explain what you chose to change and how you checked it. Credit AI, prepared material, or peer help. Open your downloaded file once.',
    'connectnote':'An optional adult-led demonstration, or practice for users eligible for each service. Use designated teaching material; private accounts are not required.',
    'connection':'Explore what connectors can do (optional)',
    'setupintro':'A connector lets AI read material from a service you authorize. Watch an adult instructor demonstrate; connect yourself only if eligible for each service. This website does not connect accounts.',
    'nextideas':['Turn a club mission card into a reading, creative, or trip plan.','Change one tool feature and ask a peer to try it.','No AI account? Edit your saved text, check the sources, and bring a request for the instructor to test next time.'],
    'classroom':'Try it without an AI account', 'classhint':'Edit and check prepared material. This is not a claim that you generated an AI response yourself.',
    'classrecord':'Record my change and check', 'classanswer':'After trying: what to check',
    'classnext':'Go straight to saving your work when done. You can revisit the AI steps with an adult instructor later.',
    'prepared':'Load prepared code and test it',
    'policy':'ChatGPT: an adult must operate it for under-13s; ages 13–17 need parent or guardian permission. Other tools have their own rules.',
})

def account_note(lang):
    l=LABELS[lang]
    return '<p class="small-text">'+l['policy']+' <a href="https://help.openai.com/en/articles/8313401-is-chatgpt-safe-for-all-ages" target="_blank" rel="noopener">'+('Official guidance' if lang=='en' else '官方說明')+'</a></p>'

LABELS['zh-Hant'].update({
    'intro':'選一個題目，用 AI 做出第一版，再改成自己的作品。',
    'howsteps':['複製資料，貼到 AI。','改一處，再核對結果。','保存作品，有興趣再挑戰。'],
    'ready':'課程預設已備妥 AI 帳號。',
    'mapnote':'選你想做的題目。會的部分直接跳過。',
    'where':'在 ChatGPT 或你慣用的 AI 工具操作',
    'copynote':'複製後貼到 AI 對話送出，再回來核對。',
    'ownhint':'換個題目，用剛才的方法再試一次。',
    'finishnote':'存下成果，留一句「我改了什麼、怎麼確認」。',
    'nextideas':['換個題目，再做一版。','替小工具加一個功能，找同學試用。'],
})
LABELS['en'].update({
    'intro':'Pick a task, make a first version with AI, then make it your own.',
    'howsteps':['Copy the material into AI.','Make one change and check it.','Save your work; try a challenge if you like.'],
    'ready':'An AI account is assumed to be ready.',
    'mapnote':'Choose something you want to make. Skip what you already know.',
    'where':'Use ChatGPT or your usual AI tool',
    'copynote':'Paste and send in your AI conversation, then return to check the result.',
    'ownhint':'Try the same method with a different task.',
    'finishnote':'Save your result and note what you changed and how you checked it.',
    'nextideas':['Try another topic and make a new version.','Add one feature to your tool and ask a classmate to try it.'],
})

def render_module(module, lang, modules, prefix):
    from build_curriculum import UI, p, pre, listing, button, workspace
    t=UI[lang]; l=LABELS[lang]; c=module['locales'][lang]; key=module['id']; idx=modules.index(module)
    def copy(kind, label=None):
        return button(('Copy broken code and request' if lang=='en' else '複製故障程式碼與要求') if key=='M09' else (label or l['copy']),f'data-copy-module="{key}" data-copy-kind="{kind}"')+f'<p id="copy-{key}-{kind}" role="status"></p>'
    out=f'<article id="{module["anchor"]}" class="module wrap section" data-module="{key}">'
    out+=p(l['lesson'].format(n=idx+1)+' · '+str(module['minutes'])+' '+l['minutes'],'eyebrow')+'<h1 tabindex="-1">'+esc(c['title'])+'</h1>'+p(c['goal'],'lead')
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
        out+='<details class="preview-guide"><summary>'+('Where do I paste code and test it?' if lang=='en' else '程式碼要貼哪裡？怎麼看預覽？')+'</summary>'+figure('preview',lang,prefix)+note(lang)+'</details>'
    out+=workspace(module,lang,prefix,t)
    out+='<section class="learning-step"><h2>2. '+l['change']+'</h2>'
    if c.get('followup'):
        f=c['followup'];out+=pre(f['source'])+pre(f['prompt'])+copy('followup')+'<details><summary>'+l['reference']+'</summary>'+pre(f['expected'])+'</details>'
    out+=f'<details class="independent" id="independent-{key}"><summary>{l["own"]}</summary>'+p(l['ownhint'])+pre(c['independent']['task'])
    if key=='M09':out+=debug_links(lang,prefix,'independent')
    out+=copy('independent',t['copytask'])+'<details><summary>'+l['reference']+'</summary>'+pre(c['independent']['expected'])+'</details></details></section>'
    out+='<section class="learning-step" id="save-'+key+'"><h2>3. '+l['finish']+'</h2>'+p(l['finishnote'])+resume_help(lang)+'<details class="module-record"><summary>'+l['record']+'</summary>'+p(l['savehint'],'small-text')
    out+=f'<label for="exercise-{key}">{t["exercise"]}</label><select id="exercise-{key}">'+''.join(f'<option value="{v}">{label}</option>' for v,label in zip(('guided','independent','challenge','connection') if c.get('connection') else ('guided','independent','challenge'),t['exercise_types']+['Connected account' if lang=='en' else '連線練習']))+'</select>'
    out+=f'<label for="mode-{key}">{t["mode"]}</label><select id="mode-{key}">'+''.join(f'<option value="{i}">{label}</option>' for i,label in enumerate(t['modes']))+'</select>'
    out+=f'<label for="question-{key}">{t["question"]}</label><textarea id="question-{key}" rows="3" maxlength="12000"></textarea><label for="result-{key}">{t["result"]}</label><textarea id="result-{key}" rows="4" maxlength="30000" placeholder="{t["placeholder"]}"></textarea>'
    for kind in ('guided','independent','challenge','connection','classroom'):
        checks=c['checks'] if kind=='guided' else t['other_checks']
        out+=f'<div data-evidence-kind="{kind}"'+(' hidden' if kind!='guided' else '')+'>'+''.join(f'<label class="check-line"><input type="checkbox" data-evidence="{i}"><span>{esc(check)}</span></label>' for i,check in enumerate(checks))+'</div>'
    out+=button(t['download'],f'data-download-record="{key}"')+f'<p id="record-{key}-status" role="status"></p></details><a download href="{prefix}downloads/curriculum/{key.lower()}-{lang}.txt">{t["material"]}</a></section>'
    out+='<section class="learning-step further"><h2>'+l['advanced']+'</h2>'
    if c.get('connection'):
        f=c['connection'];out+=f'<details class="connection" id="connection-{key}"><summary>'+esc(f['title'])+'</summary>'+p(l['connectnote'])+'<a href="#connection-guide">'+l['setup']+'</a>'+connection_guide(lang,prefix,key)+listing(f['steps'],'ol')+pre(f['source'])+pre(f['prompt'])+copy('connection',l['connectcopy'])+'<details><summary>'+l['reference']+'</summary>'+pre(f['expected'])+'</details></details>'
    out+=f'<details class="challenge" id="challenge-{key}"><summary>{l["challenge"]}</summary>'+p(c['challenge']['task'])+pre(c['challenge']['source'])+pre(c['challenge']['prompt'])
    if key=='M09':out+=debug_links(lang,prefix,'challenge')
    out+=copy('challenge')+'<details><summary>'+l['reference']+'</summary>'+pre(c['challenge']['expected'])+'</details></details>'
    if key=='M07':
        out+='<details><summary>'+t['lab7']+'</summary><a download href="'+prefix+'downloads/curriculum/monthly-spending.csv">'+('Download sample CSV' if lang=='en' else '下載範例表格 CSV')+'</a><div class="actions">'+button(t['strict'],'data-threshold="strict" aria-pressed="true"')+button(t['inclusive'],'data-threshold="inclusive" aria-pressed="false"')+'</div><p id="threshold-result" role="status"></p></details>'
    if key=='M10':
        out+='<details><summary>'+t['lab10']+'</summary><label for="sensor-reading">'+t['sensor']+'</label><select id="sensor-reading">'+''.join('<option value="'+v+'">'+label+'</option>' for v,label in zip(('27','28','29','missing'),t['temps']))+'</select><div class="actions">'+button(t['simulate'],'id="simulate-rule"')+button(t['repeat'],'id="repeat-rule" disabled')+button(t['reset'],'id="reset-rule"')+'</div><p id="rule-result" role="status"></p><p id="rule-count" role="status"></p></details>'
    q=c['quiz'];out+='<details><summary>'+l['selfcheck']+'</summary><fieldset class="lesson-question"><legend>'+esc(q['question'])+'</legend>'+''.join(f'<label><input type="radio" name="quiz-{key}" value="{i}"><span>{esc(choice)}</span></label>' for i,choice in enumerate(q['choices']))+button(t['answer'],f'data-check-quiz="{key}"')+f'<p id="quiz-{key}-feedback" role="status"></p></fieldset></details>'
    needs=[m for m in modules if m['id'] in module['needs']]
    if needs:out+='<details><summary>'+l['more']+'</summary>'+p(c['skip'])+'<ul>'+''.join('<li><a href="#'+m['anchor']+'">'+esc(m['locales'][lang]['title'])+'</a></li>' for m in needs)+'</ul></details>'
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
    html+='</section><section class="wrap section" id="connection-guide" data-view="setup"><h1 tabindex="-1">'+l['setup']+'</h1>'+p(l['setupintro'])+connection_guide(lang,prefix)+listing(l['setupsteps'],'ol')+p(l['unavailable'])+'<a href="https://developers.openai.com/training/walkthroughs/plugins-and-skills" target="_blank" rel="noopener">'+l['official']+'</a><div class="actions"><a href="#lesson-gmail">Gmail</a><a href="#lesson-drive">Google Drive</a><a href="#lesson-notion">Notion</a><button id="return-to-connection" type="button">'+('Back to my exercise' if en else '返回剛才的練習')+'</button></div></section>'
    html+=''.join(render_module(m,lang,modules,prefix) for m in modules)
    html+='<section class="wrap section" id="continue" data-view="continue"><span id="takeaway"></span><h1 tabindex="-1">'+l['continue']+'</h1>'+p(l['continuedesc'])+resume_help(lang)+listing(l['nextideas'])+p(l['savehint'])+button(t['saveall'],'id="download-all-records"')+'<p id="all-record-status" role="status"></p><a href="#course-map">'+l['home']+'</a></section><noscript>'+p(t['noscript'])+'</noscript></main>'
    html+='<section class="copy-fallback wrap" id="copy-fallback" hidden><label for="manual-copy">'+t['manual']+'</label><textarea id="manual-copy" rows="8" readonly></textarea>'+button(t['copyreturn'],'id="copy-return"')+'</section><footer class="learning-footer">'+('Fictional material · Make one change, show one check, save your work.' if en else '練習採用虛構資料 · 自己改一處、核對一次、保存作品')+'</footer>'
    payload={'modules':[{**{k:m[k] for k in ('id','anchor','minutes','needs')},**m['locales'][lang]} for m in modules], 'ui':t,'preparedFixtures':{'M08':checklist_fixture(lang,False),'M09':checklist_fixture(lang,True),'M09fixed':checklist_fixture(lang,False)},'debugFixtures':{'guided':checklist_fixture(lang,True),'independent':reset_fixture(lang,True),'challenge':search_fixture(lang,True)}}
    html+='<dialog id="prepared-confirm" aria-labelledby="prepared-title"><h2 id="prepared-title">'+('Replace the guided exercise code?' if en else '取代主練習的程式碼？')+'</h2>'+p(('Your guided exercise already has code. Cancel and download it first if you want to keep it. Other exercises will be preserved.' if en else '主練習已有程式碼。要保留時，請先取消並下載；其他練習的內容會保留。'))+'<div class="actions">'+button(('Cancel, keep my code' if en else '取消，保留原碼'),'id="prepared-cancel" autofocus')+button(('Replace with prepared code' if en else '確認載入預備程式'),'id="prepared-replace"')+'</div></dialog>'
    return html+zoom_dialog(lang)+'<script id="curriculum-data" type="application/json">'+json.dumps(payload,ensure_ascii=False).replace('</',r'<\/')+'</script></body></html>\n'
