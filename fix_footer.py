import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Hide footer for swiss_minimal
c = c.replace("{% if active_style == 'neumorphic_3d' %}style=\"display: none !important;\"{% endif %}", "{% if active_style in ['neumorphic_3d', 'swiss_minimal'] %}style=\"display: none !important;\"{% endif %}")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FOOTER HIDDEN")
