import io
with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()
start = c.find('<form method="POST"')
end = c.find('</form>') + 7
with io.open('form.txt', 'w', encoding='utf-8') as f:
    f.write(c[start:end])
print("SUCCESS")
