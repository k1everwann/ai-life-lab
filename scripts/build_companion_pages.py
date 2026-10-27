"""Build the bilingual seminar guide and the simple after-class entry points."""
from pathlib import Path
from html import escape

ROOT = Path(__file__).resolve().parents[1]
SCHEDULE = [
    (0, 5, "今天會做什麼", "What we will do", "先看旅行準備清單的完成樣子。", "Show the finished travel preparation list."),
    (5, 17, "看四個成品", "See four projects", "Travel、N1、Home、TickForge，各約三分鐘。", "Travel, N1, Home, and TickForge: about three minutes each."),
    (17, 25, "Gmail：找信中重點", "Gmail: find the important details", "指定教學郵件，整理時間、待辦、來源與回覆草稿。", "Use specified teaching emails to extract dates, tasks, sources, and a reply draft."),
    (25, 33, "Drive：讀文件做比較", "Drive: read and compare files", "讀兩份指定教學行程文件，標出時間差異與缺漏。", "Read two specified teaching itineraries; identify time differences and missing information."),
    (33, 42, "Notion：找筆記、整理計畫", "Notion: find notes and organize a plan", "查教學筆記，先整理草稿；核對後再示範建立頁面。", "Find teaching notes and prepare a draft; demonstrate creating a page after checking it."),
    (42, 57, "一起做旅行準備清單", "Make a travel preparation list", "複製資料到 AI → 補一個要求 → 回來源核對 → 保存。", "Copy data into AI, add one requirement, check the sources, and save."),
    (57, 60, "帶走與下一步", "Take it away and continue", "重新開啟保存的清單，選一個自己的生活題目。", "Reopen the saved list and choose an everyday topic of your own."),
]

COPY = {
    "zh-Hant": {
        "brand": "AI 生活實驗室", "home": "回小講座", "next": "課後繼續做", "guide": "講師備課", "nav": "主要導覽",
        "guide_title": "這一場，照這個順序帶", "guide_intro": "先展示四個成品，再帶大家做一份簡單的旅行準備清單。60 分鐘，使用電腦。",
        "prep_title": "課前準備", "prep": [
            "開好小講座網站與要使用的 AI 工具。實際連接器只用已確認權限的教學帳號。",
            "四個正式服務由講師自行開啟；投影前確認畫面適合公開。網站的互動示意全部使用虛構資料，可作備案。",
            "準備 Gmail 教學郵件、Drive 教學文件、Notion 教學筆記。先確認能讀到內容，再彩排一次提問與來源核對。",
            "學員不必當場串接私人帳號；直接用首頁提供的相同文字資料。尚未確認學員帳號與工具可用性，需課前完成。",
        ],
        "schedule_title": "60 分鐘流程", "schedule_headers": ["時間", "帶什麼", "當段成果"],
        "show_title": "每個成品，只帶一個用途", "show_headers": ["成品", "現場操作", "接回今天的練習"],
        "show_rows": [
            ["Travel", "選一段旅行，點地點看行程與回憶。", "先把旅行資訊整理成一份清單，再考慮做成地圖。"],
            ["Japanese N1", "做一題、看解析，說明如何回到複習。", "自己的學習需求也能變成教材與小工具。"],
            ["Home", "看感測器與空調狀態，說明設備管理用途。", "資料、固定規則、自動化與 AI 各有分工；主課不操作真實設備。"],
            ["TickForge", "展示資料觀察與比較流程。", "先確認來源、日期、股／口與合約，再解釋差異；主課不進行交易。"],
        ],
        "practice_title": "實作時，跟著學員走四步", "practice": [
            "在教材頁複製練習資料與第一個問題，切到 AI 工具貼上並送出。讓大家看見正在使用哪個視窗。",
            "讀 AI 的草稿，請學員自己補一個要求，例如按期限排序，或把不確定資訊另外列出。",
            "回到三份來源核對時間與待辦。訂房資料未提供入住時間，不能由 AI 猜一個時間當成已確認。",
            "回教材頁貼入核對後的清單，下載或複製保存，再打開檔案確認。沒有 AI 的學員可看固定示例做判斷，實際提問留待課後。",
        ],
        "check_title": "離開前，只確認這三件事", "checks": ["能說出自己今天整理了什麼。", "能指出一項資訊的來源，以及一項仍需確認的事。", "能重新開啟自己的保存紀錄。"],
        "fallback_title": "現場卡住時", "fallback": "正式服務打不開，就用首頁的虛構互動示意。連接器不能用，就貼上同一份教學文字。AI 工具不能用，就先判讀固定示例並記下尚未完成的提問。寄信與更新 Notion 是另外的動作，核對內容與目的地後才示範執行。",
        "sources_title": "內容與來源", "sources": "四個成品的功能概念依專案文件查證；公開教材重新編寫虛構資料。網站不提供私人服務連結、不呼叫 AI、不連接信箱、文件、設備或券商。實際連接器功能以現場帳號與權限為準。",
        "source_link": "連接器官方說明", "legacy": "其他教案（另選，不併入本場）", "legacy_guide": "舊版手機／網頁教案與繁中 PDF", "analysis": "生活資料分析：兩堂延伸課", "web": "做自己的生活清單網頁",
        "next_title": "回家後，從同一個方法繼續", "next_intro": "先找回今天的清單，再換一份自己的資料。一次加一個要求就好。",
        "stages": [
            ("1　找回今天的成果", "打開今天保存的文字檔，確認有問題、來源、結果與待確認事項。還沒保存，就回首頁完成最後一步。", "index.html#takeaway", "回保存成果"),
            ("2　換成自己的生活題目", "旅行行李、活動準備或讀書計畫都可以。先準備一小份適合提供的資料，寫清楚要整理成什麼。", "index.html#classroom", "重做一次簡單練習"),
            ("3　試一個連接器", "選 Gmail 的一封教學信、Drive 的一份文件，或 Notion 的一頁筆記。在自己的 AI 工具確認帳號與讀取範圍，請它說明實際讀到什麼；不能使用時就貼上文字。", "index.html#principles", "看三種接資料的用法"),
        ],
        "reuse_title": "下次可以這樣問", "reuse_prompt": "請只根據我指定的資料，整理一份【我想完成的成果】。\n每項重要資訊附上來源，缺資料請標待確認。先提供草稿，不寄信、不修改原資料。\n\n我的下一個要求：請把【想調整的部分】改成【我希望的方式】。",
        "log_label": "下載空白練習紀錄", "log_note": "這是可另存的文字範本。填寫後用自己的編輯器保存，不會替你自動保存。",
        "optional_title": "想多做一點，再選一個", "optional_intro": "下面是獨立延伸，不需要全部學完。", "advanced": "網頁作品的保存、修改與復原", "closing": "先做一件用得上的事，再慢慢加功能。",
    },
    "en": {
        "brand": "AI Life Lab", "home": "Back to the talk", "next": "Continue after class", "guide": "Instructor guide", "nav": "Main navigation",
        "guide_title": "A simple order for this session", "guide_intro": "Show four projects, then help everyone make a simple travel preparation list. A 60-minute session using computers.",
        "prep_title": "Before the session", "prep": [
            "Open the teaching website and your chosen AI tool. Use a teaching account with verified permissions for connector demonstrations.",
            "Open the four real services yourself and check that their screens are suitable for projection. The fictional interactive examples on this site provide a fallback.",
            "Prepare teaching emails in Gmail, files in Drive, and notes in Notion. Confirm their contents are readable, then rehearse a request and a source check.",
            "Learners do not need to connect private accounts in class; use the same text supplied on the homepage. Learner account and tool availability still needs a pre-class check.",
        ],
        "schedule_title": "The 60-minute plan", "schedule_headers": ["Minutes", "What to show", "Outcome"],
        "show_title": "One useful idea per project", "show_headers": ["Project", "What to demonstrate", "Link to today's exercise"],
        "show_rows": [
            ["Travel", "Choose a trip and open a place to see its itinerary and memories.", "Organize travel details into a list before considering a map."],
            ["Japanese N1", "Answer one question, read the explanation, and show the review path.", "A personal learning need can become reusable material or a small tool."],
            ["Home", "Show sensor and air-conditioning status and explain device management.", "Data, fixed rules, automation, and AI have different roles. Do not operate real devices in the core lesson."],
            ["TickForge", "Show the process of observing and comparing data.", "Check sources, dates, shares/contracts, and contract identity before explaining a change. No trading in the core lesson."],
        ],
        "practice_title": "Walk through the same four steps as learners", "practice": [
            "Copy the practice data and initial question on the teaching page. Switch to the AI tool, paste, and send. Make it clear which window you are using.",
            "Read the AI draft. Ask learners to add one requirement themselves, such as ordering by deadline or listing uncertainties separately.",
            "Check dates and tasks against the three sources. The booking information does not give a check-in time; an AI guess cannot count as confirmed information.",
            "Return to the teaching page, paste the checked list, copy or download it, then reopen the saved file. Learners without AI can examine the fixed example and do the actual AI request later.",
        ],
        "check_title": "Three things to check before leaving", "checks": ["Explain what you organized today.", "Point to a source for one detail and one item that still needs confirmation.", "Reopen your saved record."],
        "fallback_title": "If something does not work", "fallback": "If a real service will not open, use the fictional interactive example. If a connector is unavailable, paste the same teaching text. Without an AI tool, examine the fixed example and record that the request is still to do. Sending email and updating Notion are separate actions: check the content and destination before demonstrating them.",
        "sources_title": "Content and sources", "sources": "Project concepts were checked against their documentation; public exercises use newly authored fictional data. This website contains no private service links and calls no AI, email, document, device, or brokerage service. Actual connector capabilities depend on the account and permissions available in class.",
        "source_link": "Official connector guide", "legacy": "Other lesson plans (separate sessions)", "legacy_guide": "Earlier phone/webpage guide and Traditional Chinese PDFs", "analysis": "Everyday data analysis: two extension lessons", "web": "Build your own checklist webpage",
        "next_title": "Continue with the same method at home", "next_intro": "Reopen today's list, then try one dataset of your own. Add one requirement at a time.",
        "stages": [
            ("1　Find today's result", "Open your saved text file. Check that it includes your question, sources, result, and unknowns. If you have not saved it yet, finish the last step on the homepage.", "index.html#takeaway", "Return to saving your result"),
            ("2　Choose an everyday topic of your own", "Try packing, event preparation, or a study plan. Prepare a small piece of suitable source material and say what you want it organized into.", "index.html#classroom", "Repeat the simple exercise"),
            ("3　Try one connector", "Choose one teaching email in Gmail, one Drive file, or one Notion page. Confirm the account and reading scope in your AI tool, and ask it to describe what it actually read. Paste text if the connector is unavailable.", "index.html#principles", "See three ways to bring in data"),
        ],
        "reuse_title": "A request to reuse next time", "reuse_prompt": "Using only the material I specify, prepare [the result I want].\nInclude sources for important details and mark missing information as to confirm. Provide a draft first; do not send email or change source data.\n\nMy next requirement: change [the part to adjust] to [what I would like].",
        "log_label": "Download a blank practice record", "log_note": "This is a text template you can save separately. Edit and save it in your own editor; it does not save itself.",
        "optional_title": "Choose one extension when you want more", "optional_intro": "These are separate options. You do not need to complete all of them.", "advanced": "Save, revise, and restore a webpage project", "closing": "Make one useful thing first, then add features gradually.",
    },
}

def p(value):
    return '<p>' + escape(value) + '</p>'

def items(values, ordered=False):
    tag = 'ol' if ordered else 'ul'
    return '<' + tag + '>' + ''.join('<li>' + escape(x) + '</li>' for x in values) + '</' + tag + '>'

def table(headers, rows):
    return '<div class="table-scroll"><table><thead><tr>' + ''.join('<th scope="col">' + escape(x) + '</th>' for x in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join('<td>' + escape(str(x)) + '</td>' for x in row) + '</tr>' for row in rows) + '</tbody></table></div>'

def shell(lang, filename, title, intro, content):
    c = COPY[lang]
    english = lang == 'en'
    prefix = '../' if english else ''
    zh = '../' + filename if english else filename
    en = filename if english else 'en/' + filename
    current_zh = '' if english else ' aria-current="page"'
    current_en = ' aria-current="page"' if english else ''
    return f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{escape(intro, quote=True)}"><title>{escape(title)} | {c['brand']}</title><link rel="stylesheet" href="{prefix}styles.css?v=5"><link rel="stylesheet" href="{prefix}seminar.css?v=1"><script src="{prefix}language.js?v=4" defer></script></head>
<body class="seminar-page"><a class="skip" href="#main">{'Skip to main content' if english else '跳到主要內容'}</a>
<header class="site-header"><a class="brand" href="index.html">{c['brand']}</a><nav aria-label="{c['nav']}"><a href="index.html">{c['home']}</a><a href="next-steps.html">{c['next']}</a><a href="instructor.html">{c['guide']}</a></nav><div class="language-switch" role="group" aria-label="Language"><a href="{zh}" data-language-switch="zh-Hant" lang="zh-Hant"{current_zh}>繁體中文</a><a href="{en}" data-language-switch="en" lang="en"{current_en}>English</a></div></header>
<main id="main" class="seminar-main"><section class="section wrap"><p class="eyebrow">{c['brand']}</p><h1>{escape(title)}</h1><p class="lead">{escape(intro)}</p></section>{content}</main><footer class="site-footer wrap"><p>{c['closing']}</p><a href="index.html">{c['home']}</a></footer></body></html>
'''

def section(identifier, title, content):
    return '<section id="' + identifier + '" class="section wrap"><h2>' + escape(title) + '</h2>' + content + '</section>'

def render_guide(lang):
    c = COPY[lang]
    en = lang == 'en'
    schedule = [(f'{start}–{end}', row_en if en else row_zh, result_en if en else result_zh) for start, end, row_zh, row_en, result_zh, result_en in SCHEDULE]
    content = section('prepare', c['prep_title'], items(c['prep']))
    content += section('schedule', c['schedule_title'], table(c['schedule_headers'], schedule))
    content += section('showcase-guide', c['show_title'], table(c['show_headers'], c['show_rows']))
    content += section('practice-guide', c['practice_title'], items(c['practice'], True))
    content += section('before-leaving', c['check_title'], items(c['checks']))
    content += section('fallback', c['fallback_title'], p(c['fallback']))
    content += section('sources', c['sources_title'], p(c['sources']) + '<a href="https://learn.chatgpt.com/docs/plugins" target="_blank" rel="noopener">' + c['source_link'] + ' ↗</a>')
    content += section('other-lessons', c['legacy'], '<ul><li><a href="workshop-instructor.html">' + c['legacy_guide'] + '</a></li><li><a href="analysis.html#lessons">' + c['analysis'] + '</a></li></ul>')
    return shell(lang, 'instructor.html', c['guide_title'], c['guide_intro'], content)

def render_next(lang):
    c = COPY[lang]
    content = ''
    for i, (title, intro, url, link) in enumerate(c['stages'], 1):
        content += section('step-' + str(i), title, p(intro) + '<a class="text-link" href="' + url + '">' + link + ' →</a>')
    log_file = ('../' if lang == 'en' else '') + 'downloads/seminar-learning-log' + ('-en' if lang == 'en' else '') + '.txt'
    content += section('reuse', c['reuse_title'], '<pre style="white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;background:#f6f7f9;padding:16px">' + escape(c['reuse_prompt']) + '</pre><p><a class="button outline" href="' + log_file + '" download>' + c['log_label'] + '</a></p>' + p(c['log_note']))
    content += section('optional', c['optional_title'], p(c['optional_intro']) + '<ul><li><a href="analysis.html">' + c['analysis'] + '</a></li><li><a href="practice.html?route=computer#classroom">' + c['web'] + '</a></li><li><a href="web-project.html">' + c['advanced'] + '</a></li></ul>')
    return shell(lang, 'next-steps.html', c['next_title'], c['next_intro'], content)

def build():
    for lang in COPY:
        directory = ROOT / 'en' if lang == 'en' else ROOT
        (directory / 'instructor.html').write_text(render_guide(lang), encoding='utf-8', newline='\n')
        (directory / 'next-steps.html').write_text(render_next(lang), encoding='utf-8', newline='\n')
    logs = {
        'seminar-learning-log.txt': '我的生活應用練習\n\n我想完成什麼：\n來源與讀取範圍：\n我先問了什麼：\n我補充的一個要求：\n核對後的結果：\n回查過的來源：\n仍需確認：\n保存位置：\n下次想試什麼：\n',
        'seminar-learning-log-en.txt': 'My everyday AI practice\n\nWhat I want to complete:\nSources and reading scope:\nMy initial request:\nOne requirement I added:\nMy checked result:\nSources I reopened:\nStill to confirm:\nWhere I saved it:\nWhat I want to try next:\n',
    }
    for filename, content in logs.items():
        (ROOT / 'downloads' / filename).write_text(content, encoding='utf-8', newline='\n')

if __name__ == '__main__':
    build()
