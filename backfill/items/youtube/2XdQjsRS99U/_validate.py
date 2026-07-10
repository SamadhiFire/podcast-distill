import re, json

# Read transcript
with open(r'd:/Users/AS/Desktop/podcast-distill/backfill/items/youtube/2XdQjsRS99U/transcript.txt', 'r', encoding='utf-8') as f:
    transcript = f.read()

# Extract allowed numbers from transcript
pattern = re.compile(r'(?<![A-Za-z])\$?\d[\d,]*(?:\.\d+)?%?')
raw_matches = pattern.findall(transcript)
allowed = set()
for m in raw_matches:
    cleaned = m.replace(',', '').replace('$', '')
    allowed.add(cleaned)

print(f'Total allowed numbers: {len(allowed)}')
print(f'Sample large: {sorted([x for x in allowed if len(x) > 2])[:40]}')

# Read summary
with open(r'd:/Users/AS/Desktop/podcast-distill/backfill/items/youtube/2XdQjsRS99U/summary.json', 'r', encoding='utf-8') as f:
    summary = json.load(f)

# Extract digit sequences from all digest string fields
def extract_from_text(text):
    matches = pattern.findall(text)
    return [m.replace(',', '').replace('$', '') for m in matches]

# Check key_facts value + context
issues = []
for i, kf in enumerate(summary['digest']['key_facts']):
    for field in ['value', 'context']:
        digits = extract_from_text(kf[field])
        for d in digits:
            if d not in allowed:
                issues.append(f'key_fact[{i}].{field}: "{d}" from "{kf[field]}" NOT in allowed set')

# Check summary paragraphs
for i, para in enumerate(summary['digest']['summary']):
    digits = extract_from_text(para)
    for d in digits:
        if d not in allowed:
            issues.append(f'summary[{i}]: "{d}" NOT in allowed set')

# Check core_points
for i, cp in enumerate(summary['digest']['core_points']):
    digits = extract_from_text(cp)
    for d in digits:
        if d not in allowed:
            issues.append(f'core_point[{i}]: "{d}" NOT in allowed set')

# Check other fields
for field in ['short_title', 'one_liner', 'why_it_matters']:
    digits = extract_from_text(summary['digest'][field])
    for d in digits:
        if d not in allowed:
            issues.append(f'{field}: "{d}" NOT in allowed set')

for i, ta in enumerate(summary['digest']['takeaways']):
    digits = extract_from_text(ta)
    for d in digits:
        if d not in allowed:
            issues.append(f'takeaway[{i}]: "{d}" NOT in allowed set')

for i, te in enumerate(summary['digest']['tensions']):
    digits = extract_from_text(te)
    for d in digits:
        if d not in allowed:
            issues.append(f'tension[{i}]: "{d}" NOT in allowed set')

if issues:
    print('ISSUES FOUND:')
    for issue in issues:
        print(f'  - {issue}')
else:
    print('ALL NUMBERS VALIDATED SUCCESSFULLY')
