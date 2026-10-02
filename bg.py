import io

def fix_css(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    old_bg = '''    background: #0a0a0a;
    background-image: radial-gradient(#2b3038 1px, transparent 1px), radial-gradient(#2b3038 1px, transparent 1px);'''
    new_bg = '''    background: #0a0a0a url('/static/images/stealth_bg.jpg') no-repeat center center fixed;
    background-size: cover;'''
    
    c = c.replace(old_bg, new_bg)
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

fix_css('d:/GitHub/TGBot/templates/login.html')
fix_css('d:/GitHub/TGBot/static/login_concepts_demo.html')

print("SUCCESS")
