"""Fix remaining typos and formatting issues in Phase Field paper."""
filepath = "G:/Xiaogan_Supercomputing_data/SCX/papers/scx_phase_field/main.md"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()
changes = []
# Fix f_S definition at line 123: \\frac{2} -> \\frac{\\alpha}{2} and \\frac{4} -> \\frac{\\beta}{4}
old = "f_S(\\Sf) = \\frac{2} (\\Sf - \\Sf_0)^2 + \\frac{4} \\Sf^4"
new = "f_S(\\Sf) = \\frac{\\alpha}{2} (\\Sf - \\Sf_0)^2 + \\frac{\\beta}{4} \\Sf^4"
if old in content:
    content = content.replace(old, new)
    changes.append("f_S definition: restored alpha and beta coefficients")
else:
    # Debug: hex dump of the area
    idx = content.find('\\frac{2} (\\Sf')
    if idx >= 0:
        print(f"Found at {idx}: {repr(content[idx-10:idx+40])}")
# Fix coupling term consistency: Gamma(gf, Sf) -> lambda*||gf||^2*Sf
old_gamma = "\\lambda \\, \\Gamma(\\gf, \\Sf)"
new_gamma = "\\lambda \\, \\|\\gf\\|^2 \\Sf"
# Actually Gamma might be intentional as a general term. Let me check...
# Leave Gamma for now as it's defined as coupling functional
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
for c in changes:
    print(f"[FIX] {c}")
if not changes:
    print("No changes")
