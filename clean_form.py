import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Remove the accumulated neumorphic blocks before the first swiss_minimal block
# We know they all start with {% elif active_style == 'neumorphic_3d' %}
c = re.sub(r"({% elif active_style == 'neumorphic_3d' %}.*?)(?={% elif active_style == 'swiss_minimal' %})", "", c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("CLEANED")
