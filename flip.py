import io

def flip_css(c):
    # Hexagon margin
    c = c.replace('margin-right: -10px;', 'margin-left: -10px;')
    
    # Body wrap clip-path (chamfer top-left and bottom-left)
    old_wrap = 'clip-path: polygon(0 0, calc(100% - 15px) 0, 100% 15px, 100% 100%, 0 100%);'
    new_wrap = 'clip-path: polygon(15px 0, 100% 0, 100% 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);'
    c = c.replace(old_wrap, new_wrap)
    
    # Body wrap padding
    c = c.replace('padding: 2px 2px 2px 0;', 'padding: 2px 0 2px 2px;')
    
    # Body clip-path (chamfer top-left and bottom-left)
    old_body = 'clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);'
    new_body = 'clip-path: polygon(14px 0, 100% 0, 100% 100%, 14px 100%, 0 calc(100% - 14px), 0 14px);'
    c = c.replace(old_body, new_body)
    
    # Body padding
    c = c.replace('padding: 8px 15px 8px 30px;', 'padding: 8px 30px 8px 15px;')
    
    return c

for file in ['d:/GitHub/TGBot/templates/login.html', 'd:/GitHub/TGBot/static/login_concepts_demo.html']:
    with io.open(file, 'r', encoding='utf-8') as f:
        c = f.read()
    c = flip_css(c)
    with io.open(file, 'w', encoding='utf-8') as f:
        f.write(c)

print('SUCCESS')
