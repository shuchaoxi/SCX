import re

pattern = re.compile(r'[\u4e00-\u9fff]+')

files = [
    'theory/self_evolution/spring_convergence_analysis.tex',
    'theory/theorems/01_noise_detection_guarantee.tex',
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as fh:
        content = fh.read()
    matches = pattern.findall(content)
    for m in matches:
        # Find context (surrounding 40 chars)
        for i, line in enumerate(content.split('\n')):
            if m in line:
                print(f'{fpath} line {i+1}: fragment=[{m}]')
                print(f'  context: ...{line[max(0,line.find(m)-20):line.find(m)+len(m)+20]}...')
                print()
