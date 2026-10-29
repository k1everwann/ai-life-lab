# AI 生活應用

十二個可自由選擇的生活應用課程，支援繁體中文與英文。固定目錄，一次閱讀一課；每課先看用途與成果，再跟著操作、換題練習、保存成果。四個私人專案由講師自行現場展示，網站不內嵌示意操作。

- [繁體中文](https://k1everwann.github.io/ai-life-lab/)
- [English](https://k1everwann.github.io/ai-life-lab/en/)

## 操作截圖

教材附 11 張實際介面截圖：第一次貼上與追問、Gmail／Drive／Notion 各課的貼文字練習、公開服務入口，以及 HTML 工作區。圖片放在對應操作旁，支援大圖與鍵盤關閉；英文版提供英文說明，圖中介面為繁中。截圖日期、來源與更新方式見 [截圖來源](assets/walkthrough/README.md)。連接器圖片只到公開介紹入口，不代表已完成帳號授權。

## 在同一頁可以練什麼

1. M01–M03：第一次操作 AI、只改一項要求、核對來源與版本。
2. M04–M07：Gmail、Google Drive、Notion 與月份資料分析。
3. M08–M10：請自己的 AI 生成 HTML、測試除錯、規則與去重模擬。
4. M11–M12：跨語言改寫及學員自己的生活應用。
5. 每課有資料、可複製要求、操作步驟、獨立題、挑戰、參考結果。觀念題、挑戰及操作紀錄均為選用；不同練習的紀錄各自暫存於本頁，離開前需下載。

首頁直接選課，不再展示講座排程。沒有講師版或另一份課後教材入口；舊 instructor.html 與 next-steps.html 直接導回同頁。所有單元可直接用錨點開啟，舊 lesson-gmail 等書籤保留。

## 教學資料與真實操作

公開示範全部使用虛構資料，不含私人行程、照片、帳單、交易、設備或來源網址。本站不呼叫 AI，也不連接帳號、設備或券商。

連接器示範要先把對應單元的教學資料準備到教學帳號，再指定實際信件日期、主旨或文件／筆記連結。課堂可直接複製相同文字到自己的AI工具練習，不要求學員先完成三種帳號連接。讀資料、產生草稿、寄信與建立頁面是不同步驟。

M08要求學員真正把需求交給自己的AI產生HTML，不能以預製清單取代。M09另附刻意漏算第一項的故障清單及參考修正版。程式碼預覽封鎖外部連線、沒有同源權限；輸入與程式碼不自動保存或上傳。切課保留本頁輸入，離頁前自行下載文字紀錄與HTML。

## 維護

- `scripts/build_course.py`：首頁與相容導回頁的統一建置入口，勿直接修改生成的HTML。
- `scripts/learning_layout.py`：目前首頁、章節目錄與單課閱讀介面。
- `scripts/build_curriculum.py`、`curriculum-content.json`：12課雙語內容、共用提示與教材下載產生器。
- `curriculum.js`、`curriculum.css`：選課、複製、判斷題、紀錄下載、隔離程式碼預覽、門檻與規則模擬。
- `downloads/curriculum/`：24份雙語教材文字、雙語故障／修正版HTML及簡單月份CSV。
- `course-content.json`：保留已建立的四展示說明及舊單課資料，與新版12課分開。
- `seminar-content.json`、`templates/showcase-*.html`：舊版四個互動示意與來源留存，目前首頁不使用。
- `course.js`、`course.css`、`seminar.js`：前版單課實作留存，新首頁不載入。
- `seminar.css`：四個展示的共用樣式。`language.js`切語言前提醒保存修改。
- `scripts/build_companion_pages.py`：舊維護命令的相容入口，會呼叫build_course。

```text
python scripts/build_course.py
python scripts/validate.py
python -m http.server 5085 --bind 127.0.0.1
```

原生HTML/CSS/JavaScript，GitHub Pages從repository root提供服務。Node不在PATH時用AI_LAB_NODE指定；既有PDF驗證需pypdf。

`analysis.html`、`practice.html`、`web-project.html`保留舊網址，不是完成主課的前提。舊版雙路線教案與PDF由build_materials.py維護，不代表本次單頁課程。放大字體切換維持移除。

驗證涵蓋12課完整性、先備鏈、下載與嵌入資料一致、月份算式、雙語時程、引用、語法與公開資料邊界；瀏覽器另測選課、複製、觀念題、紀錄下載、故障重現與修正版計數、隔離預覽、規則邊界與去重、語言提醒及窄螢幕。真實連接器帳號與學員試教仍需課前彩排；功能與代理稽核不代表教學成效已經驗證。交付狀態見HANDOFF.md。

## 本次教學設計參考

- [GitHub Skills: Introduction to GitHub](https://github.com/skills/introduction-to-github)：先說明會做出什麼，再逐步操作；問題排除另行展開。
- [Microsoft: Generative AI for Beginners](https://github.com/microsoft/generative-ai-for-beginners)：各課可獨立選擇，完成後有延伸學習。借鏡結構，不搬入開發環境門檻。
- [既有培訓指南](https://github.com/k1everwann/codex-starter-guide)：固定章節目錄、直接實作入口。
- [OpenAI 官方連接應用教學](https://developers.openai.com/training/walkthroughs/plugins-and-skills)：連接帳號、指定任務、回原始資料確認。功能依帳號與工作區而異。

以上為結構參考，課程文字與程式碼由本專案撰寫。
