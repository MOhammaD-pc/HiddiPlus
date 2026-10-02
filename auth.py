import io

def fix_auth(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    if "login.html" in file_path:
        c = c.replace('>AUTHORIZE<', '>مجوز دسترسی<')
    else:
        c = c.replace('>AUTHORIZE<', '>مجوز دسترسی<')
        
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

fix_auth('d:/GitHub/TGBot/templates/login.html')
fix_auth('d:/GitHub/TGBot/static/login_concepts_demo.html')

print("SUCCESS")
