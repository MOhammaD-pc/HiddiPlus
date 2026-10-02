import io

def fix_captcha_filter(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()
    
    old_filter = 'filter: contrast(1.5) sepia(1) hue-rotate(330deg) saturate(3);'
    new_filter = 'filter: invert(1) sepia(1) saturate(5) hue-rotate(350deg) brightness(1.2) contrast(1.2);'
    c = c.replace(old_filter, new_filter)
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

fix_captcha_filter('d:/GitHub/TGBot/templates/login.html')
fix_captcha_filter('d:/GitHub/TGBot/static/login_concepts_demo.html')

print("SUCCESS")
