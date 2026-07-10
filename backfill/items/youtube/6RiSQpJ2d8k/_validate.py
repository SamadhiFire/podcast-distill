import json, re

with open(r'd:/Users/AS/Desktop/podcast-distill/backfill/items/youtube/6RiSQpJ2d8k/summary.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

d = data['digest']
cjk = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf]')
errors = []

# Check CJK in Chinese fields
for field in ['short_title', 'one_liner', 'why_it_matters']:
    if not cjk.search(d[field]):
        errors.append(f'{field} missing CJK chars')

for i, p in enumerate(d['summary']):
    if not cjk.search(p):
        errors.append(f'summary[{i}] missing CJK chars')

for i, cp in enumerate(d['core_points']):
    if not cjk.search(cp):
        errors.append(f'core_points[{i}] missing CJK chars')

for i, ta in enumerate(d['takeaways']):
    if not cjk.search(ta):
        errors.append(f'takeaways[{i}] missing CJK chars')

for i, t in enumerate(d['topics']):
    if not cjk.search(t):
        errors.append(f'topics[{i}] missing CJK chars')

for i, tn in enumerate(d['tensions']):
    if not cjk.search(tn):
        errors.append(f'tensions[{i}] missing CJK chars')

for i, kf in enumerate(d['key_facts']):
    if not cjk.search(kf['label']):
        errors.append(f'key_facts[{i}].label missing CJK chars')
    if not cjk.search(kf['context']):
        errors.append(f'key_facts[{i}].context missing CJK chars')

if d.get('quote') and d['quote'].get('text'):
    if not cjk.search(d['quote']['text']):
        errors.append('quote.text missing CJK chars')

# Check no markdown
md_pattern = re.compile(r'[*#_~\[\]]')
all_strings = [d['short_title'], d['one_liner'], d['why_it_matters']]
all_strings += d['summary'] + d['core_points'] + d['takeaways'] + d['topics'] + d['tensions']
for kf in d['key_facts']:
    all_strings += [kf['label'], kf['value'], kf['context']]
for s in all_strings:
    if md_pattern.search(s):
        errors.append(f'Possible markdown in: {s[:50]}')

if errors:
    print('ERRORS:')
    for e in errors:
        print(f'  - {e}')
else:
    print('CJK + MARKDOWN CHECK: ALL PASSED')
