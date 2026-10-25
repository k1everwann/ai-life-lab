# AI Life Lab 交付與維護

## 目前範圍

- 新的公開教材網站，不改動既有 codex-starter-guide。
- Repository： https://github.com/k1everwann/ai-life-lab
- GitHub Pages： https://k1everwann.github.io/ai-life-lab/
- Branch：main；Pages source：repository root。
- 技術：原生 HTML、CSS、JavaScript；瀏覽無建置步驟。
- 已公開上線：GitHub Pages 首次 build 為 built，程式提交 dea991f273a4cf24b7a9b4f906ed537141073520。
- 正式 HTTP 驗證：首頁、講師頁、JS、CSS、兩份 PDF 與完成品共 7 個端點皆為 200，SHA-256 與本機完全相符。
- 公開首頁已在瀏覽器開啟，無 warning/error；新 repository 可見性為 PUBLIC。

## 內容與操作

- 兩條各 60 分鐘課程，包含共同 7 分鐘開場。依設備選一條，不要求一位講師同場教完兩套。
- 手機：虛構通知、需求複製、三題來源查核、Gmail/Drive 指令、旅遊預算與帶走卡。
- 電腦：需求組合、單檔 HTML 範本/完成品、隔離預覽、下載、四項實測。
- 成果：Outfit、Japanese N1、Glow 與既有工程教材功能摘要；互動均清楚標示教學重現。
- 公開資料：沒有私人 Notion 連結、個人衣櫃/收藏紀錄、真實信件、主機拓樸、私人圖片或憑證。

## 本次驗證

- scripts/validate.py：本地引用與錨點、雙路線連續 60 分鐘、情境日期星期、預算 4400/4000 與缺漏處理、PDF 頁數與文字、JS 語法、敏感內容檢查全部通過。
- 瀏覽器實測：成果題目與收藏切換、查核 3/3、預算 4400、通知複製、客製需求複製、範例載入及 iframe 預覽通過。
- 完成品互動：勾兩項為 2、取消一項為 1、重設為 0，均通過。
- 390px 瀏覽器：手機及電腦路線無文件水平溢位；測試階段 console 無 warning/error。
- PDF：講師手冊 8 頁、速查卡 2 頁，已全部渲染並逐頁視覺檢查。
- Astra 內容審查：已修正未知回覆狀態的推定與截止時間邊界。未發現其他發布阻斷。

## 維護規則

- 僅 route/audit/checklist 使用本機 localStorage；自由輸入與 HTML 不自動保存、不由網站主動上傳。
- HTML 預覽使用 sandbox 及 CSP，但仍執行貼入的程式；只用可信任且無私人資料的練習碼。
- PDF 與講師頁共用 scripts/build_materials.py 內容來源。更新後重建並渲染檢查；主頁的課程安排須同步核對。
- 成果與課程能力分開：不把規則引擎稱為 LLM、不把資料庫稱為 AI、不宣稱搜尋完整或已代為報名。
- 課前需在實際 iPhone/Android、投影及預計帳號確認產品可用性。瀏覽器尺寸檢查不等於手機實機驗證。
- 本教材尚未完成真實學員試教，不宣稱成效、完成率或節省時間。

## 靜態網站運作

- Entry point：index.html；講師頁：instructor.html。
- 正式服務由 GitHub Pages 管理，無私人主機部署、資料庫或排程。
- 健康檢查：首頁、instructor.html、script.js 與兩份 PDF HTTP 200；Pages build 的 commit 與 main 相符。
- 回復：將已確認可用的版本重新提交至 main，等待 Pages build 成功；避免 force push。
- 故障：先查 Pages build/status，再查路徑大小寫、引用與瀏覽器 console；不要修改 Forge 私人服務。

## 交付狀態與開課前待辦

- 公開 repository 建立、main 推送、Pages 啟用及正式內容驗證已完成。
- 本文件更新的提交另行推送後，確認 Pages 的最新 build commit 與 main 相符。
- 真實學員試教與手機實機測試於開課前完成。

## 2026-10-25 簡約教材版型

- 依使用者回饋，移除大型宣傳首屏、裝飾插畫、旋轉卡片、陰影與原綠米配色，改為白灰底、深色文字及少量藍色操作。
- 首頁直接顯示兩條課程與下載入口；桌面有固定章節目錄，手機使用可收合目錄。標題為桌面 28px、手機 24px。
- 講師頁、獨立範例與兩份 PDF 同步使用新的配色。兩條 60 分鐘課程、練習資料與互動能力保留。
- 版型參考實際查看的 MDN Learn、CS50x 與 Google Machine Learning Crash Course；來源連結與採用重點記於 README。沒有複製外部網站素材。
- 此次驗證：validate.py 與 diff check 通過；桌面及 390px 的主頁、講師頁沒有文件水平溢位；章節目錄可切換路線；查核 3/3、預算 4400、HTML 範例勾選 2→取消 1→重設 0 均正確；console 無 warning/error。
- PDF 仍為 8 頁講師手冊與 2 頁學員卡，已重新渲染並檢視全部頁面。
- 靜態 CSS／JS 引用加入版本參數，避免既有瀏覽器沿用舊版外觀。
- 發布仍使用 main 與相同 GitHub Pages 網址；本次最終提交與部署狀態以交付時 GitHub main 及 Pages build 為準。
