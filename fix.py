import io

def fix_login(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Hide theme toggle for stealth_tactical
    c = c.replace("{% if active_style != 'hacker_terminal' %}", "{% if active_style not in ['hacker_terminal', 'stealth_tactical'] %}")
    
    # Remove 'تغییر تصویر' text next to captcha
    c = c.replace('<i class="fas fa-rotate me-1"></i>تغییر تصویر', '<i class="fas fa-rotate fs-6"></i>')
    
    # Remove background toggler if exists (I didn't see one but just in case)
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

fix_login('d:/GitHub/TGBot/templates/login.html')

print("SUCCESS")
