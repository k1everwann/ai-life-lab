"""Small, task-local helpers for source-code access and returning learners."""
from html import escape

def debug_links(lang,prefix,kind):
    names={'guided':('broken-checklist','correct-checklist'),'independent':('reset-bug','correct-reset'),'challenge':('search-reset-bug','correct-search-reset')}
    broken,fixed=names[kind];en=lang=='en'
    root=prefix+'downloads/curriculum/'
    links=[(broken,False,'Open the broken webpage ↗' if en else '開啟故障網頁 ↗'),(broken,True,'Download the original file' if en else '下載故障原檔'),(fixed,True,'Download the reference fix' if en else '下載參考修正版')]
    return '<div class="debug-files"><p>'+('First open the broken webpage and reproduce the error. The copy button includes its complete source code, so you do not need a text editor.' if en else '先開啟故障網頁，試出問題。下方複製按鈕會帶入完整程式碼，不必另外用記事本開檔。')+'</p><div class="actions">'+''.join('<a '+('download' if download else 'target="_blank" rel="noopener"')+' href="'+root+name+'-'+lang+'.html">'+text+'</a>' for name,download,text in links)+'</div></div>'

def resume_help(lang):
    en=lang=='en'
    title='How to continue next time' if en else '下次要怎麼接著做？'
    steps=['Open your downloaded record and copy your request and latest result.','Paste them into a new AI conversation, then add one change: “Continue from the version below. This time, only change …”','Check the new result and save a new copy. This website does not import records; paste your notes back into the matching exercise if needed.'] if en else ['打開下載的紀錄，複製自己的需求與最後成果。','貼到 AI 新對話，再加一句：「沿用以下版本，這次只改……」。','核對新版後再保存。本站沒有匯入紀錄功能；若要續填，請貼回對應練習的欄位。']
    code='For an HTML project, return to its AI conversation, or copy the complete HTML section from your saved lesson record into a new conversation. A file on your computer is not automatically visible to AI.' if en else 'HTML 作品可回到原本的 AI 對話繼續，或從已下載的操作紀錄複製「完整 HTML 程式碼」到新對話；AI 不會自動讀取電腦裡的檔案。'
    return '<details class="resume-help"><summary>'+title+'</summary><ol>'+''.join('<li>'+escape(s)+'</li>' for s in steps)+'</ol><p>'+code+'</p></details>'
