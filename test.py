import io
with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()
i1 = c.find('/* ─── استایل ۴:')
i2 = c.find('/* ─── استایل ۵:')
print(i1, i2)
