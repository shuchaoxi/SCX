import sys
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_phase_field/main.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
changes = []
# Fix f_S definition - add - sign
old1 = "f_S(\\Sf) = \\frac{\\alpha}{2} (\\Sf"
new1 = "f_S(\\Sf) = -\\frac{\\alpha}{2} (\\Sf"
if old1 in content:
    content = content.replace(old1, new1)
    changes.append("f_S: added negative sign")
# Fix chemical potential
old2 = "\\alpha(\\Sf - \\Sf_0) + \\beta \\Sf^3"
new2 = "-\\alpha(\\Sf - \\Sf_0) + \\beta \\Sf^3"
if old2 in content:
    content = content.replace(old2, new2)
    changes.append("mu_S: added negative sign")
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
for c in changes:
    print(f"[FIX] {c}")
if not changes:
    print("No changes")
