import io

def translate_file(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    # Translate stealth_tactical text
    if "login.html" in file_path:
        c = c.replace('<span class="stealth-floating-label">USERNAME</span>', '<span class="stealth-floating-label">شناسه کاربری (OPERATIVE)</span>')
        c = c.replace('<span class="stealth-floating-label">PASSWORD</span>', '<span class="stealth-floating-label">کلید دسترسی (ACCESS KEY)</span>')
        c = c.replace('<span class="stealth-floating-label" style="position: static; font-size: 0.8rem; letter-spacing: 2px;">VERIFICATION CODE</span>', '<span class="stealth-floating-label" style="position: static; font-size: 0.8rem; letter-spacing: 2px;">کد تأیید امنیتی (HUD)</span>')
        c = c.replace('placeholder="[ ENTER CODE ]"', 'placeholder="[ ورود کد ]"')
    else:
        c = c.replace('<span class="stealth-floating-label">USERNAME</span>', '<span class="stealth-floating-label">شناسه کاربری</span>')
        c = c.replace('<span class="stealth-floating-label">PASSWORD</span>', '<span class="stealth-floating-label">کلمه عبور</span>')
        c = c.replace('<span class="stealth-floating-label" style="font-size: 0.8rem; letter-spacing: 2px;">VERIFICATION CODE</span>', '<span class="stealth-floating-label" style="font-size: 0.8rem; letter-spacing: 2px;">کد تأیید امنیتی</span>')
        c = c.replace('placeholder="[ ENTER CODE ]"', 'placeholder="[ کد ۵ رقمی ]"')
    
    # Also fix the absolute right eye icon for RTL -> absolute left
    c = c.replace('right: 15px;', 'left: 15px;')
    c = c.replace('end-0', 'start-0')
    c = c.replace('me-3', 'ms-3')
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

translate_file('d:/GitHub/TGBot/templates/login.html')
translate_file('d:/GitHub/TGBot/static/login_concepts_demo.html')

print("SUCCESS")
