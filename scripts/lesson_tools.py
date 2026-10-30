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
    steps=['Open your downloaded record: find your own proposed change, material source, and checking evidence.','Without an AI account, change one requirement in your own text record and compare the prepared result with its source. Mark this as material review.','Bring the record back for an adult to demonstrate your request. Eligible learners may continue in AI themselves; twelve-year-olds do not operate ChatGPT and ages 13–17 need parental permission.','Check the new result against its source, label who operated the tool, and save a new copy. This website does not import records; paste notes into the matching exercise if needed.'] if en else ['打開下載的紀錄，找到自己提出的修改、材料來源與核對證據。','沒有 AI 帳號也能繼續：先在自己的文字紀錄改一項需求，將預備結果與來源核對，標示為材料判讀。','下次帶回紀錄，請成人示範你的要求。符合資格者可自行在 AI 對話繼續；12歲不自行操作 ChatGPT，13–17歲須家長同意。','核對新版與來源，註明實際操作的人，再另存一份。本站沒有匯入紀錄功能；若要續填，請貼回對應練習欄位。']
    code='For HTML work, keep the complete code with your record. An adult demonstrator or eligible learner can continue from that version in the original conversation or paste it into a new one. AI cannot automatically see files on your computer.' if en else 'HTML 作品請連同完整程式碼保存。下次由成人示範，或符合資格者沿用原對話、將版本貼到新對話繼續；AI 不會自動讀取電腦裡的檔案。'
    return '<details class="resume-help"><summary>'+title+'</summary><ol>'+''.join('<li>'+escape(s)+'</li>' for s in steps)+'</ol><p>'+code+'</p></details>'
