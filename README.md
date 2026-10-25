# AI 生活實驗室

給一般家庭與零基礎學員的 AI 教材。提供兩條各自完整的 60 分鐘課程：手機整理生活資訊，或電腦製作自己的網頁。

- 網站：https://k1everwann.github.io/ai-life-lab/
- 講師入口：https://k1everwann.github.io/ai-life-lab/instructor.html
- 手機路線：https://k1everwann.github.io/ai-life-lab/?route=phone#classroom
- 電腦路線：https://k1everwann.github.io/ai-life-lab/?route=computer#classroom
- 既有工程教材：https://k1everwann.github.io/codex-starter-guide/

## 使用方式

先看成果展示與共同原理，再選擇一條課程。上課可開啟投影模式；學員在手機或電腦複製練習指令，提交到自己可用的 AI 工具。網站本身沒有呼叫 AI，也沒有接入信箱或雲端硬碟。

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

## 本機預覽與驗證

使用 Python 3：

    python -m http.server 5085 --bind 127.0.0.1

開啟 http://127.0.0.1:5085/。正式分享使用 GitHub Pages 網址。

驗證腳本需要 Python 的 reportlab 與 pypdf 套件，以及 Node.js；網站瀏覽不需要這些套件。

    python scripts/validate.py
    node --check script.js

PDF 重建需要 reportlab 與繁體中文字型。預設使用 Windows 的 Microsoft JhengHei，可透過 AI_LAB_FONT 與 AI_LAB_FONT_BOLD 指定可嵌入字型路徑：

    python scripts/build_materials.py

重建後須渲染 PDF 並檢視每頁排版。PDF 中的來源與功能說明是 2026-10-25 的教材核對狀態，不代表每次開課的產品可用性。

## 隱私與展示界線

本公開 repository 只包含虛構練習資料及已核實的專案功能摘要。沒有私人資料庫、真實衣櫃、私人原圖、信件、主機位址、憑證或私人 Notion 頁面。

成果區是功能教學重現，不是正式系統截圖。Forge Outfit 的選衣規則、AI 影像與排程分開說明；Forge Glow 是書影音資料整理案例，不宣稱內建 AI。N1 案例說明作答與查證方式，不發布私人音檔或題庫。

只有路線選擇、查核選項與驗收勾選保存在本機瀏覽器 localStorage。自由輸入與程式碼不自動保存；按下載時才在本機建立檔案。網站不設分析追蹤。

HTML 預覽使用不含 same-origin 權限的 sandbox 與 CSP 限制資源。預覽仍會執行使用者貼入的 JavaScript；只使用可信任、無私人資料的練習碼，不能把預覽當成程式安全審查。

## 發布

GitHub Pages 使用 main branch 的 repository root，無框架、套件安裝或建置流程。先驗證、檢視差異、檢查敏感資料，再明確 stage 與推送。部署狀態與本次驗證見 HANDOFF.md。
