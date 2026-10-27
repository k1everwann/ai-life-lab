"""Recalculate the fictional teaching cases from their downloadable source rows."""
from pathlib import Path
from decimal import Decimal
import csv
import json
import re

ROOT=Path(__file__).resolve().parents[1]

def validate():
    data=json.loads((ROOT/'everyday-cases.json').read_text(encoding='utf-8'))
    assert data['fictional'] is True and data['schemaVersion']==1
    assert data['currency']=='TWD' and data['timezone']=='Asia/Taipei'
    cases={case['id']:case for case in data['cases']}
    assert set(cases)=={'credit','travel','market'}
    tables={};ids=set()
    for case in cases.values():
        own_ids=set()
        for file in case['files']:
            path=ROOT/file['path'];assert path.is_file()
            if path.suffix!='.csv':continue
            with path.open(encoding='utf-8',newline='') as stream:rows=list(csv.DictReader(stream))
            assert rows and all(None not in row for row in rows)
            tables[path.name]=rows
            for row in rows:
                assert row['row_id'] not in ids
                ids.add(row['row_id']);own_ids.add(row['row_id'])
        for locale in ('zh','en'):
            content=case[locale]
            assert all(content.get(key) for key in ('title','hook','shortPrompt','followupPrompt','checks','preparedResult','unknowns'))
            for finding in content['preparedResult']['findings']:
                assert set(finding.get('rowIds',[]))<=own_ids
        for a,b in zip(case['zh']['checks'],case['en']['checks']):
            assert (a['id'],a['type'],a['expected'])==(b['id'],b['type'],b['expected'])
            assert [o['value'] for o in a.get('options',[])]==[o['value'] for o in b.get('options',[])]
        assert len(case['zh']['checks'])==len(case['en']['checks'])
        assert not re.search(r'[\u4e00-\u9fff]',json.dumps(case['en'],ensure_ascii=False))

    def consumption(rows):
        result=Decimal(0);missing=[];categories={}
        for row in rows:
            if row['transaction_type'] not in ('purchase','refund'):continue
            if not row['amount']:missing.append(row['row_id']);continue
            amount=Decimal(row['amount'])
            if row['transaction_type']=='refund':assert amount<0
            result+=amount
            key=row['category_hint'] or 'unknown'
            categories[key]=categories.get(key,Decimal(0))+amount
        return result,missing,categories
    previous,pm,pc=consumption(tables['credit-previous.csv'])
    current,cm,cc=consumption(tables['credit-current.csv'])
    expected=cases['credit']['expected']
    assert previous==expected['previous']==5000 and current==expected['current']==6700
    assert current-previous==expected['delta']==1700
    assert (current-previous)/previous*100==expected['percent']==34
    assert not pm and cm==expected['missingAmountRows']==['C1012']
    assert expected['currentComplete'] is False
    for category in expected['categories']:
        before=pc.get(category['id'],Decimal(0));after=cc.get(category['id'],Decimal(0))
        assert (before,after,after-before)==(category['previous'],category['current'],category['delta'])
        if before==0:assert category['percent'] is None
        else:assert (after-before)/before*100==category['percent']

    travel=tables['travel-plan.csv'];expected=cases['travel']['expected']
    total=Decimal(0);missing=[];overlap=0
    def minutes(value):
        h,m=map(int,value.split(':'));return h*60+m
    for i,row in enumerate(travel):
        if row['budget']=='':missing.append(row['row_id'])
        else:
            assert row['unit'] in ('per_person','per_group')
            total+=Decimal(row['budget'])*(Decimal(row['participants']) if row['unit']=='per_person' else 1)
        for other in travel[i+1:]:
            if row['day']==other['day']:
                overlap+=max(0,min(minutes(row['end']),minutes(other['end']))-max(minutes(row['start']),minutes(other['start'])))
    assert total==expected['knownBudget']==3800
    assert missing==expected['missingBudgetRows']==['T05']
    assert overlap==expected['overlapMinutes']==15 and expected['fullBudget'] is None

    market={row['row_id']:row for row in tables['market-check.csv']};expected=cases['market']['expected']
    for name in ('stock','futures'):
        before,after=[market[row_id] for row_id in expected[name+'Rows']]
        for key in ('instrument','metric','unit','contract','expiry'):
            assert before[key]==after[key]
        delta=Decimal(after['value'])-Decimal(before['value'])
        assert delta==expected[name+'VolumeDelta']
        assert delta/Decimal(before['value'])*100==expected[name+'VolumePercent']
    assert market['M05']['unit']!=market['M02']['unit']
    assert market['M06']['contract']!=market['M04']['contract']
    assert not market['M07']['value'] and not market['M07']['source_published']
    assert expected['mixedUnitTotal'] is None and expected['canInferDirection']=='no'

    assert len(data['lessons']['zh'])==len(data['lessons']['en'])==2
    for zh,en in zip(data['lessons']['zh'],data['lessons']['en']):
        durations=[s['minutes'] for s in zh['segments']]
        assert durations==[s['minutes'] for s in en['segments']]
        assert all(m>0 for m in durations) and sum(durations)==60
    print(f'PASS everyday analysis: {len(ids)} unique fictional source rows; bilingual answers and references agree')
    print('PASS card: 5000 / known 6700 / +1700 / 34%; missing price, excluded payments, refund and zero-base rules')
    print('PASS travel: known 3800 TWD / 15-minute overlap; missing costs remain unknown')
    print('PASS market volumes: +2000 shares (20%) / +20 contracts (25%); incompatible and missing rows retained')
    print('PASS two analysis lessons: matching bilingual segments, 60 minutes each')

if __name__=='__main__':validate()
