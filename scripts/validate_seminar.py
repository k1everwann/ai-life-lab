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
        self.links = []
        self.preview_sandbox = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get('id'):
            self.ids.add(a['id'])
        if tag == 'a':
            self.links.append(a.get('href', ''))
        if tag == 'iframe' and a.get('id') == 'checklist-preview':
            self.preview_sandbox = a.get('sandbox')
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
    course = json.loads((ROOT / 'course-content.json').read_text(encoding='utf-8'))
    assert [row['minutes'] for row in course['schedule']] == [8, 24, 12, 13, 3]
    assert shape(course['locales']['zh-Hant']) == shape(course['locales']['en'])
    for locale in course['locales'].values():
        assert len(locale['outcomes']) == 3
        assert [lesson['key'] for lesson in locale['lessons']] == ['gmail', 'drive', 'notion']
        assert [lesson['practiceAnswer'] for lesson in locale['lessons']] == [1, 2, 0]
        for lesson in locale['lessons']:
            assert len(lesson['steps']) == 4 and len(lesson['practiceChoices']) == 3
            assert lesson['prompt'] and lesson['example'] and lesson['check']
        assert '10:00' in locale['sourceD']['text'] and '20:00' in locale['sourceD']['text']
        assert '09:00' in locale['lessons'][1]['example'] and '10:00' in locale['lessons'][1]['example']
        choices = locale['mistakeExercise']['choices']
        assert {choice['key'] for choice in choices if choice['correct']} == {'ticket', 'checkin'}
        assert len(locale['continueSteps']) == 3
    curriculum = json.loads((ROOT / 'curriculum-content.json').read_text(encoding='utf-8'))
    required = {'course-map', 'continue', 'takeaway', 'download-all-records', 'code-M08', 'code-M09', 'preview-M08', 'preview-M09'} | {item['anchor'] for item in curriculum['modules']}
    for relative in ('index.html', 'en/index.html'):
        parser = SeminarPage()
        source = (ROOT / relative).read_text(encoding='utf-8')
        parser.feed(source)
        assert required <= parser.ids, relative + ': incomplete modular course'
        assert parser.demos == [], 'Project demonstrations belong to the live talk, not the lesson website'
        assert 'showcase' not in json.loads(source.split('<script id="curriculum-data" type="application/json">')[1].split('</script>')[0])
        assert 'sandbox="allow-scripts"' in source and 'allow-same-origin' not in source, 'Keep code previews isolated'
        assert not any('instructor.html' in link or 'next-steps.html' in link for link in parser.links), 'The main lesson must not send learners to a separate instructor or continuation page'
        assert 'script.js?' not in source, 'Do not load the earlier route-selection script'
        assert 'route-phone' not in source and 'route-computer' not in source
    print('PASS course: one bilingual modular page with all lesson anchors and isolated code previews')
    print('PASS seminar bilingual source: identical keys and established fictional facts')
    print('PASS seminar checks: unknown check-in, distinct deadlines, stock +25%, futures -12.5%, unique quiz completion')

if __name__ == '__main__':
    validate()
