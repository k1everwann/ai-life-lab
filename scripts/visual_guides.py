"""Real public-UI screenshots with bilingual, task-local instructions."""
from html import escape

SHOTS = {
 'start': ('chat-start-zh.jpg',1280,720, '先找到輸入框', 'Find the message box', '這是未登入的 ChatGPT 首頁。中央「問問 ChatGPT」是輸入框；左側「新對話」可開始另一個題目。', 'This is the signed-out ChatGPT home screen. The central “Ask ChatGPT” box accepts your message; “New chat” on the left starts a different topic.'),
 'paste': ('chat-paste-zh.jpg',805,225, '把資料與要求貼在同一個輸入框', 'Paste the material and request in the same box', '按上方「複製資料與要求」，切到 ChatGPT，點輸入框後按 Ctrl+V（Mac：⌘V），再按右下角向上箭頭送出。圖中用第 1 課示範；這一課請貼上上方的資料。', 'Use “Copy material and request” above, switch to ChatGPT, click the message box and press Ctrl+V (Mac: ⌘V). Send with the upward arrow at the bottom right. The image uses Lesson 1; paste this lesson’s material instead.'),
 'answer': ('chat-answer-zh.jpg',635,245, '收到回答，先對照原文', 'Check the response against the original', '這次實際回答把回覆期限列為 11/18 18:00，並保留「集合地點尚未公布」。先核對這些內容，再使用回答；左下雙方框圖示可複製。', 'This actual response preserves the November 18, 18:00 deadline and the unknown meeting location. Check these facts before using the response. The overlapping-squares icon at the bottom left copies it.'),
 'followup': ('chat-followup-zh.jpg',635,320, '要修改，就在同一段對話繼續說', 'Ask for a change in the same conversation', '不用另開對話。在回答下方的輸入框寫你想改的地方，再送出。圖中已輸入「改成一句可以傳給朋友的提醒，語氣親切一點」，尚未送出。', 'Keep the same conversation. Type what you want changed in the box below the response, then send. The unsent draft shown asks: “Make this a friendly, one-sentence reminder I can send to a friend.”'),
 'directory': ('plugins-directory-zh.jpg',900,350, '從外掛程式目錄找服務', 'Find the service in the plugin directory', '左側選「外掛程式」，右上角輸入服務名稱搜尋。先核對服務名稱與開發者；名字包含 Gmail 的其他產品，不等於 Gmail 連接器。找不到時先做貼文字練習。', 'Select “Plugins” on the left and search at the top right. Check the service and developer: a different product with Gmail in its name is not the Gmail connector. If unavailable, use the text exercise first.'),
 'drive': ('drive-entry-zh.jpg',635,205, '確認是 Google Drive，再繼續', 'Check that this is Google Drive', '這是公開的 Google Drive 服務介紹頁。「安裝外掛程式」會引導登入；這張圖還沒有完成連線。登入後依實際畫面核對帳號與存取範圍。', 'This is the public Google Drive listing. “Install plugin” leads to sign-in; this image does not show a completed connection. After signing in, check the account and requested access on your own screen.'),
 'notion': ('notion-entry-zh.jpg',635,245, '確認是 Notion，再繼續', 'Check that this is Notion', '這是公開的 Notion 服務介紹頁。「安裝外掛程式」會引導登入；這張圖還沒有選工作區或授權頁面。後續依實際畫面，只選這次要練習的內容。', 'This is the public Notion listing. “Install plugin” leads to sign-in; no workspace or page access has been selected here. Follow your own screen and choose only the material for this exercise.'),
 'preview': ('html-preview-zh.jpg',800,640, '程式碼貼上方，操作結果看下方', 'Paste code above; test the result below', '上方大欄位放完整 HTML；按「更新隔離預覽」後，下方才出現網頁。請真的勾選項目，確認數字會變。圖中使用教材的參考修正版示範位置，不是你的 AI 必須產生的版型。', 'Paste the complete HTML in the large field, then select “Update isolated preview”. The webpage appears below. Click its checkboxes and check the count. This image uses the prepared reference fix to show the controls; your AI may produce a different layout.'),
}

for key,file,h,zh,en in (
 ('gmail-paste','gmail-paste-zh.jpg',280,'這課的郵件，貼上後會長這樣','This lesson’s email, pasted into ChatGPT'),
 ('drive-paste','drive-paste-zh.jpg',280,'這課的兩個方案，貼上後會長這樣','This lesson’s two plans, pasted into ChatGPT'),
 ('notion-paste','notion-paste-zh.jpg',250,'這課的筆記，貼上後會長這樣','This lesson’s notes, pasted into ChatGPT')):
    SHOTS[key]=(file,635,h,zh,en,'在 ChatGPT 新對話的輸入框按 Ctrl+V（Mac：⌘V）。確認資料與要求都貼上後，按右下角的向上箭頭送出；長文字可在框內捲動。','In a new ChatGPT conversation, click the message box and press Ctrl+V (Mac: ⌘V). Check that both the material and request are present, then send with the upward arrow at the bottom right. Scroll inside the box to read long drafts.')

def figure(key,lang,prefix,show_title=True):
    file,w,h,zh,en,zhtext,entext=SHOTS[key]
    title,text=(en,entext) if lang=='en' else (zh,zhtext)
    url=prefix+'assets/walkthrough/'+file
    zoom='View larger image' if lang=='en' else '查看大圖'
    return '<figure class="walkthrough-shot"><figcaption>'+('<strong>'+escape(title)+'</strong>' if show_title else '')+'<p>'+escape(text)+'</p></figcaption><a class="screenshot-link" href="'+url+'" target="_blank" rel="noopener" data-screenshot aria-label="'+escape(zoom+': '+title,quote=True)+'"><img src="'+url+'" width="'+str(w)+'" height="'+str(h)+'" loading="lazy" alt="'+escape(title+' — '+text,quote=True)+'"><span>'+zoom+' ↗</span></a></figure>'

def note(lang):
    return '<p class="screenshot-note">'+('Real screenshots · 2026-10-29 · Traditional Chinese interface, with English instructions. The screen may vary by account or version. Examples contain fictional data.' if lang=='en' else '實際截圖 · 2026-10-29 · 畫面可能依帳號與版本不同。示範只使用虛構資料。')+'</p>'

def chat_guide(lang,prefix,key):
    en=lang=='en'
    steps=[('start','開啟 ChatGPT，找到輸入框','Open ChatGPT and find the message box'),('paste','貼上資料，送出要求','Paste the material and send'),('answer','核對回答中的日期與資訊','Check dates and facts in the response'),('followup','在同一段對話追問','Ask for a change in the same conversation')]
    panels=''.join('<details class="visual-step" name="visual-'+key+'"'+(' open' if key=='M01' and i==0 else '')+'><summary>'+str(i+1)+'. '+(english if en else chinese)+'</summary>'+figure(shot,lang,prefix,False)+'</details>' for i,(shot,chinese,english) in enumerate(steps))
    if key=='M01':
        return '<div class="visual-guide"><h3>'+('Follow the pictures, one step at a time' if en else '看圖操作，一次看一步')+'</h3>'+panels+note(lang)+'</div>'
    shot={'M04':'gmail-paste','M05':'drive-paste','M06':'notion-paste'}.get(key)
    title='Need help with the controls? See the Lesson 1 example' if en else '不知道在哪裡操作？看第 1 課的圖解'
    return '<div class="visual-guide">'+(figure(shot,lang,prefix) if shot else '')+'<details class="common-visuals"><summary>'+title+'</summary>'+panels+note(lang)+'</details>'+(note(lang) if shot else '')+'</div>'


def connection_guide(lang,prefix,key=None):
    keys={'M04':['directory'],'M05':['drive'],'M06':['notion']}.get(key,['directory','drive','notion'])
    return '<div class="visual-guide">'+''.join(figure(k,lang,prefix) for k in keys)+note(lang)+'</div>'

def zoom_dialog(lang):
    close='Close image' if lang=='en' else '關閉大圖'
    hint='Scroll sideways to see details on a small screen.' if lang=='en' else '小螢幕可左右捲動，查看原尺寸細節。'
    return '<dialog id="screenshot-dialog" aria-label="'+('Screenshot' if lang=='en' else '操作截圖')+'"><form method="dialog"><button autofocus>'+close+'</button></form><p>'+hint+'</p><div class="image-pan" tabindex="0" aria-label="'+hint+'"><img id="screenshot-large" alt=""></div><p id="screenshot-caption"></p></dialog>'
