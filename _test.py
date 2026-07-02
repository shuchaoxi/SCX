import os, sys
sys.stdout.reconfigure(encoding='utf-8')
f = 'theory/README.tex'
print(f'Testing: {f}', flush=True)
print(f'Exists: {os.path.exists(f)}', flush=True)
with open(f, 'r', encoding='utf-8') as fh:
    c = fh.read()
print(f'Length: {len(c)}', flush=True)
