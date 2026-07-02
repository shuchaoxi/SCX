#!/usr/bin/env python3
"""Fix REX block in Monte Carlo paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_monte_carlo/main.md"

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Fix the \tau character (single backslash vs double)
# The file has a stray \t before \tau
content = content.replace(
    "    \\tau_{mix}^{REX}(T_1)",
    "    \\\\tau_{mix}^{REX}(T_1)"
)

# Fix double $$
count = content.count("$$\n$$\n")
print(f"Found {count} instances of double $$")
content = content.replace(
    "$$\n$$\n\n",
    "$$\n\n"
)

# Make sure tau is correct in the formula
# Replace any remaining single-backslash tau
content = content.replace(
    "    \tau_{mix}^{REX}(T_1)",
    "    \\\\tau_{mix}^{REX}(T_1)"
)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("REX block fixed")

# Verify
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()
for i, line in enumerate(lines):
    if 'rex_mixing_time' in line or 'REX 的混合加速' in line or 'tau_{mix}' in line:
        print(f"Line {i+1}: {line.rstrip()}")
