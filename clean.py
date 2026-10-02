import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# I will use a regex to strip out the old block
# Look for /* ۶. سه‌بعدی نئومورفیک (neumorphic_3d) */ down to just before /* NEUMORPHIC 3D RE-IMPLEMENTATION */
c = re.sub(r"/\* ۶\. سه‌بعدی نئومورفیک \(neumorphic_3d\) \*/.*?/\* NEUMORPHIC 3D RE-IMPLEMENTATION \*/", "/* NEUMORPHIC 3D RE-IMPLEMENTATION */", c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
