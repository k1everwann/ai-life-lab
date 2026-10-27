# AI 生活實驗室

AI 生活應用小講座，適合零基礎學員。提供兩條各自完整的 60 分鐘課程：手機整理生活資訊，或電腦製作自己的網頁。

另新增「生活資料分析」連續兩堂各 60 分鐘：第一堂讀一份虛構信用卡資料、分類合計、追問與保存；第二堂比較月份，再選旅行或市場資料遷移。三組案例由生活問題開始，不要求先學寫程式。

- 生活分析：https://k1everwann.github.io/ai-life-lab/analysis.html
- English analysis：https://k1everwann.github.io/ai-life-lab/en/analysis.html

網站支援繁體中文／英文，頁面上方可切換語言。英文入口：
https://k1everwann.github.io/ai-life-lab/en/

電腦課後練習：https://k1everwann.github.io/ai-life-lab/next-steps.html

英文課後練習：https://k1everwann.github.io/ai-life-lab/en/next-steps.html

- 網站：https://k1everwann.github.io/ai-life-lab/
- 講師入口：https://k1everwann.github.io/ai-life-lab/instructor.html
- 手機路線：https://k1everwann.github.io/ai-life-lab/?route=phone#classroom
- 電腦路線：https://k1everwann.github.io/ai-life-lab/?route=computer#classroom
- 既有工程教材：https://k1everwann.github.io/codex-starter-guide/

## 使用方式

先看成果展示與共同原理，再選擇一條課程。開場主講投資研究與學習網站，各約 90 秒；其他案例供自行點閱。網站本身沒有呼叫 AI，也沒有接入信箱或雲端硬碟。

手機課先用簡短任務，再看缺漏、親自補一個要求；整合版長指令收在後方。五步指引涵蓋複製、貼上、返回、核對修改與保存成果。帶走卡可輸入今天核對後的清單，複製到備忘錄或下載，再重新開啟確認。成果與補充要求不會自動保存或上傳。

查核分兩層：AI 是否忠實整理，以及原始消息是否可信；活動回主辦單位，股票資訊回正式公告核對日期與單位。Gmail／Drive 38–48 分鐘、各約五分鐘的正式示範保留。

手機課的核心練習不需要 Gmail 或 Drive 連接器。講師可在自己的教學帳號示範已準備的虛構資料；功能依帳號與平台條件而異。未符合所選 AI 平台使用年齡的學員，由講師或家長操作 AI，孩子使用本頁做判斷練習。

## 內容與檔案

- index.html、styles.css、script.js：主教材、雙路線、互動查核與 HTML 預覽。
- instructor.html：課程安排、成果展示講稿、前置準備及故障備案。
- downloads/instructor-guide.pdf：雙路線講師手冊。
- downloads/student-cards.pdf：兩頁學員速查卡。
- downloads/family-notices.txt、travel-budget.csv：虛構練習資料。
- examples/starter.html：尚未加入互動的起步範本。
- examples/my-checklist.html：可勾選、取消、重設與即時計數的完成品。
- scripts/build_materials.py：產生講師頁與 PDF 的維護工具；使用者瀏覽不需要 Python。
- scripts/validate.py：驗證本地引用、錨點、練習資料、課程時長及 JavaScript 語法。
- en/：英文主教材、講師頁、互動程式、單檔範例與虛構練習資料。既有兩份 PDF 為繁體中文版，英文頁已明確標示，並提供完整英文 HTML 教案。
- next-steps.html、en/next-steps.html、continuation.css、continuation.js：五關課後練習、可複製需求、選修專題、驗收與復原。
- language.js：切換對應語言並保留課程路線與章節；修改過文字或程式碼時，先顯示留在本頁／仍要切換的提醒，不自動保存輸入。
- downloads/learning-log.txt、learning-log-en.txt：可下載的空白學習紀錄。
- analysis.html、en/analysis.html、analysis.js、analysis.css：雙語生活分析、分堂資料複製、學員追問、固定答案核對與文字紀錄下載。
- everyday-cases.json：中英文案例、來源列、預備分析、核對題與兩堂課的時間／完成條件。
- downloads/analysis/：四份虛構 CSV 與繁中／英文資料字典。
- scripts/validate_analysis.py：從實際 CSV 重算淨消費、分類、差額、零分母、旅行費用與重疊、市場可比條件及兩語課時；已納入 validate.py。

## 生活分析的案例與來源界線

信用卡第一堂只複製9月資料，第二堂另外複製兩月資料與學員追問。消費與負數退款納入、付款與轉帳排除；類別空白保留待分類。本月缺一筆金額，所以 6,700 是已知小計，1,700／34% 只比較已知金額，不能宣稱完整生活支出成長。

旅行案例按日期與地點整理、核對每人／整團費用、找出時間重疊，保留缺價與交通時間。旅行地圖／日誌功能概念已由維護文件查證，公開版本全部使用新編虛構資料，不轉載私人行程、照片、位置、數量、維運內容或來源連結。位置節點僅為教學示意，不是導航或最短路線。

市場案例使用虛構股票成交量與同一期貨合約成交量；可比資料分別計算，不把股與口相加、不混不同合約。數值是教學成交量，不是持倉、交易績效或即時資訊；來源日期亦為固定虛構情境。

網站只提供資料、可複製要求、固定預備答案與練習核對，沒有呼叫 AI 或連接私人帳號。講師在實際 AI 工具確認可用連接器、教學帳號與讀取範圍；無連接器可下載／貼上相同資料。真實學員試教與 AI 帳號流程仍待課前完成。

## 初學者與課後使用

電腦路線先說明教材、AI 工具、HTML 檔案與瀏覽器四個位置，再用六步走完製作需求到開啟網頁。保存 HTML 不等於保存勾選進度，也不等於公開上線。錯誤回報範例只在實際觀察到該錯誤時使用；沒有錯誤，可新增一個項目再測。

課後五關依完成條件前進：找回檔案、自訂主題、一次小修改、驗收與復原、選一個專題。另有保存勾選進度的選修挑戰，不要求付費方案、API key 或公開發布。這些活動另行安排，兩條正式課程仍各 60 分鐘。

已移除原本的放大字體功能；閱讀需要可使用瀏覽器縮放。

## 視覺設計

採教材文件版型：桌面左側章節目錄、手機可收合目錄，首頁直接呈現課程與下載入口。標題為桌面 28px、手機 24px，使用白灰底、深色文字與少量藍色操作，取消大型宣傳首屏、插畫卡片與大片留白。講師頁、範例與 PDF 使用相同配色。

參考版型與資訊結構：

- [MDN Learn](https://developer.mozilla.org/en-US/docs/Learn_web_development)：章節目錄與正文層級。
- [CS50x](https://cs50.harvard.edu/x/)：課程導覽、文字與教材直接呈現。
- [Google Machine Learning Crash Course](https://developers.google.com/machine-learning/crash-course/)：模組化課程入口。

未複製這些網站的圖像、品牌資產或程式碼。

## 本機預覽與驗證

使用 Python 3：

    python -m http.server 5085 --bind 127.0.0.1

開啟 http://127.0.0.1:5085/。正式分享使用 GitHub Pages 網址。

驗證腳本需要 Python 的 reportlab 與 pypdf 套件，以及 Node.js；網站瀏覽不需要這些套件。

    python scripts/validate.py
    node --check script.js

若環境的 node 命令無法直接啟動，可用 AI_LAB_NODE 指定可執行檔完整路徑。新增檢查包含雙語對應頁、語言標記、初學者導引、英文預算資料與講師頁產生器一致性。

PDF 重建需要 reportlab 與繁體中文字型。預設使用 Windows 的 Microsoft JhengHei，可透過 AI_LAB_FONT 與 AI_LAB_FONT_BOLD 指定可嵌入字型路徑：

    python scripts/build_materials.py

重建後須渲染 PDF 並檢視每頁排版。PDF 中的來源與功能說明是 2026-10-25 的教材核對狀態，不代表每次開課的產品可用性。

build_materials.py 重建中文講師頁與繁中 PDF；英文講師頁為獨立維護內容。調整教案時須同步 en/instructor.html，並人工核對用語、課時、來源與操作等價，不能只依賴靜態驗證。

## 隱私與展示界線

本公開 repository 只包含虛構練習資料及已核實的專案功能摘要。沒有私人資料庫、真實衣櫃、私人原圖、信件、主機位址、憑證或私人 Notion 頁面。

成果區是功能教學重現，不是正式系統截圖。Forge Outfit 的選衣規則、AI 影像與排程分開說明；Forge Glow 是書影音資料整理案例，不宣稱內建 AI。N1 案例說明作答與查證方式，不發布私人音檔或題庫。

TickForge 案例依 [TickForge Community 公開說明](https://github.com/k1everwann/tickforge-community) 重現資料、規則、選用 AI 複核、風險檢查與模擬的分工，不代表私人正式系統現況。AI 逾時拒絕候選進場，風險退出不等 AI；展示沒有行情、券商、帳戶、持倉、策略參數或績效。網站沒有螢幕擷取或讀取其他私人視窗的能力；現場分享仍應只分享教材分頁，避免整個桌面切換時露出私人視窗。

主教材的路線選擇、查核選項與驗收勾選保存在本機瀏覽器 localStorage。課後頁另提供預設關閉的五關勾選記錄，啟用後以 ai-life-lab.continuation.v1 保存勾選鍵，兩語共用；關閉或清除只刪除這項課後記錄。勾選是自我記錄，不是自動測試結果。自由輸入與程式碼不自動保存；按下載時才在本機建立檔案。網站不設分析追蹤。

HTML 預覽使用不含 same-origin 權限的 sandbox 與 CSP 限制資源。預覽仍會執行使用者貼入的 JavaScript；只使用可信任、無私人資料的練習碼，不能把預覽當成程式安全審查。

## 發布

GitHub Pages 使用 main branch 的 repository root，無框架、套件安裝或建置流程。先驗證、檢視差異、檢查敏感資料，再明確 stage 與推送。部署狀態與本次驗證見 HANDOFF.md。
