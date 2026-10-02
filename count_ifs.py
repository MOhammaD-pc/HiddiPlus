import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

lines = c.split('\n')
stack = []
for i, line in enumerate(lines):
    # simple heuristic: count matches
    ifs = len(re.findall(r'{%-?\s*if\s+', line))
    endifs = len(re.findall(r'{%-?\s*endif\s*', line))
    if ifs > endifs:
        for _ in range(ifs - endifs):
            stack.append(i + 1)
    elif endifs > ifs:
        for _ in range(endifs - ifs):
            if stack:
                stack.pop()
            else:
                print(f"Extra endif at line {i+1}")

if stack:
    print(f"Unclosed if statements from lines: {stack}")
else:
    print("Perfect match!")
