import io

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

old_user = """<div class="neo-track">
                <div class="neo-raised-btn">
                    <i class="fas fa-user"></i>
                </div>
                <input type="text" class="neo-input font-monospace" placeholder="نام کاربری |" style="direction: rtl; text-align: left;">
            </div>"""

new_user = """<div class="neo-track">
                <div class="neo-raised-btn"><i class="fas fa-user"></i></div>
                <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                    <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">نام کاربری</span>
                    <input type="text" class="neo-input px-0 font-monospace" placeholder="username" style="text-align: left;">
                </div>
                <i class="fas fa-id-badge" style="color: #64748b; margin-right: 15px; opacity: 0.5;"></i>
            </div>"""

c = c.replace(old_user, new_user)

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED DEMO")
