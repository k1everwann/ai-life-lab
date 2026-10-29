"""Check teaching fixtures, full bilingual lesson coverage and course packaging."""
import csv
import json
import re
from decimal import Decimal
from pathlib import Path
from html.parser import HTMLParser
from build_curriculum import UI, lesson_text

ROOT=Path(__file__).resolve().parents[1]

class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.data=[]; self.inside=False; self.user_fields=[]; self.active=None
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='script' and a.get('id')=='curriculum-data':self.inside=True
        if tag=='textarea' and 'readonly' not in a:
            self.active=[];self.user_fields.append(self.active)
    def handle_data(self,text):
        if self.inside:self.data.append(text)
        if self.active is not None:self.active.append(text)
    def handle_endtag(self,tag):
        if tag=='script':self.inside=False
        if tag=='textarea':self.active=None

def shape(x):
    if isinstance(x,dict):return {k:shape(v) for k,v in x.items()}
    if isinstance(x,list):return [shape(v) for v in x]
    return type(x).__name__

def validate():
    data=json.loads((ROOT/'curriculum-content.json').read_text(encoding='utf-8'))
    modules=data['modules']; ids=[m['id'] for m in modules]
    assert ids==[f'M{i:02d}' for i in range(1,13)],'Need all twelve modules in order'
    assert len(set(m['anchor'] for m in modules))==12
    visited=set()
    for m in modules:
        assert set(m['needs'])<=visited, f'{m["id"]}: dependency missing or cycle'
        visited.add(m['id'])
        assert shape(m['locales']['zh-Hant'])==shape(m['locales']['en']),f'{m["id"]}: bilingual structure'
        for lang,c in m['locales'].items():
            assert all(c.get(k) for k in ('title','goal','why','outcome','quick','skip','source','prompt','expected','checks'))
            assert ('connection' in c)==(m['id'] in ('M04','M05','M06'))
            if c.get('connection'):
                assert all(c['connection'].get(k) for k in ('title','source','prompt','steps','expected'))
            assert 3<=len(c['steps'])<=7
            assert c['independent']['task'] and c['independent']['expected']
            assert all(c['challenge'][k] for k in ('task','source','prompt','expected'))
            assert 0<=c['quiz']['answer']<len(c['quiz']['choices'])
            assert c['quiz']['answer']==m['locales']['zh-Hant']['quiz']['answer']
            path=ROOT/'downloads'/'curriculum'/f'{m["id"].lower()}-{lang}.txt'
            assert path.read_text(encoding='utf-8')==lesson_text(m,lang),f'{path}: lesson pack drift'
    for lang in UI:
        for row,minutes in zip(UI[lang]['plansrows'],(60,90,120)):
            total=sum(int(re.search(r'(\d+)\s*$',part).group(1)) for part in row[1].split('→'))
            assert total==minutes,(lang,row,total)
        page=Page();page.feed((ROOT/('en/index.html' if lang=='en' else 'index.html')).read_text(encoding='utf-8'))
        embedded=json.loads(''.join(page.data))
        assert len(embedded['modules'])==12
        assert 'showcase' not in embedded, 'Embedded private-project simulations have been retired'
        fixture_files={'guided':'broken-checklist','independent':'reset-bug','challenge':'search-reset-bug'}
        for kind,name in fixture_files.items():
            expected=(ROOT/'downloads/curriculum'/f'{name}-{lang}.html').read_text(encoding='utf-8')
            assert embedded['debugFixtures'][kind]==expected,f'{lang}/{kind}: copied debugging source differs from downloadable file'
        for m,e in zip(modules,embedded['modules']):
            assert e['id']==m['id'] and e['source']==m['locales'][lang]['source']
        assert len(page.user_fields)==26 and not any(''.join(x).strip() for x in page.user_fields),'Learner text/code must start blank'
    rows=list(csv.DictReader((ROOT/'downloads/curriculum/monthly-spending.csv').open(encoding='utf-8')))
    source=next(m for m in modules if m['id']=='M07')['locales']
    for lang in source:
        lesson_rows=list(csv.reader(source[lang]['source'].splitlines()[1:]))[1:]
        assert [(r[0],r[1],Decimal(r[3])) for r in lesson_rows]==[(r['row_id'],r['month'],Decimal(r['amount_twd'])) for r in rows]
    sums={month:sum(Decimal(r['amount_twd']) for r in rows if r['month']==month) for month in ('2026-09','2026-10')}
    assert sums=={'2026-09':2100,'2026-10':2350}
    changes=[Decimal(rows[i+3]['amount_twd'])-Decimal(rows[i]['amount_twd']) for i in range(3)]
    assert changes==[150,50,50]
    assert len([d for d in changes if d>50])==1 and len([d for d in changes if d>=50])==3
    assert round((sums['2026-10']-sums['2026-09'])/sums['2026-09']*100,1)==Decimal('11.9')
    assert sums['2026-10']-100==2250
    assert round(Decimal(150)/2100*100,1)==Decimal('7.1')
    print('PASS curriculum: 12 full bilingual modules, dependency chain, blank learner fields and downloadable lessons')
    print('PASS curriculum fixtures: 2100→2350, +250/11.9%; >50 vs >=50 yields 1 vs 3; refund 2250/+150/7.1%')
    print('PASS flexible session slices: 60/90/120 minutes in both languages')

if __name__=='__main__':validate()
