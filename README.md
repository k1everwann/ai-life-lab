# AI 生活應用小講座

先看 Travel、Japanese N1、Home、TickForge 四個成品，再用同一份虛構資料做出自己的旅行準備清單。零基礎，使用電腦，一場 60 分鐘。

- [繁體中文](https://k1everwann.github.io/ai-life-lab/)
- [English](https://k1everwann.github.io/ai-life-lab/en/)
- [講師備課](https://k1everwann.github.io/ai-life-lab/instructor.html)
- [課後繼續做](https://k1everwann.github.io/ai-life-lab/next-steps.html)

## 一條學習順序

1. 看四個成品：旅行整理、個人學習、設備管理、投資資料研究。
2. 看 Gmail 找郵件、Drive 讀文件、Notion 找筆記的示範。
3. 複製三份教學資料到自己的 AI 工具，先問一個問題。
4. 看草稿後，親自補一個要求，回來源核對，再保存成果。

網站提供虛構互動示意、可複製資料與固定示例。實際 AI 與連接器操作在講師／學員自己的工具中進行；本站不呼叫 AI，不連私人帳號、設備或券商。各成品的既有功能概念已由文件查證，公開內容不含私人行程、照片、帳單、交易、來源連結或部署位置。

Gmail、Drive、Notion 可執行哪些動作，依帳號與權限確認。查詢、整理草稿、寄信與更新頁面是不同步驟；現場先確認內容與目的地，再示範寫入。無連接器可使用同一份文字資料；無 AI 可先判讀固定示例，另記尚未完成的 AI 操作。

## 課後教材

首頁與課後入口不要求學員先學寫程式。較深入的教材保留為獨立選修：

- `analysis.html`、`en/analysis.html`：信用卡、旅行、股票／期貨虛構資料分析，兩堂各 60 分鐘。
- `practice.html`、`en/practice.html`：較早的手機整理資訊／電腦做網頁雙路線，各 60 分鐘。
- `web-project.html`、`en/web-project.html`：網頁作品的保存、自訂、修改、驗收與復原。
- `workshop-instructor.html`、`en/workshop-instructor.html`：舊版雙路線教案；其中兩份繁中 PDF 是舊版教材，不是新講座流程。

舊版手機課的 Gmail／Drive 各五分鐘安排維持在該選修教案內。首頁舊的 `?route=computer` 或 `?route=phone` 網址仍能開啟新版小講座，首頁不再依過去的路線或瀏覽器紀錄改變主線。

## 維護與驗證

- 原生 HTML、CSS、JavaScript；GitHub Pages 從 repository root 提供服務，學員不需安裝套件。
- `seminar-content.json`、`seminar.js`、`seminar.css`：新版四成品示意與單一練習。雙語使用同一份內容來源。
- `scripts/build_companion_pages.py`：產生新版講師頁、課後頁與空白文字紀錄。
- `scripts/build_materials.py`：維護選修雙路線教案與既有繁中 PDF，不覆蓋新版講師頁。
- `language.js`：頁面上方切換繁中／英文；修改自由輸入後切換，先提醒保存。
- `scripts/validate.py`：驗證雙語、連結、錨點、課時、資料、JavaScript、既有 PDF 與公開資料邊界。

```text
python scripts/build_companion_pages.py
python scripts/validate.py
python -m http.server 5085 --bind 127.0.0.1
```

若 Node 不在 PATH，以 `AI_LAB_NODE` 指定可執行檔；需 Python 的 pypdf 驗證舊版 PDF。實際學員試教與教學帳號彩排仍須課前完成；靜態驗證不代表已驗證真實帳號的連接器流程。

版型採白灰底、深色文字與少量藍色，標題不超過 28px；沒有放大字體切換功能。交付與驗證狀態見 `HANDOFF.md`。
