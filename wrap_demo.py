import io
with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()
c = c.replace('id="tab-swiss" dir="rtl"', 'id="tab-swiss" dir="ltr"')
with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("SUCCESS")
