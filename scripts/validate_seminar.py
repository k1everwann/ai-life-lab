"""Check the redesigned seminar's shared source data and beginner-critical facts."""
from pathlib import Path
from html.parser import HTMLParser
import json
import re

ROOT = Path(__file__).resolve().parents[1]

class SeminarPage(HTMLParser):
    def __init__(self):
        super().__init__()
        self.json_text = []
        self.in_json = False
        self.ids = set()
        self.inputs = {}
        self.active_input = None
        self.demos = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'script' and a.get('id') == 'seminar-data':
            self.in_json = True
        if tag == 'textarea' and a.get('id') in ('learner-followup', 'learner-result'):
            self.active_input = a['id']
            self.inputs[self.active_input] = ''
        if a.get('data-demo'):
            self.demos.append(a['data-demo'])

    def handle_data(self, value):
        if self.in_json:
            self.json_text.append(value)
        if self.active_input:
            self.inputs[self.active_input] += value

    def handle_endtag(self, tag):
        if tag == 'script':
            self.in_json = False
        if tag == 'textarea':
            self.active_input = None

def shape(value):
    if isinstance(value, dict):
        return {key: shape(item) for key, item in value.items()}
    if isinstance(value, list):
        return [shape(item) for item in value]
    return type(value).__name__

def validate():
    data = json.loads((ROOT / 'seminar-content.json').read_text(encoding='utf-8'))
    assert [row['key'] for row in data['schedule']] == ['opening', 'showcase', 'gmail', 'drive', 'notion', 'practice', 'takeaway']
    assert [row['minutes'] for row in data['schedule']] == [5, 12, 8, 8, 9, 15, 3]
    assert sum(row['minutes'] for row in data['schedule']) == 60
    assert set(data['locales']) == {'zh-Hant', 'en'}
    zh, en = data['locales']['zh-Hant'], data['locales']['en']
    assert shape(zh) == shape(en), 'Bilingual content has different keys or list lengths'
    for locale in (zh, en):
        assert list(locale['demoNames']) == ['travel', 'study', 'home', 'market']
        assert [source['key'] for source in locale['sources']] == ['A', 'B', 'C']
        assert [connector['key'] for connector in locale['connectors']] == ['gmail', 'drive', 'notion']
        assert len(locale['steps']) == 4 and len(locale['checks']) == 4
        for source, expected_times in zip(locale['sources'], (('18:00',), ('09:00', '20:00'), ('21:00',))):
            for time in expected_times:
                assert time in source['text'], (source['key'], time)
                assert time in locale['example'], 'Prepared answer lost a source time'
        assert '16:00' not in locale['example'], 'Do not invent a check-in time'
        assert len(locale['firstPrompt']) < 150, 'The first request must stay short'
    # These two products deliberately move in opposite directions and use different units.
    stock, futures = data['market']['stock'], data['market']['futures']
    assert stock['unitKey'] == 'shares' and futures['unitKey'] == 'contracts'
    assert stock['values'][1] - stock['values'][0] == 3000
    assert (stock['values'][1] / stock['values'][0] - 1) * 100 == 25
    assert futures['values'][1] - futures['values'][0] == -40
    assert (futures['values'][1] / futures['values'][0] - 1) * 100 == -12.5
    assert data['quiz']['answer'] == 'まみれ'
    assert len(set(data['quiz']['options'])) == 4
    assert 'だらけ' not in data['quiz']['options'], 'Avoid a plausible second completion of 汗（ ）'
    assert min(data['home']['temperatures']) < data['home']['threshold'] <= max(data['home']['temperatures'])
    required = {'showcase', 'principles', 'classroom', 'takeaway', 'copy-initial', 'learner-followup', 'copy-followup', 'learner-result', 'practice-mode', 'copy-record', 'download-record'}
    for relative in ('index.html', 'en/index.html'):
        parser = SeminarPage()
        source = (ROOT / relative).read_text(encoding='utf-8')
        parser.feed(source)
        assert json.loads(''.join(parser.json_text)) == data, relative + ': embedded JSON drift'
        assert required <= parser.ids, relative + ': incomplete single exercise'
        assert parser.demos == ['travel', 'study', 'home', 'market']
        assert parser.inputs == {'learner-followup': '', 'learner-result': ''}, 'Never prefill a learner answer as their work'
        assert 'script.js?' not in source, 'Do not load the earlier route-selection script'
        assert 'route-phone' not in source and 'route-computer' not in source
    print('PASS seminar: one 60-minute sequence; four projects, three connectors, one four-step exercise')
    print('PASS seminar bilingual source: identical keys, embedded data, facts, and blank learner fields')
    print('PASS seminar checks: unknown check-in, distinct deadlines, stock +25%, futures -12.5%, unique quiz completion')

if __name__ == '__main__':
    validate()
