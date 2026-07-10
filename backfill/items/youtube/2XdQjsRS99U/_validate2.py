import json

with open(r'd:/Users/AS/Desktop/podcast-distill/backfill/items/youtube/2XdQjsRS99U/summary.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

dig = d['digest']
issues = []

def check(name, val, maxlen):
    if len(val) > maxlen:
        issues.append(f'{name}: {len(val)} chars > {maxlen} max')

check('short_title', dig['short_title'], 18)
check('one_liner', dig['one_liner'], 30)
check('why_it_matters', dig['why_it_matters'], 60)

for i, p in enumerate(dig['summary']):
    check(f'summary[{i}]', p, 150)

for i, cp in enumerate(dig['core_points']):
    check(f'core_point[{i}]', cp, 90)

for i, kf in enumerate(dig['key_facts']):
    check(f'key_fact[{i}].label', kf['label'], 18)
    check(f'key_fact[{i}].value', kf['value'], 36)
    check(f'key_fact[{i}].context', kf['context'], 90)

for i, ta in enumerate(dig['takeaways']):
    check(f'takeaway[{i}]', ta, 70)
    if '?' in ta or '\uff1f' in ta:
        issues.append(f'takeaway[{i}]: contains question mark')

for i, g in enumerate(dig['guests']):
    check(f'guest[{i}]', g, 90)

for i, t in enumerate(dig['topics']):
    check(f'topic[{i}]', t, 12)

for i, te in enumerate(dig['tensions']):
    check(f'tension[{i}]', te, 90)

# Check counts
if not (2 <= len(dig['summary']) <= 6):
    issues.append(f'summary count: {len(dig["summary"])} not in 2-6')
if not (3 <= len(dig['core_points']) <= 7):
    issues.append(f'core_points count: {len(dig["core_points"])} not in 3-7')
if len(dig['key_facts']) > 8:
    issues.append(f'key_facts count: {len(dig["key_facts"])} > 8')
if not (1 <= len(dig['takeaways']) <= 2):
    issues.append(f'takeaways count: {len(dig["takeaways"])} not in 1-2')
if len(dig['guests']) > 5:
    issues.append(f'guests count: {len(dig["guests"])} > 5')
if len(dig['topics']) > 3:
    issues.append(f'topics count: {len(dig["topics"])} > 3')
if len(dig['tensions']) > 3:
    issues.append(f'tensions count: {len(dig["tensions"])} > 3')
if not (1 <= dig['importance_score'] <= 5):
    issues.append(f'importance_score: {dig["importance_score"]} not in 1-5')
if dig['content_density'] not in ('brief', 'standard', 'high'):
    issues.append(f'content_density: {dig["content_density"]} invalid')

# Check CJK presence in Chinese fields
import re
cjk_pattern = re.compile(r'[\u4e00-\u9fff]')
for field in ['short_title', 'one_liner', 'why_it_matters']:
    if not cjk_pattern.search(dig[field]):
        issues.append(f'{field}: no CJK characters')
for i, p in enumerate(dig['summary']):
    if not cjk_pattern.search(p):
        issues.append(f'summary[{i}]: no CJK characters')
for i, cp in enumerate(dig['core_points']):
    if not cjk_pattern.search(cp):
        issues.append(f'core_point[{i}]: no CJK characters')
for i, ta in enumerate(dig['takeaways']):
    if not cjk_pattern.search(ta):
        issues.append(f'takeaway[{i}]: no CJK characters')
for i, t in enumerate(dig['topics']):
    if not cjk_pattern.search(t):
        issues.append(f'topic[{i}]: no CJK characters')
for i, te in enumerate(dig['tensions']):
    if not cjk_pattern.search(te):
        issues.append(f'tension[{i}]: no CJK characters')

# Check no markdown
md_pattern = re.compile(r'(\*\*|```|<[^>]+>)')
for field in ['short_title', 'one_liner', 'why_it_matters']:
    if md_pattern.search(dig[field]):
        issues.append(f'{field}: contains markdown')
for i, p in enumerate(dig['summary']):
    if md_pattern.search(p):
        issues.append(f'summary[{i}]: contains markdown')

if issues:
    print('ISSUES FOUND:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('ALL CONSTRAINTS VALIDATED SUCCESSFULLY')
