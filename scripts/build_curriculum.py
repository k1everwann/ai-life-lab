"""Render the task-based bilingual course pool, using public fictional inputs."""
from pathlib import Path
from html import escape as esc
import json
import csv
import io
import hashlib

ROOT = Path(__file__).resolve().parents[1]
UI = {
    'zh-Hant': {
        'title': 'AI 生活應用', 'lead': '先看能做什麼，再選一件事親手完成。已經會的部分，直接試題或挑戰。',
        'meta': '電腦操作 · 12 個可自由選擇的單元 · 繁體中文／English',
        'nav': ['看成品', '選課程', '保存與繼續'], 'start': '從第一次操作開始', 'map': '選一個現在想做的任務',
        'mapnote': '不必上完全部。每課先試一題；已會就直接做挑戰，需要協助就展開步驟。時間是完整單元的估計，可分次完成。',
        'groups': ['開始操作與核對', '用自己的資料', '製作工具與流程', '表達與自選專題'],
        'minutes': '分鐘', 'needs': '先備能力', 'none': '無；從操作開始', 'proof': '已會這項能力可直接開始，不必重上前課。',
        'quick': '先試這題', 'skip': '什麼情況可以跳過說明？', 'jump': '直接做挑戰', 'guide': '跟著做：資料與步驟',
        'fiction': '本課資料皆為新編虛構資料。本站不呼叫 AI，也不連接你的帳號；請把練習貼到自己的 AI 工具。',
        'source': '教學資料', 'prompt': '第一個要求', 'copy': '複製資料與要求', 'expected': '對照參考結果',
        'fixed': '以下是事先準備的參考結果。先做一次，再逐項核對自己的回答。',
        'independent': '自己做：換一個情境', 'challenge': '加深挑戰', 'copytask': '複製這個任務',
        'quiz': '再確認一個關鍵觀念', 'answer': '檢查答案與理由', 'checks': '完成時，能展示這些成果',
        'self': '勾選只是本頁的自我紀錄，沒有自動判定你已學會；關閉後不保留，請下載紀錄。', 'other_checks': ['能展示自己完成的成果，並逐項對照這個練習的參考結果。', '保留實際來源、自己的操作與至少一項核對證據。'],
        'record': '留下自己的操作與核對', 'mode': '我實際做到哪一步', 'exercise': '這份紀錄對應哪個練習', 'exercise_types': ['主練習', '獨立練習', '加深挑戰'],
        'jumpown': '直接自己做', 'followup': '第二輪：只更新一處', 'aitool': '開啟 ChatGPT（新分頁）', 'aitoolnote': '也可使用講師指定、你已能登入的 AI 工具；保留教材分頁，方便回來核對。',
        'modes': ['尚未操作', '看示範／紙上判讀', '已在自己的 AI 工具操作', '已實際連接指定教學來源'],
        'question': '我實際送出的要求／修改', 'result': '我的結果與核對方式', 'placeholder': '寫下或貼上自己的成果、改了什麼、如何核對，以及仍待補的部分。',
        'download': '下載這課操作紀錄', 'material': '下載這課教材（含參考答案）',
        'previous': '上一課', 'next': '下一課', 'back': '返回課程地圖', 'current': '目前單元',
        'save': '保存後，下次接著做', 'savenote': '文字與程式碼不會自動保存或上傳。先下載自己的紀錄；下次開啟文字檔，把成果貼回對應單元再繼續。切語言前也請先保存。',
        'saveall': '下載所有已填紀錄', 'extensions': '延伸資料與舊教材',
        'extensionnote': '需要更多資料時再使用；主要的 12 課都在同一頁。舊教材的時間安排不代表這次課程。',
        'setup': 'Gmail／Drive／Notion：連接前先知道',
        'setuptext': '本課使用虛構資料，不需要連接私人帳號。若你的 ChatGPT 提供 Plugins（外掛），可搜尋 Gmail、Google Drive 或 Notion，依提示連接帳號，先核對帳號與要求的權限，安裝後開啟新聊天。功能會依方案、平台、地區、推出進度與工作區設定而異。看不到外掛時，使用本課文字繼續練習；這只完成資料整理，實際連接另記待補。',
        'official': '官方設定說明', 'plans': '講座可以怎麼選課', 'plantext': '以下是核心練習的組合，不代表在短時間完成所有整課。帳號登入與工具準備請在課前完成。',
        'plansrows': [
            ['60 分鐘', '看成品 8 → 先試 5 → M01 核心 15 → M02 核心 15 → M03 核心 12 → 保存 5'],
            ['90 分鐘', '看成品 8 → 準備／先試 7 → M02／M03 核心 20 → Gmail／Drive／Notion 擇一 35 → 自己練 15 → 保存 5'],
            ['120 分鐘', '看成品 8 → 準備／先試 7 → M03 核心 20 → M08 首版 35 → M09 修改／測試 25 → M12 選題／起步 20 → 保存 5']],
        'glossary': '遇到不熟悉的詞', 'terms': [('提示詞／要求', '你交給 AI 的問題、資料與希望得到的結果。'), ('來源', '答案所依據的原始信件、文件、筆記或資料列。'), ('外掛／連接器', '讓 AI 在你允許的範圍讀取或操作其他服務的功能。'), ('HTML', '瀏覽器可以開啟的網頁檔案；副檔名是 .html。'), ('預覽／部署', '預覽是先測試；部署是放到網站供人使用。下載檔案不會自動公開。')],
        'code': '程式碼工作區', 'codetext': 'HTML 是可由瀏覽器開啟的網頁程式碼。把 AI 產生的完整程式碼貼在這裡，再按預覽試用。這裡不會發布網站；請只使用本課虛構資料。',
        'codeinput': '完整 HTML 程式碼', 'preview': '更新隔離預覽', 'codedownload': '下載這份 HTML', 'emptycode': '請先貼上完整 HTML。',
        'previewready': '預覽已更新。請實際操作，再比對預期結果；預覽不保留輸入或勾選。',
        'downloadready': '已開始下載。到瀏覽器下載清單開啟 HTML，確認檔案與功能；這不代表已公開上線。',
        'codeframe': '隔離的 HTML 練習預覽', 'broken': '下載故障版清單', 'correct': '下載參考修正版',
        'filehelp': '檔案練習：先下載故障版，用瀏覽器打開測試；要看程式碼，用文字編輯器開啟同一檔案。保留原檔，修改另存新檔。',
        'lab7': '門檻小實驗（固定程式計算，沒有呼叫 AI）', 'strict': '增加超過 50 元', 'inclusive': '增加至少 50 元',
        'lab10': '規則小實驗（僅模擬提醒，不控制設備）', 'sensor': '測試一筆讀值', 'temps': ['27°C', '28°C', '29°C', '缺少讀值'],
        'simulate': '測試新事件', 'repeat': '重播同一事件', 'reset': '重設模擬',
        'copied': '已複製。切到自己的 AI 工具，貼上並送出，再回來核對。', 'manual': '無法自動複製；請選取下面文字，按 Ctrl+C（Mac 用 Command+C）。',
        'choose': '請先選一個答案。', 'right': '答對了。', 'retry': '再看一次來源。', 'emptyrecord': '先填入自己的要求或結果，再下載。', 'copyreturn': '返回剛才的練習',
        'recordsaved': '已開始下載文字紀錄，請到下載清單開啟確認。', 'noscript': '互動需要 JavaScript。所有課程、資料和參考答案仍可閱讀，文字可手動複製。',
    },
    'en': {
        'title': 'Everyday AI', 'lead': 'See what is possible, then complete one useful task yourself. Try the task or challenge to skip what you already know.',
        'meta': 'On a computer · 12 flexible modules · 繁體中文 / English',
        'nav': ['See projects', 'Choose a module', 'Save and continue'], 'start': 'Start with your first AI task', 'map': 'Choose a task you want to do',
        'mapnote': 'You do not need every module. Try the entry task first. Move to the challenge if you can do it, or open the steps for help. Times estimate a full module; you can finish over several sessions.',
        'groups': ['Start and verify', 'Work with your data', 'Build tools and workflows', 'Communicate and create'],
        'minutes': 'min', 'needs': 'Skills to bring', 'none': 'None; start with basic operation', 'proof': 'If you can demonstrate the skill, start here without repeating an earlier module.',
        'quick': 'Try this first', 'skip': 'When can I skip the instructions?', 'jump': 'Go straight to the challenge', 'guide': 'Follow along: data and steps',
        'fiction': 'All lesson data is fictional. This site does not call AI or connect your accounts. Paste the exercise into your own AI tool.',
        'source': 'Teaching data', 'prompt': 'Your first request', 'copy': 'Copy data and request', 'expected': 'Compare the reference result',
        'fixed': 'This is a prepared reference result. Try the task first, then check your own response against it.',
        'independent': 'Do it yourself: a new situation', 'challenge': 'Take the challenge', 'copytask': 'Copy this task',
        'quiz': 'Check one key idea', 'answer': 'Check answer and reason', 'checks': 'Show these results when you finish',
        'self': 'Ticks are a self-reported record for this page, not automatic assessment. They reset when the page closes; download your record.', 'other_checks': ['Show my own completed work and compare each part with this exercise’s reference result.', 'Retain the actual source, my operations, and at least one check as evidence.'],
        'record': 'Keep your own work and checks', 'mode': 'What I actually did', 'exercise': 'Which exercise does this record describe?', 'exercise_types': ['Guided task', 'Independent task', 'Challenge'],
        'jumpown': 'Do it independently', 'followup': 'Round two: change one thing', 'aitool': 'Open ChatGPT (new tab)', 'aitoolnote': 'You can also use the AI tool specified by your instructor that you can sign in to. Keep the lesson tab open so you can return to check.',
        'modes': ['Not attempted yet', 'Watched / reasoned on paper', 'Used my own AI tool', 'Connected the specified teaching source'],
        'question': 'The request / change I actually sent', 'result': 'My result and how I checked it', 'placeholder': 'Keep your result, what you changed, how you checked it, and anything still to do.',
        'download': 'Download my record for this module', 'material': 'Download this lesson (with reference answers)',
        'previous': 'Previous module', 'next': 'Next module', 'back': 'Back to the course map', 'current': 'Current module',
        'save': 'Save now and continue next time', 'savenote': 'Text and code are not saved automatically or uploaded. Download your record first. Next time, open the text file and paste your work back into the module. Save before changing language too.',
        'saveall': 'Download all records I have filled in', 'extensions': 'More data and earlier material',
        'extensionnote': 'Use these when you need more practice. All 12 main modules are on this page. Earlier schedules do not describe this course.',
        'setup': 'Before connecting Gmail / Drive / Notion',
        'setuptext': 'This course uses fictional data; no personal account connection is required. If Plugins is available in your ChatGPT, search for Gmail, Google Drive, or Notion, connect when prompted, and check the account and requested permissions first. Start a new chat after installation. Features vary by plan, platform, region, rollout, and workspace settings. If you cannot see the plugin, continue with the lesson text. This practises data work; record the actual connection as still to do.',
        'official': 'Official setup guide', 'plans': 'Choose a talk format', 'plantext': 'These combine core exercises, not entire modules compressed into a short session. Sign in and prepare tools before class.',
        'plansrows': [
            ['60 min', 'Projects 8 → entry task 5 → M01 core 15 → M02 core 15 → M03 core 12 → save 5'],
            ['90 min', 'Projects 8 → preparation / entry task 7 → M02 / M03 core 20 → choose Gmail, Drive OR Notion 35 → own task 15 → save 5'],
            ['120 min', 'Projects 8 → preparation / entry task 7 → M03 core 20 → M08 first version 35 → M09 change / test 25 → M12 project starter 20 → save 5']],
        'glossary': 'Look up an unfamiliar word', 'terms': [('Prompt / request', 'The question, material, and desired result you give AI.'), ('Source', 'The original email, document, note, or data row supporting an answer.'), ('Plugin / connector', 'A feature that lets AI read or act in another service within your permissions.'), ('HTML', 'A webpage file a browser can open, with a .html extension.'), ('Preview / deploy', 'Preview to test; deploy to make a website available. Downloading a file does not publish it.')],
        'code': 'Code workspace', 'codetext': 'HTML is the code a browser opens as a webpage. Paste the complete code from your AI, then preview and test it here. This does not publish a website. Use only the fictional lesson material.',
        'codeinput': 'Complete HTML code', 'preview': 'Update isolated preview', 'codedownload': 'Download this HTML', 'emptycode': 'Paste complete HTML first.',
        'previewready': 'Preview updated. Try the controls and compare with your expected result. Updating the preview resets its inputs and ticks.',
        'downloadready': 'Download started. Open the HTML from your browser downloads and check the file and behavior. It has not been published.',
        'codeframe': 'Isolated HTML practice preview', 'broken': 'Download the broken checklist', 'correct': 'Download the reference fix',
        'filehelp': 'Download the broken file and open it in a browser to test. Open the same file in a text editor to read the code. Keep the original and save changes as a new file.',
        'lab7': 'Threshold experiment (fixed calculations, no AI call)', 'strict': 'Increase greater than TWD 50', 'inclusive': 'Increase of at least TWD 50',
        'lab10': 'Rule experiment (simulated alert; no device control)', 'sensor': 'Test one reading', 'temps': ['27°C', '28°C', '29°C', 'Missing reading'],
        'simulate': 'Test a new event', 'repeat': 'Replay the same event', 'reset': 'Reset simulation',
        'copied': 'Copied. Paste and send it in your own AI tool, then come back to check.', 'manual': 'Automatic copy is unavailable. Select the text below and press Ctrl+C (Command+C on Mac).',
        'choose': 'Choose an answer first.', 'right': 'Correct.', 'retry': 'Check the source again.', 'emptyrecord': 'Enter your own request or result before downloading.', 'copyreturn': 'Return to the exercise',
        'recordsaved': 'Text download started. Open it from your downloads to check.', 'noscript': 'Interaction needs JavaScript. You can still read every lesson, source, and reference answer and copy text manually.',
    }
}

def p(text, cls=''):
    return f'<p class="{cls}">{esc(text)}</p>'

def pre(text):
    return '<pre class="lesson-text">' + esc(text) + '</pre>'

def listing(items, tag='ul'):
    return f'<{tag}>' + ''.join('<li>' + esc(x) + '</li>' for x in items) + f'</{tag}>'

def button(label, attrs):
    return '<button type="button" class="button outline" ' + attrs + '>' + esc(label) + '</button>'

def workspace(module, lang, prefix, t):
    key = module['id']
    if key not in ('M08', 'M09'):
        return ''
    out = '<section id="workspace-'+key+'" class="code-workspace"><h3>' + t['code'] + '</h3>' + p(t['codetext'])
    out += '<label for="code-' + key + '">' + t['codeinput'] + '</label><textarea id="code-' + key + '" data-code rows="10" spellcheck="false" maxlength="150000"></textarea><div class="actions">'
    out += button(t['preview'], f'data-preview="{key}"') + button(t['codedownload'], f'data-code-download="{key}"')
    out += '</div><p role="status" id="code-status-' + key + '"></p><iframe hidden id="preview-' + key + '" title="' + t['codeframe'] + '" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe></section>'
    return out

def lesson_text(module, lang):
    from learning_layout import LABELS
    t=UI[lang]; l=LABELS[lang]; c=module['locales'][lang]
    lines=[c['title'],c['why'],l['outcome'],c['goal'],l['sample'],c['outcome'],l['samplehint'],l['follow'],l['where'],l['source'],c['source'],l['prompt'],c['prompt'],'\n'.join(f'{i}. {step}' for i,step in enumerate(c['steps'],1)),l['reference'],c['expected'],l['check'],'\n'.join(c['checks'])]
    if c.get('followup'):
        f=c['followup'];lines.extend([l['change'],f['source'],f['prompt'],f['expected']])
    lines.extend([l['own'],c['independent']['task'],c['independent']['expected'],l['challenge'],c['challenge']['task'],c['challenge']['source'],c['challenge']['prompt'],c['challenge']['expected']])
    if c.get('connection'):
        f=c['connection'];lines.extend([f['title'],f['source'],f['prompt'],'\n'.join(f['steps']),f['expected']])
    lines.extend([l['finish'],l['finishnote']])
    return '\n\n'.join(lines)+'\n'

def render(lang, demo=None, oldcourse=None, showcase=None, oldcopy=None):
    from learning_layout import render as render_lessons
    return render_lessons(lang)

def write_materials():
    data=json.loads((ROOT/'curriculum-content.json').read_text(encoding='utf-8'))
    directory=ROOT/'downloads'/'curriculum'; directory.mkdir(exist_ok=True)
    for lang in UI:
        for module in data['modules']:
            (directory/f'{module["id"].lower()}-{lang}.txt').write_text(lesson_text(module,lang),encoding='utf-8',newline='\n')
        for broken in (True,False):
            name=('broken' if broken else 'correct')+f'-checklist-{lang}.html'
            (directory/name).write_text(checklist_fixture(lang,broken),encoding='utf-8',newline='\n')
            resetname=('reset-bug' if broken else 'correct-reset')+f'-{lang}.html'
            (directory/resetname).write_text(reset_fixture(lang,broken),encoding='utf-8',newline='\n')
            searchname=('search-reset-bug' if broken else 'correct-search-reset')+f'-{lang}.html'
            (directory/searchname).write_text(search_fixture(lang,broken),encoding='utf-8',newline='\n')
    analysis=next((m for m in data['modules'] if m['id']=='M07'),None)
    if analysis:
        rows=list(csv.reader(analysis['locales']['en']['source'].splitlines()[1:]))
        stream=io.StringIO(newline='');writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(['row_id','month','category','amount_twd']);writer.writerows(rows[1:])
        (directory/'monthly-spending.csv').write_text(stream.getvalue(),encoding='utf-8',newline='\n')

def checklist_fixture(lang, broken):
    en=lang=='en'
    title=('Checklist: debugging exercise' if en else '清單：除錯練習')
    tasks=['Download tickets','Confirm meeting location','Bring a water bottle'] if en else ['下載車票','確認集合地點','帶水壺']
    note=('Fictional teaching file. Ticks reset on refresh. '+('Intentionally broken: find the counting error.' if broken else 'Reference fix: every checked task is counted.')) if en else ('虛構教學檔案；重新整理不保留勾選。'+('此版本刻意保留計數錯誤，請重現並修正。' if broken else '參考修正版：計入所有勾選項目。'))
    script='(()=>{const boxes=[...document.querySelectorAll("input[type=checkbox]")];const count=document.getElementById("count");function update(){count.textContent=boxes'+('.slice(1)' if broken else '')+'.filter(box=>box.checked).length;}boxes.forEach(box=>box.addEventListener("change",update));document.getElementById("reset").addEventListener("click",()=>{boxes.forEach(box=>{box.checked=false;});update();});function init(){boxes.forEach(box=>{box.checked=false;});update();}window.addEventListener("pageshow",init);init();})();'
    return f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; script-src \'unsafe-inline\'; connect-src \'none\'; form-action \'none\'; base-uri \'none\'"><title>{title}</title><style>body{{font:16px/1.7 system-ui,sans-serif;max-width:700px;margin:auto;padding:24px;color:#202124}}h1{{font-size:26px}}label{{display:flex;gap:12px;align-items:center;padding:12px 0}}input{{width:22px;height:22px}}button{{font:inherit;padding:10px 16px;background:white;border:1px solid #2458a6;min-height:44px}}:focus-visible{{outline:2px solid #2458a6;outline-offset:3px}}</style></head><body><h1>{title}</h1><p>{note}</p><p role="status" aria-live="polite">'+('Completed' if en else '已完成')+' <strong id="count">0</strong> / 3</p>'+''.join('<label><input type="checkbox"><span>'+esc(task)+'</span></label>' for task in tasks)+'<button type="button" id="reset">'+('Reset all' if en else '全部重設')+'</button><script>'+script+'</script></body></html>\n'

def reset_fixture(lang,broken):
    html=checklist_fixture(lang,False)
    html=html.replace('Confirm meeting location','Write three questions').replace('確認集合地點','寫三個問題')
    html=html.replace('Download tickets','Choose an article').replace('下載車票','選一篇文章')
    import re
    html=re.sub(r'<label><input type="checkbox"><span>(Bring a water bottle|帶水壺)</span></label>','',html)
    html=html.replace('/ 3','/ 2').replace('function update()','function updateCount()').replace(',update)',',updateCount)').replace('update();','updateCount();')
    if broken:html=html.replace('box.checked=false;});updateCount();','box.checked=false;});')
    old='Reference fix: every checked task is counted.' if lang=='en' else '參考修正版：計入所有勾選項目。'
    new=('Intentionally broken reset: check both, then reset. The count is stale.' if broken else 'Reference reset fix: clear the checks and update the count.') if lang=='en' else ('刻意保留重設錯誤：勾兩項再重設，計數沒有更新。' if broken else '重設參考修正版：清除勾選後也更新計數。')
    return html.replace(old,new)

def search_fixture(lang,broken):
    html=checklist_fixture(lang,False)
    label='Search tasks' if lang=='en' else '搜尋項目'
    control=f'<label for="search">{label}</label><input id="search" type="search" autocomplete="off">'
    html=html.replace('<p role="status"',control+'<p role="status"',1)
    script='(()=>{const boxes=[...document.querySelectorAll("input[type=checkbox]")];const count=document.getElementById("count");const search=document.getElementById("search");function update(){count.textContent=boxes.filter(b=>b.checked).length;}function filter(){boxes.forEach(b=>{b.parentElement.hidden=!b.parentElement.textContent.toLowerCase().includes(search.value.toLowerCase());});}boxes.forEach(b=>b.addEventListener("change",update));search.addEventListener("input",filter);document.getElementById("reset").addEventListener("click",()=>{boxes'+('.filter(b=>!b.parentElement.hidden)' if broken else '')+'.forEach(b=>{b.checked=false;});search.value="";filter();update();});function init(){boxes.forEach(b=>{b.checked=false;});search.value="";filter();update();}window.addEventListener("pageshow",init);init();})();'
    import re
    html=re.sub(r'<script>.*?</script>','<script>'+script+'</script>',html,flags=re.S)
    html=html.replace('label{display:flex;','[hidden]{display:none!important}label{display:flex;')
    old='Reference fix: every checked task is counted.' if lang=='en' else '參考修正版：計入所有勾選項目。'
    new=('Intentionally broken: reset clears visible tasks only.' if broken else 'Reference fix: reset clears all tasks, including hidden ones.') if lang=='en' else ('刻意保留錯誤：重設只清可見項目。' if broken else '參考修正版：重設清除所有項目，包含隱藏項目。')
    return html.replace(old,new)

if __name__=='__main__':
    write_materials()
