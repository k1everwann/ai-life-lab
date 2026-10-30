"""Real public-UI screenshots with bilingual, task-local instructions."""
from html import escape
import hashlib
from pathlib import Path

SHOTS = {
 'start': ('chat-start-zh.jpg',1280,720, '先找到輸入框', 'Find the message box', '這是未登入的 ChatGPT 首頁。中央「問問 ChatGPT」是輸入框；左側「新對話」可開始另一個題目。', 'This is the signed-out ChatGPT home screen. The central “Ask ChatGPT” box accepts your message; “New chat” on the left starts a different topic.'),
 'paste': ('chat-paste-zh.jpg',805,225, '貼上資料，按箭頭送出', 'Paste the material and send', '點輸入框，按 Ctrl+V（Mac：⌘V），再按右下角向上箭頭。請貼本課資料。', 'Click the message box, press Ctrl+V (Mac: ⌘V), then select the upward arrow at the bottom right. Use this lesson’s material.'),
 'answer': ('chat-answer-zh.jpg',635,245, '收到回答，先對照資料', 'Check the answer against the material', '先核對回答。想保存時，可按回答下方的雙方框圖示複製。', 'Check the answer first. To save it, use the overlapping-squares icon below the response to copy it.'),
 'followup': ('chat-followup-zh.jpg',635,320, '在同一段對話提出修改', 'Ask for a change in the same conversation', '在回答下方的輸入框，寫出你要改的地方，再送出。', 'Use the message box below the response to describe your change, then send.'),
 'directory': ('plugins-directory-zh.jpg',900,350, '從外掛程式目錄找服務', 'Find the service in the plugin directory', '左側選「外掛程式」，右上角輸入服務名稱搜尋。先核對服務名稱與開發者；名字包含 Gmail 的其他產品，不等於 Gmail 連接器。找不到時先做貼文字練習。', 'Select “Plugins” on the left and search at the top right. Check the service and developer: a different product with Gmail in its name is not the Gmail connector. If unavailable, use the text exercise first.'),
 'drive': ('drive-entry-zh.jpg',635,205, '確認是 Google Drive，再繼續', 'Check that this is Google Drive', '這是公開的 Google Drive 服務介紹頁。「安裝外掛程式」會引導登入；這張圖還沒有完成連線。登入後依實際畫面核對帳號與存取範圍。', 'This is the public Google Drive listing. “Install plugin” leads to sign-in; this image does not show a completed connection. After signing in, check the account and requested access on your own screen.'),
 'notion': ('notion-entry-zh.jpg',635,245, '確認是 Notion，再繼續', 'Check that this is Notion', '這是公開的 Notion 服務介紹頁。「安裝外掛程式」會引導登入；這張圖還沒有選工作區或授權頁面。後續依實際畫面，只選這次要練習的內容。', 'This is the public Notion listing. “Install plugin” leads to sign-in; no workspace or page access has been selected here. Follow your own screen and choose only the material for this exercise.'),
 'preview': ('html-preview-20261030.jpg',1265,712, '貼程式碼，再按預覽', 'Paste code, then preview', '貼上完整 HTML，按「預覽網頁」，在下方試用。圖中使用本課的預備範例；你的作品可以長得不同。', 'Paste the complete HTML, select “Preview webpage”, and try it below. This image uses the lesson’s prepared example; your design can look different.'),
}

for key,file,h,zh,en in (
 ('gmail-paste','gmail-paste-zh.jpg',280,'先前郵件範例：看貼上與送出位置','Earlier email example: locate paste and send'),
 ('drive-paste','drive-paste-zh.jpg',280,'先前方案範例：看貼上與送出位置','Earlier comparison example: locate paste and send'),
 ('notion-paste','notion-paste-zh.jpg',250,'先前筆記範例：看貼上與送出位置','Earlier notes example: locate paste and send')):
    SHOTS[key]=(file,635,h,zh,en,'在 ChatGPT 新對話的輸入框按 Ctrl+V（Mac：⌘V）。確認資料與要求都貼上後，按右下角的向上箭頭送出；長文字可在框內捲動。','In a new ChatGPT conversation, click the message box and press Ctrl+V (Mac: ⌘V). Check that both the material and request are present, then send with the upward arrow at the bottom right. Scroll inside the box to read long drafts.')

def figure(key,lang,prefix,show_title=True):
    file,w,h,zh,en,zhtext,entext=SHOTS[key]
    title,text=(en,entext) if lang=='en' else (zh,zhtext)
    if key!='preview':text+=(' Image: earlier example, for locating controls.' if lang=='en' else ' 圖中為先前範例，僅示意操作位置。')
    url=prefix+'assets/walkthrough/'+file+'?v='+hashlib.sha256((Path(__file__).resolve().parents[1]/'assets/walkthrough'/file).read_bytes()).hexdigest()[:12]
    zoom='View larger image' if lang=='en' else '查看大圖'
    return '<figure class="walkthrough-shot"><figcaption>'+('<strong>'+escape(title)+'</strong>' if show_title else '')+'<p>'+escape(text)+'</p></figcaption><a class="screenshot-link" href="'+url+'" target="_blank" rel="noopener" data-screenshot aria-label="'+escape(zoom+': '+title,quote=True)+'"><img src="'+url+'" width="'+str(w)+'" height="'+str(h)+'" loading="lazy" alt="'+escape(title+' — '+text,quote=True)+'"><span>'+zoom+' ↗</span></a></figure>'

def note(lang,key=None):
    date='2026-10-30' if key=='preview' else '2026-10-29'
    return '<p class="screenshot-note">'+(('Real screenshot · '+date+' · Traditional Chinese interface; use this lesson’s material. Your screen may differ.') if lang=='en' else ('實際截圖 · '+date+' · 畫面可能不同，題目請用本課資料。'))+'</p>'

def chat_guide(lang,prefix,key):
    en=lang=='en'
    steps=[('start','開啟 ChatGPT，找到輸入框','Open ChatGPT and find the message box'),('paste','貼上資料，送出要求','Paste the material and send'),('answer','核對回答中的日期與資訊','Check dates and facts in the response'),('followup','在同一段對話追問','Ask for a change in the same conversation')]
    panels=''.join('<details class="visual-step" name="visual-'+key+'"'+(' open' if key=='M01' and i==1 else '')+'><summary>'+str(i+1)+'. '+(english if en else chinese)+'</summary>'+figure(shot,lang,prefix,False)+'</details>' for i,(shot,chinese,english) in enumerate(steps))
    if key=='M01':
        return '<div class="visual-guide"><h3>'+('Follow the pictures, one step at a time' if en else '看圖操作，一次看一步')+'</h3>'+panels+note(lang)+'</div>'
    shot={'M04':'gmail-paste','M05':'drive-paste','M06':'notion-paste'}.get(key)
    title='Where do I click? See pictures' if en else '不知道按哪裡？看圖解'
    return '<div class="visual-guide">'+(figure(shot,lang,prefix) if shot else '')+'<details class="common-visuals"><summary>'+title+'</summary>'+panels+note(lang)+'</details>'+(note(lang) if shot else '')+'</div>'


def connection_guide(lang,prefix,key=None):
    keys={'M04':['directory'],'M05':['drive'],'M06':['notion']}.get(key,['directory','drive','notion'])
    return '<div class="visual-guide">'+''.join(figure(k,lang,prefix) for k in keys)+note(lang)+'</div>'

def zoom_dialog(lang):
    close='Close image' if lang=='en' else '關閉大圖'
    hint='Scroll sideways to see details on a small screen.' if lang=='en' else '小螢幕可左右捲動，查看原尺寸細節。'
    return '<dialog id="screenshot-dialog" aria-label="'+('Screenshot' if lang=='en' else '操作截圖')+'"><form method="dialog"><button autofocus>'+close+'</button></form><p>'+hint+'</p><div class="image-pan" tabindex="0" aria-label="'+hint+'"><img id="screenshot-large" alt=""></div><p id="screenshot-caption"></p></dialog>'
