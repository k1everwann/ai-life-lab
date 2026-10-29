"""Build one complete bilingual lesson, including the worked examples and tool workshop."""
from pathlib import Path
from html import escape
import json
import re

ROOT = Path(__file__).resolve().parents[1]

COPY = {
    'zh-Hant': {
        'title': 'AI 生活應用小講座', 'lead': '先看四個成品，再學會用自己的資料，做出一份可勾選的準備清單。',
        'nav': ['看成品', '接資料', '跟著做', '做出清單', '繼續練'], 'meta': '零基礎 · 電腦操作 · 60 分鐘', 'outcomes': '今天會學會什麼',
        'prepare': '準備一台電腦與你已登入、能使用的 AI 工具。教學資料都在本頁；沒有連接器也能用貼上文字跟著做。',
        'schedule': '看看這 60 分鐘怎麼走', 'schedule_labels': ['四個成品與做法', 'Gmail／Drive／Notion', '自己提問、追問與核對', '做出可勾選的小工具', '保存與課後練習'], 'minute': '分鐘',
        'role_labels': ['需要的資料', 'AI 可以幫忙', '系統負責', '你可以先做'],
        'connect_title': '把自己的資料交給 AI，才有自己的答案', 'connect_lead': '先從一封信、一份文件或一頁筆記開始。下面每一段都有做法、可貼上的資料、示範結果與小練習。',
        'setup_title': '第一次接帳號，照這四步', 'setup': [
            '在 ChatGPT 的「Plugins／外掛」頁找 Gmail、Google Drive 或 Notion；其他 AI 工具請找它的應用程式或連接設定。',
            '開啟外掛詳情並安裝；有連接提示時，登入你要用的帳號，閱讀這次允許存取的內容與動作。',
            '開始新對話，選用對應外掛，明確指定教學信件、文件連結或筆記頁；先請 AI 說明實際讀到了什麼。',
            '打開回覆附的來源核對。找不到來源時，改貼本頁教學資料；先練會方法，再處理帳號設定。',
        ], 'source_ready': '連接器示範使用事先準備好的教學帳號。自行重做時，先用教學 Gmail 寄一封內容為 A 的信給自己，確認收件匣看得到；B 與 D 建成 Drive 文件、C 建成 Notion 頁，再指定實際主旨、日期或連結。課堂也可直接按下方「複製資料＋這段問法」，用文字完成練習。', 'setup_source': '設定方式依工具與帳號而異。', 'official': 'OpenAI 官方外掛說明',
        'goal': '這一段要完成', 'source': '先看資料', 'prompt': '可以這樣問', 'copy_lesson': '複製資料＋這段問法', 'worked': '對照示範結果', 'fixed': '以下是事先寫好的教學示範；實際 AI 的回答可能不同。', 'check': '回來源確認',
        'quiz': '換你判斷', 'check_answer': '看答案與理由', 'choose_first': '先選一個答案，再看理由。', 'correct': '答對了。', 'incorrect': '再對照一下來源。',
        'practice_title': '跟著做：把旅行資料整理成可執行的下一步', 'practice_lead': '這次只做一件事：找出出發前要處理什麼、什麼時候做，以及哪些還不知道。',
        'weak': '只說這句，AI 還不知道你的資料與目標', 'strong': '說清楚資料、成果與缺漏怎麼處理', 'step1': '1　在教材複製資料與問題', 'step1text': '下面的 A、B、C 是同一趟旅行。先讀過，再把資料和問題一起交給 AI。',
        'step2': '2　到 AI 送出，讀第一版草稿', 'step2text': '另開你已能使用的 AI 工具，貼上並送出。這裡是教材；AI 的回答會出現在你的 AI 工具中。保留兩個分頁，方便切回來。',
        'step3': '3　回來寫一個你需要的修改，再到同一個對話追問', 'step3text': '看草稿後，選你真的需要的改法。可參考下列方向，用自己的話修改；這些例子不會代替你送出。',
        'followup_label': '我的補充要求', 'followup_copy': '複製我的追問', 'followup_next': '切到同一個 AI 對話貼上、送出，再帶著新回答回來。',
        'step4': '4　回來源核對，留下你的結果', 'checks': '請對照你自己的 AI 回答核對；勾選只是自己的紀錄。', 'show_reference': '需要時，對照完整參考清單',
        'mistake_check': '檢查我找到的問題', 'mistake_hint': '選出草稿中需要修正的敘述；可複選。', 'mistake_correct': '這兩項需要修正。', 'mistake_retry': '還有選項需要再對照來源。',
        'tool_title': '把清單做成自己能用的小工具', 'tool_intro': '把已核對的待辦一行一項貼進來，產生可勾選、計數、重設的清單。這一步由網站的固定範本製作；AI 幫你整理內容。',
        'tool_name': '清單名稱', 'tool_default': '我的旅行準備清單', 'tool_items': '待辦項目，每行一項', 'tool_items_hint': '帶入文字後，先刪掉標題、提醒與表格線，只留要做的事。需要確認的資訊可寫成「向旅店詢問入住時間」。', 'tool_imported': '已帶入文字；請先整理成一行一項的待辦，再產生清單。', 'tool_placeholder': '11/18 18:00 前回覆旅店人數\n下載車票\n向旅店確認入住時間（待確認）',
        'use_result': '帶入核對結果，再整理待辦', 'sample_tool': '先用教學範例試做', 'build_tool': '產生並預覽清單', 'download_tool': '下載我的清單網頁',
        'tool_empty': '請填清單名稱，並至少寫一項待辦。', 'tool_many': '先保留 30 項以內，讓第一版容易檢查。', 'tool_dirty': '內容已修改，請重新產生預覽後再下載。', 'tool_built': '清單已產生。請在下方試勾、取消與全部重設，再下載。',
        'tool_no_result': '請先填入上方核對後的成果，或用教學範例試做。', 'tool_has_items': '項目欄已有內容；請自行修改，避免覆蓋你的文字。', 'sample_note': '已載入教學範例項目。這是試做，不代表完成了實際 AI 提問。',
        'preview_title': '我的可勾選清單預覽', 'tool_check_title': '親自試這三件事，再帶走', 'tool_checks': ['勾選兩項，完成數變成 2；取消一項，變成 1。', '按「全部重設」，勾選與完成數一起歸零。', '下載 HTML，在瀏覽器重新開啟，能看見自己的名稱與項目。'],
        'tool_reopen': '下載後，到瀏覽器下載清單開啟檔案。保存的是清單檔；第一版重新整理不保留勾選進度。', 'save_title': '把過程與成品一起保存', 'save_text': '文字紀錄留下資料來源、問句、追問與核對結果；HTML 是你剛做好的清單工具。兩份都保存，下次才接得上。',
        'continue_title': '回家後，換成自己的小題目', 'continue_intro': '沿用今天的方法，每次只換一份資料或加一個要求。三個方向可以擇一試做。', 'copy_next': '複製這個練習需求', 'terms': '不熟悉的詞，在這裡查',
        'more': '想深入時，再看其他教材', 'more_text': '下面是獨立延伸，不是完成這場講座的前提。', 'analysis': '信用卡、旅行與市場資料分析', 'web': '用 AI 做網頁的完整選修', 'projects': '網頁作品的修改、測試與復原',
        'footer': '同一頁，從看懂案例到帶走自己的小工具。', 'record_tip': '本頁不會自動保存輸入。切換語言、重新整理或關閉前，先下載或複製紀錄。', 'copied': '已複製，可以貼到你的 AI 工具。',
        'artifact_count': '已完成', 'artifact_reset': '全部重設', 'artifact_note': '第一版不自動保存勾選進度；重新整理後會歸零。', 'artifact_source': '由固定範本產生的個人清單；內容由使用者提供。',
    },
    'en': {
        'title': 'Everyday AI: a short talk', 'lead': 'See four projects, then use your own data to make a checklist you can actually use.',
        'nav': ['See projects', 'Connect data', 'Try it', 'Build a checklist', 'Keep practising'], 'meta': 'For beginners · On a computer · 60 minutes', 'outcomes': 'What you will learn today',
        'prepare': 'Have a computer and an AI tool you can already sign in to and use. All teaching data is on this page; paste the text if you do not have connectors.',
        'schedule': 'See the 60-minute plan', 'schedule_labels': ['Four projects and how they work', 'Gmail / Drive / Notion', 'Ask, refine, and check', 'Build a usable checklist', 'Save and continue'], 'minute': 'min',
        'role_labels': ['Source data', 'What AI can help with', 'What the system does', 'Your first small step'],
        'connect_title': 'Give AI your data to get an answer about your situation', 'connect_lead': 'Start with one email, file, or note. Each lesson below includes steps, paste-ready data, a worked result, and a small practice question.',
        'setup_title': 'Connecting an account for the first time: four steps', 'setup': [
            'In ChatGPT, open Plugins and find Gmail, Google Drive, or Notion. In another AI tool, look for its app or connection settings.',
            'Open the plugin details and install it. When asked to connect, sign in to the intended account and review the content and actions you are allowing.',
            'Start a new chat, use the appropriate plugin, and specify the teaching email, file link, or note page. First ask AI to describe what it actually read.',
            'Open the cited source to check it. If the source is unavailable, paste the teaching text below; practise the method before troubleshooting account settings.',
        ], 'source_ready': 'Connector demonstrations use a prepared teaching account. To repeat them yourself, first send an email containing A to your own teaching Gmail and confirm it is in the inbox; create B and D as Drive files and C as a Notion page, then specify the actual subject, date, or links. In class, you can use “Copy data + this request” below to practise with the text directly.', 'setup_source': 'Setup varies by tool and account.', 'official': 'Official OpenAI plugin guide',
        'goal': 'What to complete', 'source': 'Read the source', 'prompt': 'A request to try', 'copy_lesson': 'Copy data + this request', 'worked': 'Compare the worked result', 'fixed': 'This is a prepared teaching example; your actual AI response may differ.', 'check': 'Check against the source',
        'quiz': 'Your turn to decide', 'check_answer': 'See the answer and reason', 'choose_first': 'Choose an answer before checking the reason.', 'correct': 'Correct.', 'incorrect': 'Check the source again.',
        'practice_title': 'Try it: turn travel details into useful next steps', 'practice_lead': 'Complete one task: find what must be done before departure, when to do it, and what is still unknown.',
        'weak': 'This leaves AI guessing about your data and goal', 'strong': 'Specify the material, result, and how to handle gaps', 'step1': '1　Copy the data and question on this page', 'step1text': 'Sources A, B, and C describe the same trip. Read them first, then give both the material and request to AI.',
        'step2': '2　Send it in your AI tool and read the draft', 'step2text': 'Open your available AI tool in another tab, paste, and send. This page is the lesson; the AI response appears in your AI tool. Keep both tabs open.',
        'step3': '3　Write one change you need, then ask in the same chat', 'step3text': 'Read the draft and choose a useful change. Use the suggestions as a starting point and edit in your own words; they do not send anything for you.',
        'followup_label': 'One requirement I want to add', 'followup_copy': 'Copy my follow-up', 'followup_next': 'Paste it into the same AI conversation, send, and return with the revised answer.',
        'step4': '4　Check the sources and keep your own result', 'checks': 'Check your actual AI response against the sources. Ticks are your own record.', 'show_reference': 'If needed, compare the complete reference list',
        'mistake_check': 'Check the problems I found', 'mistake_hint': 'Select the statements that need correcting. Choose more than one if needed.', 'mistake_correct': 'These two statements need correction.', 'mistake_retry': 'Some choices need another look at the source.',
        'tool_title': 'Turn the list into a tool you can use', 'tool_intro': 'Paste one checked task per line to make a checklist with ticks, a count, and reset. This step uses the website’s fixed template; AI helps organize the content.',
        'tool_name': 'Checklist name', 'tool_default': 'My travel preparation checklist', 'tool_items': 'Tasks, one per line', 'tool_items_hint': 'After bringing in text, remove headings, reminders, and table separators. Keep actions only. Turn unknowns into tasks such as “Ask the inn about check-in time”.', 'tool_imported': 'Text brought in. Edit it into one action per line before building the checklist.', 'tool_placeholder': 'Reply to the inn by 11/18 at 18:00\nDownload tickets\nConfirm check-in time with the inn (to confirm)',
        'use_result': 'Bring in my result, then edit the tasks', 'sample_tool': 'Try it with the teaching example', 'build_tool': 'Build and preview my checklist', 'download_tool': 'Download my checklist webpage',
        'tool_empty': 'Enter a checklist name and at least one task.', 'tool_many': 'Keep the first version to 30 tasks so it is easy to check.', 'tool_dirty': 'The content changed. Rebuild the preview before downloading.', 'tool_built': 'Your checklist is ready. Try ticking, unticking, and resetting below, then download it.',
        'tool_no_result': 'Fill in your checked result above, or try the teaching example.', 'tool_has_items': 'The task field already has content. Edit it yourself to keep your words.', 'sample_note': 'Teaching-example tasks loaded. This trial does not mean you completed an actual AI request.',
        'preview_title': 'My checklist preview', 'tool_check_title': 'Try these three things before taking it away', 'tool_checks': ['Tick two tasks: the count becomes 2. Untick one: it becomes 1.', 'Use “Reset all”: the ticks and count both return to zero.', 'Download the HTML and reopen it in a browser. Check your name and tasks are present.'],
        'tool_reopen': 'Open the file from your browser’s downloads. You saved the checklist file; this first version does not retain ticks after a refresh.', 'save_title': 'Save both the process and the finished tool', 'save_text': 'The text record keeps your sources, request, follow-up, and checked result. The HTML is your checklist tool. Keep both so you can continue next time.',
        'continue_title': 'Try a small topic of your own at home', 'continue_intro': 'Reuse today’s method. Change one source or add one requirement at a time. Choose one of these three directions.', 'copy_next': 'Copy this practice request', 'terms': 'Look up unfamiliar terms',
        'more': 'Other material for when you want to go further', 'more_text': 'These are separate extensions, not prerequisites for this talk.', 'analysis': 'Card spending, travel, and market data analysis', 'web': 'The full optional AI webpage workshop', 'projects': 'Revise, test, and restore a webpage project',
        'footer': 'One page, from understanding the examples to taking away your own small tool.', 'record_tip': 'This page does not save input automatically. Copy or download your record before switching language, refreshing, or closing.', 'copied': 'Copied. You can paste it into your AI tool.',
        'artifact_count': 'Completed', 'artifact_reset': 'Reset all', 'artifact_note': 'This first version does not save ticks automatically; refreshing resets them.', 'artifact_source': 'A personal checklist made from a fixed template with content supplied by its user.',
    },
}

def p(text, cls=''):
    return '<p' + (f' class="{cls}"' if cls else '') + '>' + escape(text) + '</p>'

def listing(values, ordered=False):
    tag = 'ol' if ordered else 'ul'
    return '<' + tag + '>' + ''.join('<li>' + escape(x) + '</li>' for x in values) + '</' + tag + '>'

def pre(text, cls=''):
    return '<pre class="lesson-text ' + cls + '">' + escape(text) + '</pre>'

def source(source):
    return '<div class="source-note"><h4>' + escape(source['label']) + '</h4>' + p(source['text']) + '</div>'

def showcase(lang, base, extra, c):
    html = (ROOT / 'templates' / ('showcase-' + lang + '.html')).read_text(encoding='utf-8')
    html = re.sub(r'<p class="eyebrow">.*?</p>', '<p class="eyebrow">01 · ' + ('看成品 · 8 分鐘' if lang == 'zh-Hant' else 'See projects · 8 min') + '</p>', html, count=1)
    html = html.replace(base['fiction'], '四個專案的功能，以虛構資料示意。' if lang == 'zh-Hant' else 'Four project concepts, demonstrated with fictional data.')
    html = re.sub(r'<div class="photo-placeholder".*?</div>', '', html, flags=re.S)
    for key, notes in extra['showcaseNotes'].items():
        block = '<dl class="project-method">' + ''.join('<div><dt>' + escape(label) + '</dt><dd>' + escape(notes[field]) + '</dd></div>' for label, field in zip(c['role_labels'], ('data', 'ai', 'system', 'firstStep'))) + '</dl>'
        target = p(base['demoIntents'][key])
        assert target in html, key
        html = html.replace(target, target + block, 1)
    return html

def legacy_render(lang, data, course):
    en = lang == 'en'
    t, x, c = data['locales'][lang], course['locales'][lang], COPY[lang]
    prefix = '../' if en else ''
    sections = ['showcase', 'principles', 'classroom', 'tool', 'continue']
    nav = ''.join('<a href="#' + key + '">' + label + '</a>' for key, label in zip(sections, c['nav']))
    language = '<div class="language-switch" role="group" aria-label="Language"><a href="' + ('../' if en else '') + 'index.html" data-language-switch="zh-Hant" lang="zh-Hant"' + ('' if en else ' aria-current="page"') + '>繁體中文</a><a href="' + ('' if en else 'en/') + 'index.html" data-language-switch="en" lang="en"' + (' aria-current="page"' if en else '') + '>English</a></div>'
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(c['lead'], quote=True)}"><title>{c['title']}</title><link rel="stylesheet" href="{prefix}styles.css?v=5"><link rel="stylesheet" href="{prefix}seminar.css?v=2"><link rel="stylesheet" href="{prefix}course.css?v=1"><script src="{prefix}seminar.js?v=2" defer></script><script src="{prefix}course.js?v=1" defer></script><script src="{prefix}language.js?v=4" defer></script></head><body class="seminar-page course-page"><a class="skip" href="#main">{t['skip']}</a><header class="site-header"><a class="brand" href="#top">AI Life Lab</a><nav aria-label="{'Course navigation' if en else '課程導覽'}">{nav}</nav>{language}</header><main id="main" class="seminar-main">
<section id="top" class="wrap section intro">{p(c['meta'],'eyebrow')}<h1>{c['title']}</h1>{p(c['lead'],'lead')}<h2 class="outcome-title">{c['outcomes']}</h2>{listing(x['outcomes'])}{p(c['prepare'],'small-text')}<ol class="chapter-strip">{''.join('<li><a href="#'+key+'"><span>'+str(i)+'</span>'+label+'</a></li>' for i,(key,label) in enumerate(zip(sections,c['nav']),1))}</ol><details class="seminar-schedule"><summary>{c['schedule']}</summary><ol>{''.join('<li><span>'+label+'</span><b>'+str(row['minutes'])+' '+c['minute']+'</b></li>' for label,row in zip(c['schedule_labels'],course['schedule']))}</ol></details></section>
'''
    html += '<noscript>' + p(('互動需要 JavaScript；所有步驟、資料與示範結果仍可直接閱讀，文字可手動複製。' if not en else 'JavaScript is needed for interaction. You can still read every step, source, and worked result, and copy text manually.'), 'wrap notice') + '</noscript>'
    html += showcase(lang, t, x, c)
    html += '<section id="principles" class="wrap section">' + p('02 · ' + ('接資料 · 24 分鐘' if not en else 'Connect data · 24 min'), 'eyebrow') + '<h2>' + c['connect_title'] + '</h2>' + p(c['connect_lead'])
    html += '<details class="setup-guide" open><summary>' + c['setup_title'] + '</summary>' + listing(c['setup'], True) + p(c['source_ready'], 'source-ready') + p(c['setup_source']) + '<a href="https://learn.chatgpt.com/docs/plugins" target="_blank" rel="noopener">' + c['official'] + ' ↗</a></details>'
    sources = {s['key']: s for s in t['sources']}
    for lesson in x['lessons']:
        key = lesson['key']
        pack = [sources['A']] if key == 'gmail' else ([x['sourceD'], sources['B']] if key == 'drive' else [sources['C']])
        html += '<article class="app-lesson" id="lesson-' + key + '"><h3>' + escape(lesson['title']) + '</h3>' + p(c['goal'] + '：' + lesson['goal'], 'lesson-goal') + listing(lesson['steps'], True)
        html += '<div class="worked-pair"><div><h4>' + c['source'] + '</h4>' + ''.join(source(s) for s in pack) + '<h4>' + c['prompt'] + '</h4>' + pre(lesson['prompt']) + '<button class="button" type="button" data-copy-lesson="' + key + '">' + c['copy_lesson'] + '</button><p id="copy-' + key + '-status" class="feedback" role="status"></p></div><div class="worked-answer"><h4>' + escape(lesson['exampleTitle']) + '</h4>' + p(c['fixed'], 'small-text') + pre(lesson['example']) + '<h4>' + c['check'] + '</h4>' + p(lesson['check']) + '</div></div>'
        html += p(lesson['alternate'], 'small-text') + '<fieldset class="lesson-question"><legend>' + c['quiz'] + '：' + escape(lesson['practiceQuestion']) + '</legend>' + ''.join('<label><input type="radio" name="lesson-' + key + '" value="' + str(i) + '"><span>' + escape(choice) + '</span></label>' for i, choice in enumerate(lesson['practiceChoices'])) + '<button class="button outline" type="button" data-check-lesson="' + key + '">' + c['check_answer'] + '</button><p id="question-' + key + '-feedback" class="feedback" role="status"></p></fieldset></article>'
    html += '</section><section id="classroom" class="wrap section">' + p('03 · ' + ('跟著做 · 12 分鐘' if not en else 'Try it · 12 min'), 'eyebrow') + '<h2>' + c['practice_title'] + '</h2>' + p(c['practice_lead']) + '<h3>' + escape(x['promptLesson']['title']) + '</h3><div class="prompt-comparison"><div><h4>' + c['weak'] + '</h4>' + pre(x['promptLesson']['weak']) + '</div><div><h4>' + c['strong'] + '</h4>' + pre(x['promptLesson']['strong']) + '</div></div>' + listing(x['promptLesson']['why'])
    html += '<div class="practice-step"><h3>' + c['step1'] + '</h3>' + p(c['step1text']) + '<details><summary>' + c['source'] + ' A、B、C</summary>' + ''.join(source(s) for s in t['sources']) + '</details><button type="button" id="copy-initial" class="button">' + t['copyInitial'] + '</button><p id="initial-feedback" class="feedback" role="status"></p></div>'
    html += '<div class="practice-step"><h3>' + c['step2'] + '</h3>' + p(c['step2text']) + '</div><div class="practice-step"><h3>' + c['step3'] + '</h3>' + p(c['step3text']) + listing(x['promptLesson']['followups']) + '<label for="learner-followup">' + c['followup_label'] + '</label><textarea id="learner-followup" rows="3" maxlength="2000"></textarea><button type="button" id="copy-followup" class="button">' + c['followup_copy'] + '</button><p id="followup-feedback" class="feedback" role="status"></p>' + p(c['followup_next']) + '</div>'
    m = x['mistakeExercise']
    html += '<div class="practice-step"><h3>' + c['step4'] + '</h3><h4>' + escape(m['title']) + '</h4>' + pre(m['draft']) + '<fieldset class="lesson-question"><legend>' + c['mistake_hint'] + '</legend>' + ''.join('<label><input type="checkbox" data-mistake="' + choice['key'] + '"><span>' + escape(choice['label']) + '</span></label>' for choice in m['choices']) + '<button type="button" id="check-mistakes" class="button outline">' + c['mistake_check'] + '</button><p id="mistake-feedback" class="feedback" role="status"></p></fieldset>'
    html += p(c['checks']) + '<div class="check-list">' + ''.join('<label><input type="checkbox" data-check="' + str(i) + '"><span>' + escape(check) + '</span></label>' for i, check in enumerate(t['checks'])) + '</div><details><summary>' + c['show_reference'] + '</summary>' + p(t['exampleNote']) + pre(t['example']) + '</details><label for="learner-result">' + t['resultLabel'] + '</label><textarea id="learner-result" rows="7" maxlength="20000"></textarea><label for="practice-mode">' + t['modeLabel'] + '</label><select id="practice-mode">' + ''.join('<option value="' + key + '">' + escape(value) + '</option>' for key, value in t['modeOptions'].items()) + '</select></div></section>'
    html += '<section id="tool" class="wrap section">' + p('04 · ' + ('做出清單 · 13 分鐘' if not en else 'Build a checklist · 13 min'), 'eyebrow') + '<h2>' + c['tool_title'] + '</h2>' + p(c['tool_intro']) + '<label for="tool-title">' + c['tool_name'] + '</label><input id="tool-title" type="text" maxlength="100" value="' + c['tool_default'] + '"><label for="tool-items">' + c['tool_items'] + '</label>' + p(c['tool_items_hint'], 'small-text') + '<textarea id="tool-items" rows="6" maxlength="12000" placeholder="' + escape(c['tool_placeholder'], quote=True) + '"></textarea><div class="actions"><button type="button" id="use-result" class="button outline">' + c['use_result'] + '</button><button type="button" id="load-tool-example" class="button outline">' + c['sample_tool'] + '</button></div><div class="actions"><button type="button" id="build-checklist" class="button">' + c['build_tool'] + '</button><button type="button" id="download-tool" class="button outline" disabled>' + c['download_tool'] + '</button></div><p id="tool-status" class="feedback" role="status"></p><iframe id="checklist-preview" hidden title="' + c['preview_title'] + '" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe><h3>' + c['tool_check_title'] + '</h3>' + listing(c['tool_checks'], True) + p(c['tool_reopen']) + '</section>'
    html += '<section id="takeaway" class="wrap section"><h2>' + c['save_title'] + '</h2>' + p(c['save_text']) + p(c['record_tip'], 'notice') + '<div class="actions"><button type="button" id="copy-record" class="button">' + t['copyRecord'] + '</button><button type="button" id="download-record" class="button outline">' + t['download'] + '</button></div><p id="record-feedback" class="feedback" role="status"></p></section>'
    html += '<section id="continue" class="wrap section">' + p('05 · ' + ('繼續練 · 3 分鐘' if not en else 'Keep practising · 3 min'), 'eyebrow') + '<h2>' + c['continue_title'] + '</h2>' + p(c['continue_intro'])
    for i, step in enumerate(x['continueSteps']):
        html += '<article class="continue-step"><h3>' + escape(step['title']) + '</h3>' + p(step['text']) + pre(step['prompt']) + '<button type="button" class="button outline" data-copy-next="' + str(i) + '">' + c['copy_next'] + '</button><p id="next-' + str(i) + '-status" class="feedback" role="status"></p></article>'
    html += '<details><summary>' + c['terms'] + '</summary><dl class="glossary">' + ''.join('<dt>' + escape(item['term']) + '</dt><dd>' + escape(item['meaning']) + '</dd>' for item in x['glossary']) + '</dl></details><details><summary>' + c['more'] + '</summary>' + p(c['more_text']) + '<ul><li><a href="analysis.html">' + c['analysis'] + '</a></li><li><a href="practice.html?route=computer#classroom">' + c['web'] + '</a></li><li><a href="web-project.html">' + c['projects'] + '</a></li></ul></details></section></main>'
    html += '<section id="copy-fallback" class="wrap manual-copy" hidden><label for="manual-copy">' + t['manualLabel'] + '</label>' + p(t['copyManual']) + '<textarea id="manual-copy" rows="8" readonly></textarea></section><footer class="wrap seminar-footer">' + c['footer'] + '</footer>'
    for identifier, value in (('seminar-data', data), ('course-data', course), ('course-ui', COPY)):
        html += '<script id="' + identifier + '" type="application/json">' + json.dumps(value, ensure_ascii=False, indent=2).replace('</', '<\\/') + '</script>'
    return html + '</body></html>\n'

def render(lang, data, course):
    from build_curriculum import render as render_curriculum
    return render_curriculum(lang, data, course, showcase, COPY[lang])


def redirect(lang, target):
    en = lang == 'en'
    title = 'The complete lesson is on one page' if en else '完整講座已整合在同一頁'
    return f'''<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="index.html"><title>{title}</title></head><body><h1>{title}</h1><a href="{target}">{'Open the complete lesson' if en else '開啟完整講座'}</a><nav aria-label="Language"><a href="{'../' if en else ''}index.html" data-language-switch="zh-Hant" lang="zh-Hant">繁體中文</a><a href="{'' if en else 'en/'}index.html" data-language-switch="en" lang="en">English</a></nav></body></html>\n'''

def build():
    from build_curriculum import write_materials
    write_materials()
    data = json.loads((ROOT / 'seminar-content.json').read_text(encoding='utf-8'))
    course = json.loads((ROOT / 'course-content.json').read_text(encoding='utf-8'))
    for lang in ('zh-Hant', 'en'):
        directory = ROOT / 'en' if lang == 'en' else ROOT
        (directory / 'index.html').write_text(render(lang, data, course), encoding='utf-8', newline='\n')
        (directory / 'instructor.html').write_text(redirect(lang, 'index.html'), encoding='utf-8', newline='\n')
        (directory / 'next-steps.html').write_text(redirect(lang, 'index.html#continue'), encoding='utf-8', newline='\n')

if __name__ == '__main__':
    build()
