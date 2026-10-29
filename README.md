# AI 生活應用

十二個可自由組合的單頁課程，支援完整繁體中文與英文。先看 Travel、Japanese N1、Home、TickForge 的虛構功能重現，再挑一件事親手做。不預設程度；每課可先試、跟做、自己做或直接挑戰。

- [繁體中文](https://k1everwann.github.io/ai-life-lab/)
- [English](https://k1everwann.github.io/ai-life-lab/en/)

## 在同一頁可以練什麼

1. M01–M03：第一次操作 AI、只改一項要求、核對來源與版本。
2. M04–M07：Gmail、Google Drive、Notion 與月份資料分析。
3. M08–M10：請自己的 AI 生成 HTML、測試除錯、規則與去重模擬。
4. M11–M12：跨語言改寫及 Travel／N1／Home／TickForge 自選專題。
5. 每課有資料、可複製要求、操作步驟、獨立題、挑戰、參考答案、觀念題及操作紀錄下載。勾選是自我紀錄，不是自動驗收。

首頁附60／90／120分鐘核心練習組合，不宣稱短講完成全部整課。沒有講師版或另一份課後教材入口；舊 instructor.html 與 next-steps.html 直接導回同頁。所有單元可直接用錨點開啟，舊 lesson-gmail 等書籤保留。

## 教學資料與真實操作

公開示範全部使用虛構資料，不含私人行程、照片、帳單、交易、設備或來源網址。本站不呼叫 AI，也不連接帳號、設備或券商。

連接器示範要先把對應單元的教學資料準備到教學帳號，再指定實際信件日期、主旨或文件／筆記連結。課堂可直接複製相同文字到自己的AI工具練習，不要求學員先完成三種帳號連接。讀資料、產生草稿、寄信與建立頁面是不同步驟。

M08要求學員真正把需求交給自己的AI產生HTML，不能以預製清單取代。M09另附刻意漏算第一項的故障清單及參考修正版。程式碼預覽封鎖外部連線、沒有同源權限；輸入與程式碼不自動保存或上傳。切課保留本頁輸入，離頁前自行下載文字紀錄與HTML。

## 維護

- `scripts/build_course.py`：首頁與相容導回頁的統一建置入口，勿直接修改生成的HTML。
- `scripts/build_curriculum.py`、`curriculum-content.json`：12課雙語內容、共用UI與教材下載產生器。
- `curriculum.js`、`curriculum.css`：選課、複製、判斷題、紀錄下載、隔離程式碼預覽、門檻與規則模擬。
- `downloads/curriculum/`：24份雙語教材文字、雙語故障／修正版HTML及簡單月份CSV。
- `course-content.json`：保留已建立的四展示說明及舊單課資料，與新版12課分開。
- `seminar-content.json`、`templates/showcase-*.html`：四個互動示意、共用來源A/B/C與基本學習紀錄文字。
- `course.js`、`course.css`、`seminar.js`：前版單課實作留存，新首頁不載入。
- `seminar.css`：四個展示的共用樣式。`language.js`切語言前提醒保存修改。
- `scripts/build_companion_pages.py`：舊維護命令的相容入口，會呼叫build_course。

```text
python scripts/build_course.py
python scripts/validate.py
python -m http.server 5085 --bind 127.0.0.1
```

原生HTML/CSS/JavaScript，GitHub Pages從repository root提供服務。Node不在PATH時用AI_LAB_NODE指定；既有PDF驗證需pypdf。

`analysis.html`、`practice.html`、`web-project.html`保留為頁尾收合的深入選修，不是完成主課的前提。舊版雙路線教案與PDF由build_materials.py維護，不代表本次單頁課程。放大字體切換維持移除。

驗證涵蓋12課完整性、先備鏈、下載與嵌入資料一致、月份算式、雙語時程、引用、語法與公開資料邊界；瀏覽器另測選課、複製、觀念題、紀錄下載、故障重現與修正版計數、隔離預覽、規則邊界與去重、語言提醒及窄螢幕。真實連接器帳號與學員試教仍需課前彩排；功能與代理稽核不代表教學成效已經驗證。交付狀態見HANDOFF.md。
