import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace("class='text-start mt-5'", "class='text-start mt-5' dir='ltr' style='text-align: left !important;'")
c = c.replace("class='text-start mb-2'", "class='text-start mb-2' dir='ltr' style='text-align: left !important;'")
c = c.replace('class="text-start mt-2"', 'class="text-start mt-2" dir="ltr" style="text-align: left !important;"')

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
