"""Build the public instructor page and two PDF teaching handouts."""
from pathlib import Path
from html import escape
import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
URL = "https://k1everwann.github.io/ai-life-lab/"
VERIFIED = "2026-10-25"
PHONE = [
("0-7", "7", "成果展示與共同原理", "看見用途，知道結果需要核對"),
("7-15", "8", "讀通知，找出錯誤草稿", "區分活動日、截止日與未知資訊"),
("15-23", "8", "短問句、看缺漏、補一個要求", "知道指令可以依草稿逐步補充"),
("23-38", "15", "手機五步操作與一次修改", "複製、貼上、返回核對並保留成果"),
("38-48", "10", "Gmail 與 Drive 各約五分鐘", "看懂工具取資料與核對的分工"),
("48-55", "7", "查核原文、發布者與預算", "區分忠實整理、來源可信與未知費用"),
("55-60", "5", "保存成果與出口題", "重新找到自己的清單，說出查核方式"),
]
COMPUTER = [
("0-7", "7", "成果展示與共同原理", "看懂從小問題到作品的過程"),
("7-15", "8", "看成品，寫三項需求", "選一個用途與最小功能"),
("15-23", "8", "生成、存檔與預覽示範", "分辨程式碼、檔案與可操作畫面"),
("23-38", "15", "製作第一版", "自己的 HTML 可以重新開啟"),
("38-48", "10", "測試後修改一次", "依實際結果描述問題"),
("48-55", "7", "窄螢幕與互動互測", "勾選、取消、重設與數量一致"),
("55-60", "5", "保存作品與說明限制", "知道是否保存進度，選一個後續方向"),
]
NOTICES = [
("A", "11/02", "社區自然觀察活動", "11/08（日）09:00-12:00 舉辦；11/05（四）18:00 報名截止。透過社區表單報名，成功與否需等確認信。"),
("B", "11/01", "手作課舊通知", "原訂 11/07（六）10:00，在一樓教室。"),
("C", "11/02", "手作課更正通知", "更新 B 為 11/07（六）14:00、二樓教室。11/04（三）20:00 前回覆能否出席。"),
("D", "11/02", "訂單取貨提醒", "11/06（五）前到指定門市領取，沒有提供營業時間或最後取貨時刻。"),
]
PHONE_PROMPT = "請只根據通知 A-D 整理待辦草稿，列出要做什麼、處理期限、活動時間、來源與待確認資訊。更正通知優先於舊通知，區分活動日與報名截止日。未寫明的時間或狀態標示待確認，不自行補齊。僅整理，不代為報名、回信或付款。"
BUILD_PROMPT = "請在新的練習資料夾製作單檔 index.html，主題是我的旅行準備清單，包含用途說明與至少三個項目。可勾選與取消，完成數即時更新，提供全部重設按鈕。使用繁體中文，390px 手機寬度也可操作。HTML、CSS、JavaScript 放同一檔，不使用外部套件、API、登入或網路字型。第一版重新整理後可重設，請在畫面說明。只處理練習資料夾，不部署。完成後列出我應親自執行的測試步驟。"
SOURCES = [
("公開交易研究框架與模擬界線", "https://github.com/k1everwann/tickforge-community"),
("ChatGPT 年齡與成人操作說明", "https://help.openai.com/en/articles/8313401-is-chatgpt-safe-for-all-ages"),
("既有工程入門教材", "https://github.com/k1everwann/codex-starter-guide"),
("ChatGPT 使用與成果查核", "https://learn.chatgpt.com/docs/use-chatgpt"),
("插件與手機可用性", "https://learn.chatgpt.com/docs/plugins"),
("Codex 執行環境", "https://learn.chatgpt.com/docs/environments/modes"),
("Claude Code 官方入門", "https://code.claude.com/docs/en/quickstart"),
("語言模型與文字生成原理", "https://developers.google.com/machine-learning/crash-course/llm/transformers"),
("AI 能力與批判判斷架構", "https://www.unesco.org/en/articles/ai-competency-framework-students"),
]
# Page blocks: paragraph, heading, bullet, table, callout.
PAGES = [
("一堂課的目標與提案", [
("p", "這份教材供一般家庭與 AI 零基礎學員使用。依現場設備選擇手機或電腦路線，每一套各自完整 60 分鐘，包含相同的前 7 分鐘成果展示與原理說明。"),
("callout", "讓學員完成一件自己用得上的小事，並親自確認它是否可靠、是否能用。"),
("h", "對總經理的三十秒說明"),
("p", "我們用真實生活專案讓學員看見可能性，再用手機整理通知，或用電腦做出自己的小網頁。課程交付的是可核對的待辦草稿或可操作的作品；教學網站可分享、課後可重做。"),
("table", (["路線", "設備與前置", "可帶走的成果"], [
["A 手機生活應用", "手機與可用的文字 AI；核心練習不需連接器", "經本人核對的待辦草稿與下次可用的需求"],
["B 電腦製作網頁", "電腦與已能使用的 Codex、Claude Code 或程式 AI", "自己的 HTML、一次修改與實測紀錄"]])),
("h", "上課與分享入口"),
("p", URL),
("p", "先開主頁，展示成果，再選 A 或 B。放大字級可提高閱讀字級；講師頁有流程、備案與下載。兩條路線是不同場次的備案，不要求一位講師同時教完兩套。"),
("h", "備課先看三件事"),
("bullet", "確認學員設備與工具已可用，安裝登入在課前完成。"),
("bullet", "講師只用教學帳號與虛構資料示範連接器，不投影私人信箱。"),
("bullet", "找不同熟練度的人先試走，記錄卡住的位置與時間；尚未宣稱教學成效已驗證。"),
]),
("共同開場與成果展示講稿", [
("p", "0-3 分鐘只主講投資研究與學習網站，各約 90 秒；3-7 分鐘解釋原理。每例說明：自己的問題、可操作成果、AI 與工具分工、學員今天能開始的一步。"),
("h", "主講兩例，其餘供自行點閱"),
("table", (["專案", "可以這樣說", "從小處開始"], [
["TickForge Community（主講）", "公開交易研究框架：資料、規則、選用 AI 複核與風險檢查分工，只做模擬；不展示私人投資狀況。", "股票資料的來源、時間、單位與缺漏核對清單"],
["Forge Outfit", "天氣資料、選衣規則、AI 示意圖與排程提醒各有分工。", "下雨天出門準備清單"],
["Forge Japanese N1（主講）", "用網站整理教材與練習，作答後看證據；不是即時 AI 家教。", "三題自己的練習與解析"],
["Forge Glow", "用資料庫與 API 整理書籍、電影與影集收藏；不把一般資料庫叫做 AI。", "三本書的閱讀清單"],
["公開工程教材", "把實作整理成下一個人能學的網站與原始碼。今天之後還能繼續深入。", "保存需求、修改與驗收過程"]])),
("h", "三個共同原理"),
("bullet", "模型從範例學到模式，依眼前指令與材料生成答案或程式；流暢不保證正確。"),
("bullet", "連接器與工具決定能取得什麼資料、能執行什麼動作；沒有授權的資料不能假設已讀到。"),
("bullet", "人要回原文、算總額、實際操作。把待辦列出來，不等於已完成；產出程式，也不等於功能正確。"),
("callout", "投資研究示意中，AI 逾時時拒絕候選進場，風險退出不等待 AI；先前狀態不明則阻擋新進場。不展示價格、績效或買賣建議，今天從核對清單或小測驗開始。"),
("p", "展示區為經標示的虛構資料重現，並非正式系統截圖。不要臨場打開私人主機總覽、衣櫃、真實郵件或部署設定。"),
]),
("A 手機路線 六十分鐘教案", [
("table", (["時間", "活動", "看得見的成果"], [[r[0]+" 分",r[2],r[3]] for r in PHONE])),
("h", "四項學員驗收"),
("bullet", "先用簡短任務取得草稿，再親自補一個要求；成人操作組由孩子說需求、成人送出，分開記錄平台操作。"),
("bullet", "回通知原文，區分一項報名截止與活動日期，修正錯誤或遺漏。"),
("bullet", "辨識至少一項目前無法判斷的內容，不接受 AI 自行補出的時間。"),
("bullet", "能說明原文也需要核對發布者；保存修正清單後重新找回。搜尋不保證完整，清單不代表已執行。"),
("h", "跟不上時怎麼調整"),
("p", "五步操作：按複製 → 切到 AI 長按輸入欄貼上並送出 → 切回教材 → 對照通知、補要求修改 → 把成果貼到帶走卡。成人操作組與無帳號組保留判斷練習，不混算本人平台操作。"),
("p", "Gmail、Drive 各五分鐘維持正式課程。先試走登入與切換；練習用同一組通知，不另加情境。結束時可複製到備忘錄或下載，再開啟確認真的保存。"),
]),
("A 練習資料與查核答案", [
("p", "全部為虛構教學資料，情境日 2026-11-02，日期與時間採 Asia/Taipei。"),
("table", (["通知", "內容"], [[n[0]+" / "+n[1]+" "+n[2],n[3]] for n in NOTICES])),
("h", "先短問，再補條件"),
("p", "先問：請把通知 A-D 整理成待辦清單。回原文看看期限、版本與未知時間有沒有問題，再親改一個要求，例如：請附通知來源，沒寫明的時間標待確認。"),
("h", "修改後可參考的整合版需求"),
("callout", PHONE_PROMPT),
("h", "參考答案與易錯點"),
("bullet", "活動報名：11/05 18:00 截止，活動為 11/08 09:00-12:00，來源 A；報名是否成功仍需確認信。"),
("bullet", "手作課回覆：11/04 20:00 截止；課程為 11/07 14:00、二樓，來源 C 更新 B。"),
("bullet", "包裹：11/06 前領取，來源 D；營業時間、最後取貨時刻均未知。"),
("p", "查核題依序為：與原文矛盾、有依據、目前無法判斷。對得上原文只代表忠實整理；若原文是群組轉傳，仍要向主辦單位確認日期與更新，不能把轉傳當作正式通知。"),
]),
("A 連接器與雲端資料示範", [
("h", "Gmail 約五分鐘"),
("p", "使用事先準備的教學信件。先確認登入帳號與允許動作，再指定時間範圍，展示一筆待辦如何點回原信核對。"),
("callout", "請查找最近七天本次可取得的信件，整理需要我回覆或處理的事項，附原信來源、期限與搜尋範圍。已讀不代表完成；沒有明確期限標待確認。僅讀取與整理。"),
("p", "不宣稱信箱已完整掃描，也不要求全班現場授權私人帳號。連接器出錯時，直接使用相同的虛構通知包示範，不花十分鐘排查授權。"),
("h", "Google Drive 約五分鐘"),
("p", "事先在教學 Drive 放入預算資料，以文件連結指定讀取。若只能找到檔名，不能假設已讀到內容。先確認日期、人數、幣別與計價單位，再分析。"),
("table", (["方案", "已知資料", "可驗證的計算"], [
["A", "同日四位成人，每人 800 元，整團交通 1,200 元，午餐未知", "800 × 4 + 1,200 = 4,400 元；午餐另計"],
["B", "同日四位成人，整團 4,000 元，交通與午餐已含", "已知總額 4,000 元"]])),
("p", "CSV 與資料說明可由講師頁下載。A 的午餐未知，不是零元；B 的交通已包含，不再重複加一次。此為算術與資料口徑練習，不是實際旅遊報價。"),
("h", "課前必查"),
("bullet", "用實際 iPhone／Android、預計帳號與網路試走。可用功能受方案、地區、插件與權限影響。"),
("bullet", "12 歲的 ChatGPT 實際互動由成人進行，孩子提出要求與查核；入口前說明，沒有成人時用本頁草稿。不要求借帳號。"),
("bullet", "只讀取指定教學資料。寄信、報名、付款與建立日曆不列入本堂練習。"),
]),
("B 電腦路線 六十分鐘教案", [
("table", (["時間", "活動", "看得見的成果"], [[r[0]+" 分",r[2],r[3]] for r in COMPUTER])),
("h", "課前前置"),
("bullet", "確認 Codex、Claude Code 或其他工具已可登入、接收需求及取得程式碼。VS Code 是編輯器，另確認是否有 AI 能力。"),
("bullet", "準備新的練習資料夾與瀏覽器。當堂不集中安裝工具、處理 API 金鑰或設定雲端環境。"),
("bullet", "Codex 本機模式與雲端模式能存取的檔案不同；依實際工具確認作品要存到哪裡。"),
("h", "最小作品"),
("p", "一個 index.html，含標題、用途與至少三個項目。支援勾選、取消、即時計數與全部重設，窄螢幕可閱讀。第一版不要求保存進度，但須明確說明。"),
("p", "完成品：examples/my-checklist.html；起步範本：examples/starter.html。範本刻意只有內容，讓學員請 AI 補上互動。"),
]),
("B 製作需求 測試與故障備案", [
("callout", BUILD_PROMPT),
("h", "四項可觀察驗收"),
("table", (["測試", "實際操作", "成功條件"], [
["重新開啟", "關閉後再開自己的 HTML", "看見自訂標題與至少三個項目"],
["勾選與取消", "勾兩項，再取消一項", "完成數依序 2、1"],
["全部重設", "至少勾一項，再按全部重設", "所有勾選清除，完成數為 0"],
["窄螢幕與修改", "縮窄視窗，完成一項自訂修改再測", "內容可讀，按鈕可用，受影響功能正確"]])),
("h", "描述錯誤的句型"),
("p", "我做了什麼 → 看到什麼 → 期待什麼。例如：勾選兩項後仍顯示 0，預期應為 2；請修正計數並保留我的標題與清單。"),
("h", "故障備案"),
("bullet", "檔案不能開：先確認檔名為 index.html，而非 index.html.txt；使用純文字存檔。"),
("bullet", "工具不能直接改檔：改請它輸出完整 HTML，複製到編輯器後存檔。"),
("bullet", "AI 不能用：用起步範本與完成品比較，先做需求與測試；註明尚未完成 AI 製作步驟。"),
("bullet", "預覽與獨立檔案不同：隔離框架會限制部分功能。程式只用可信任的練習碼，下載後再測儲存等能力。"),
("p", "公開分享放在課後擴充。先移除私人內容，再選擇發布方式；生成、存檔、預覽與公開上線是不同階段。"),
]),
("現場準備與資料來源", [
("h", "開課前與現場檢查"),
("bullet", "課前在桌面、手機與投影上試走主要流程。確認公開網址、PDF、範例與複製按鈕可使用。"),
("bullet", "共用七分鐘後選一條主課程；設備混合時，另一條提供自學指引或助教協助，不讓一位講師同時講兩套。"),
("bullet", "依操作熟練度提供提示，避免以年齡判斷能力。可放大字級，讓操作員與查核員輪換。"),
("bullet", "網站不會自動保存自由輸入與 HTML。帶走卡含今天成果：可複製到備忘錄或下載 ai-life-takeaway.txt；請學員重新開啟確認。"),
("h", "素材採用與界線"),
("p", "課程方向參考個人 AI 工作坊筆記中的 Vibe Coding 與 Google Workspace 應用，並核對個人專案 README 與維護文件。公開版本只保留功能摘要，不包含私人筆記、帳號、主機資訊與原始資料。"),
("p", "展示均為虛構重現，無私人截圖或嵌入。股票研究依公開社群版說明，不代表私人正式系統；N1 與收藏數量不作成效證明。"),
("h", "官方與公開延伸資料"),
] + [("source",s) for s in SOURCES] + [
("p", "產品可用性與操作入口可能變動，開課前以實際帳號及官方文件再確認。本手冊是可執行的教案，學員成效仍待試教驗證。"),
])
]
STUDENT = [
("手機路線 學員速查卡", [
("p", "今天帶走：一份自己核對、修改並保存的待辦清單。用網站虛構通知練習，不需連接私人信箱。12 歲由成人實際操作 ChatGPT，孩子說需求、做查核。"),
("h", "先問一句，再親自補一個要求"),
("callout", "請把通知 A-D 整理成待辦清單。"),
("p", "看草稿是否分清期限與活動日、採用更正版本、把未知寫成確定。再補：請附來源；沒有寫明的時間請標待確認，不要猜。"),
("h", "手機五步操作"),
("bullet", "按教材的複製，看到提示；必要時手動選取複製。"),
("bullet", "開 AI 對話，長按輸入欄貼上，確認通知與任務再送出。"),
("bullet", "用 App 或分頁切換回教材，保留教材分頁。"),
("bullet", "核對原文，補一個要求，請 AI 修改後再確認。"),
("bullet", "把修正清單貼到帶走卡，複製到備忘錄或下載，再重新開啟。"),
("h", "核對內容，也核對來源"),
("p", "看期限、版本與未知資訊；再問原文由誰發布、何時更新。群組轉傳須向主辦單位確認；股票消息回正式公告核對時間與單位。AI 忠實抄寫不代表消息真實。"),
("h", "連接器與分析提醒"),
("p", "Gmail、Drive 各五分鐘示範。搜尋不保證完整；已讀不等於已完成。分析先對人數、幣別與每人／整團，未知費用不是零。"),
("h", "保存在哪裡"),
("p", "複製後到備忘錄貼上。下載檔 ai-life-takeaway.txt 可在瀏覽器下載清單或手機檔案尋找，位置依設定而異。自由輸入不會自動保存。"),
("p", "我的下次任務：________________  查核來源：________________"),
("p", URL+"?route=phone#classroom"),
]),
("電腦路線 學員速查卡", [
("p", "今天的成果：一個屬於自己的生活清單網頁，加上一項修改與親自測試。使用已準備好的 Codex、Claude Code 或程式 AI。"),
("h", "四個步驟"),
("bullet", "選一個小問題：旅行準備、閱讀計畫或活動清單。"),
("bullet", "交代用途、內容與可確認的功能，請 AI 建立單檔 HTML。"),
("bullet", "存成 index.html，用瀏覽器開啟。確認不是 .html.txt。"),
("bullet", "依實際操作提出一次修改，再測受影響的功能。"),
("callout", BUILD_PROMPT),
("h", "自己測四件事"),
("bullet", "重新開啟：標題與至少三個項目都在。"),
("bullet", "勾兩項、取消一項：完成數依序是 2、1。"),
("bullet", "全部重設：勾選清空，完成數回到 0。"),
("bullet", "縮窄視窗：內容可讀，操作可用；自訂修改仍正常。"),
("p", "第一版重新整理後可重設，請看清楚是否有保存進度。只在練習資料夾操作，公開分享前移除私人內容。"),
("h", "回報問題句型"),
("p", "我做了＿＿，看到＿＿，期待＿＿。請修正並保留＿＿。"),
("p", URL+"?route=computer#classroom"),
])
]

def text(value):
    return escape(str(value)).replace("\n", "<br/>").replace("–", "-").replace("—", "-")

def render_html(pages):
    sections=[]
    for i,(title,blocks) in enumerate(pages):
        parts=[f'<section id="part-{i+1}"><p class="eyebrow">備課 {i+1:02d}</p><h2>{escape(title)}</h2>']
        for kind,value in blocks:
            if kind=="h": parts.append(f"<h3>{escape(value)}</h3>")
            elif kind=="p": parts.append(f"<p>{escape(value)}</p>")
            elif kind=="bullet":parts.append(f'<p class="teacher-bullet">• {escape(value)}</p>')
            elif kind=="callout":parts.append(f'<div class="prompt-box"><p>{escape(value)}</p></div>')
            elif kind=="source":parts.append(f'<p><a href="{escape(value[1])}" target="_blank" rel="noopener">{escape(value[0])} ↗</a></p>')
            elif kind=="table":
                headers,rows=value
                parts.append('<div class="table-scroll"><table><thead><tr>'+''.join(f"<th>{escape(x)}</th>" for x in headers)+'</tr></thead><tbody>'+''.join('<tr>'+''.join(f"<td>{escape(x)}</td>" for x in row)+'</tr>' for row in rows)+'</tbody></table></div>')
        parts.append("</section>");sections.append("\n".join(parts))
    return '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#ffffff"><title>講師備課｜AI 生活實驗室</title><link rel="stylesheet" href="styles.css?v=3"></head><body class="instructor-page"><header class="site-header"><a class="brand" href="index.html">AI 生活實驗室<span>講師備課</span></a><nav aria-label="主要導覽"><a href="index.html">學員教材</a><a href="https://github.com/k1everwann/ai-life-lab" target="_blank" rel="noopener">GitHub ↗</a></nav><a class="button small outline" href="index.html">返回教材</a></header><aside class="course-sidebar"><p class="sidebar-title">教案目錄</p><nav aria-label="講師教案目錄"><a href="#part-1">課程目標</a><a href="#part-2">成果展示講稿</a><a href="#part-3">A\u3000手機教案</a><a href="#part-4">通知與參考答案</a><a href="#part-5">連接器示範</a><a href="#part-6">B\u3000電腦教案</a><a href="#part-7">測試與故障備案</a><a href="#part-8">課前準備與來源</a><a href="index.html">返回學員教材</a></nav></aside><details class="mobile-toc"><summary>教案目錄</summary><nav aria-label="講師教案目錄"><a href="#part-1">課程目標</a><a href="#part-2">成果展示講稿</a><a href="#part-3">A\u3000手機教案</a><a href="#part-4">通知與參考答案</a><a href="#part-5">連接器示範</a><a href="#part-6">B\u3000電腦教案</a><a href="#part-7">測試與故障備案</a><a href="#part-8">課前準備與來源</a><a href="index.html">返回學員教材</a></nav></details><main class="wrap instructor-content"><div class="instructor-hero"><p class="breadcrumb">課程教材 / 講師備課</p><h1>雙路線教案與備課資料</h1><p class="lead">兩套各 60 分鐘教案，包含共同開場、實作、驗收與故障備案。依設備選擇手機生活應用或電腦網頁製作。</p><div class="copy-row"><a class="button" href="downloads/instructor-guide.pdf" target="_blank" rel="noopener">講師手冊 PDF</a><a class="button outline" href="downloads/student-cards.pdf" target="_blank" rel="noopener">學員速查卡 PDF</a></div><div class="overview-downloads"><a href="downloads/family-notices.txt" download>通知文字檔</a><span>·</span><a href="downloads/travel-budget.csv" download>預算 CSV</a><span>·</span><a href="downloads/travel-budget-notes.txt" download>預算資料說明</a></div></div>'+"\n".join(sections)+'</main><footer class="site-footer wrap"><p>內容核對 2026-10-25（Asia/Taipei）。練習為虛構資料；真實專案僅呈現經核實的功能摘要。</p><a href="index.html">返回學員教材</a></footer></body></html>'

def build():
    font=os.environ.get("AI_LAB_FONT",r"C:\Windows\Fonts\msjh.ttc")
    bold=os.environ.get("AI_LAB_FONT_BOLD",r"C:\Windows\Fonts\msjhbd.ttc")
    pdfmetrics.registerFont(TTFont("Lab",font,subfontIndex=0))
    pdfmetrics.registerFont(TTFont("LabBold",bold,subfontIndex=0))
    pdfmetrics.registerFontFamily("Lab",normal="Lab",bold="LabBold",italic="Lab",boldItalic="LabBold")
    INK=colors.HexColor("#202124");GREEN=colors.HexColor("#2458a6");LINE=colors.HexColor("#dfe3e8")
    styles={
    "title":ParagraphStyle("title",fontName="LabBold",fontSize=23,leading=32,textColor=INK,spaceAfter=17,wordWrap="CJK"),
    "p":ParagraphStyle("p",fontName="Lab",fontSize=10,leading=17,textColor=INK,spaceAfter=10,wordWrap="CJK"),
    "h":ParagraphStyle("h",fontName="LabBold",fontSize=13,leading=20,textColor=GREEN,spaceBefore=9,spaceAfter=9,wordWrap="CJK"),
    "small":ParagraphStyle("small",fontName="Lab",fontSize=8,leading=13,textColor=INK,spaceAfter=8,wordWrap="CJK"),
    "cell":ParagraphStyle("cell",fontName="Lab",fontSize=9,leading=15,textColor=INK,wordWrap="CJK"),
    "th":ParagraphStyle("th",fontName="LabBold",fontSize=9,leading=15,textColor=INK,wordWrap="CJK"),
    }
    def para(value,kind="p"):return Paragraph(text(value),styles[kind])
    def footer(canvas,doc):
        canvas.saveState();w,h=A4
        canvas.setFillColor(GREEN);canvas.rect(0,h-12,w,12,fill=1,stroke=0)
        canvas.setFont("Lab",8);canvas.setFillColor(colors.HexColor("#626973"))
        canvas.drawString(46,h-35,"AI LIFE LAB   /   AI 生活實驗室")
        canvas.setStrokeColor(LINE);canvas.line(46,40,w-46,40)
        canvas.drawString(46,26,"內容核對 "+VERIFIED+"  Asia/Taipei")
        canvas.drawRightString(w-46,26,str(doc.page));canvas.restoreState()
    def make_pdf(filename,pages):
        flow=[]
        for i,(title,blocks)in enumerate(pages):
            if i:flow.append(PageBreak())
            flow.append(para(title,"title"))
            for kind,value in blocks:
                if kind in ("p","h"):flow.append(para(value,kind))
                elif kind=="bullet":flow.append(para("• "+value))
                elif kind=="source":
                    flow.append(Paragraph('<link href="'+escape(value[1],quote=True)+'" color="#2458a6">'+text(value[0])+'</link><br/>'+text(value[1]),styles["small"]))
                elif kind=="callout":
                    t=Table([[para(value)]],colWidths=[A4[0]-112]);t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),colors.HexColor("#f5f6f8")),("BOX",(0,0),(-1,-1),.6,LINE),("LEFTPADDING",(0,0),(-1,-1),14),("RIGHTPADDING",(0,0),(-1,-1),14),("TOPPADDING",(0,0),(-1,-1),12),("BOTTOMPADDING",(0,0),(-1,-1),4)]));flow.extend([t,Spacer(1,12)])
                elif kind=="table":
                    headers,rows=value;total=A4[0]-96
                    if len(headers)==4:widths=[total*.13,total*.08,total*.35,total*.44]
                    elif len(headers)==3:widths=[total*.21,total*.39,total*.4]
                    else:widths=[total*.25,total*.75]
                    data=[[para(x,"th")for x in headers]]+[[para(x,"cell")for x in row]for row in rows]
                    t=Table(data,colWidths=widths,repeatRows=1,hAlign="LEFT")
                    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#eef1f5")),("VALIGN",(0,0),(-1,-1),"TOP"),("LINEBELOW",(0,0),(-1,-1),.5,LINE),("LEFTPADDING",(0,0),(-1,-1),9),("RIGHTPADDING",(0,0),(-1,-1),9),("TOPPADDING",(0,0),(-1,-1),8),("BOTTOMPADDING",(0,0),(-1,-1),8)]));flow.extend([t,Spacer(1,12)])
        dest=ROOT/"downloads"/filename;dest.parent.mkdir(exist_ok=True)
        doc=SimpleDocTemplate(str(dest),pagesize=A4,rightMargin=48,leftMargin=48,topMargin=57,bottomMargin=56,title="AI 生活實驗室 "+("講師手冊" if "instructor" in filename else "學員速查卡"),author="AI Life Lab")
        doc.build(flow,onFirstPage=footer,onLaterPages=footer)
        print(dest.name)
    (ROOT/"instructor.html").write_text(render_html(PAGES),encoding="utf-8",newline="\n")
    make_pdf("instructor-guide.pdf",PAGES);make_pdf("student-cards.pdf",STUDENT)

if __name__=="__main__":build()
