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
    steps=['Open your saved result and your last request.','Continue the original AI conversation, or paste both into a new one and ask for one change.','Check the new result and save a new copy.'] if en else ['打開上次保存的成果與要求。','沿用原本的 AI 對話，或把兩者貼進新對話，提出一項修改。','核對新版，再另存一份。']
    code='For a webpage, keep the complete HTML. AI cannot automatically read files on your computer.' if en else '網頁作品請保留完整 HTML；AI 不會自動讀取電腦裡的檔案。'
    return '<details class="resume-help"><summary>'+title+'</summary><ol>'+''.join('<li>'+escape(s)+'</li>' for s in steps)+'</ol><p>'+code+'</p></details>'
