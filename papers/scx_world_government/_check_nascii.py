import re
with open('world_government.tex', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Check for lines with non-ASCII content
for i, line in enumerate(lines, 1):
    # strip ASCII
    non_ascii = ''.join(c for c in line if ord(c) > 127)
    if non_ascii:
        print(f"Line {i}: {repr(non_ascii[:80])}")
