import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('<div class="position-relative mb-4">', '<div class="position-relative mb-4" dir="ltr">')
c = c.replace('<div class="position-relative mb-5">', '<div class="position-relative mb-5" dir="ltr">')
c = c.replace('<div class="position-relative mb-5" style="margin-top: 30px;">', '<div class="position-relative mb-5" style="margin-top: 30px;" dir="ltr">')

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
    
print("SUCCESS")
