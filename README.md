# AI 生活應用小講座

一份能從頭學到做出成品的單頁教材，支援繁體中文與英文。

- [繁體中文](https://k1everwann.github.io/ai-life-lab/)
- [English](https://k1everwann.github.io/ai-life-lab/en/)

## 在同一頁學會什麼

1. 看到 Travel、Japanese N1、Home、TickForge 的用途，分清資料、AI、程式與規則的角色。
2. 跟著 Gmail、Google Drive、Notion 的步驟，對照輸入、問法、固定示範輸出與來源核對，完成判斷題。
3. 自己提問、追問，找出混淆期限與捏造資訊的錯誤，再核對自己的結果。
4. 把待辦整理成一行一項，由網站固定範本製作可勾選、計數與重設的清單網頁。
5. 下載文字紀錄與 HTML 成品，重新開啟測試；課後在同頁換自己的資料繼續。

全程60分鐘：四個成品8、三個接資料應用24、提問與核對12、清單工具13、保存與延伸3。首頁沒有講師頁或另一份課後教材的連結；舊 instructor.html 與 next-steps.html 入口直接導回同頁。

## 教學資料與真實操作

公開示範全部使用虛構資料，不含私人行程、照片、帳單、交易、設備或來源網址。本站不呼叫 AI，也不連接帳號、設備或券商。

連接器示範要先把教學資料準備到對應帳號：Gmail有A郵件、Drive有目前行程B與舊版D、Notion有C筆記，再指定實際來源。課堂可直接複製相同文字到自己的AI工具練習，不要求學員先完成三種帳號連接。讀資料、產生草稿、寄信與建立頁面是不同步驟。

AI協助整理清單內容；清單HTML由固定範本產生。工具匯入前後需要人工只保留可執行待辦，不把標題或提醒冒充已辨識的任務。第一版清單重新整理不保留勾選進度，成品會清楚說明。

## 維護

- `scripts/build_course.py`：由以下來源產生中英文首頁及相容導回頁，勿直接修改生成的HTML。
- `course-content.json`：雙語完整教學、操作步驟、示範結果、判斷題、找錯題與課後需求。
- `seminar-content.json`、`templates/showcase-*.html`：四個互動示意、共用來源A/B/C與基本學習紀錄文字。
- `course.js`、`course.css`：三應用練習、找錯互動、清單工具、單頁版面。
- `seminar.js`、`seminar.css`：四個示意及文字紀錄保存。`language.js`切語言前提醒保存修改。
- `scripts/build_companion_pages.py`：舊維護命令的相容入口，會呼叫build_course。

```text
python scripts/build_course.py
python scripts/validate.py
python -m http.server 5085 --bind 127.0.0.1
```

原生HTML/CSS/JavaScript，GitHub Pages從repository root提供服務。Node不在PATH時用AI_LAB_NODE指定；既有PDF驗證需pypdf。

`analysis.html`、`practice.html`、`web-project.html`保留為頁尾收合的深入選修，不是完成主課的前提。舊版雙路線教案與PDF由build_materials.py維護，不代表本次單頁課程。放大字體切換維持移除。

驗證涵蓋資料、答案、來源、課時、雙語、引用、語法與公開資料邊界；瀏覽器另測複製、判斷題、成品下載與重開、勾選計數、語言提醒及窄螢幕。真實教學帳號與學員試教仍需課前彩排。交付狀態見HANDOFF.md。
