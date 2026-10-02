import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Fix the CSS for the button
old_btn_css = """.login-theme-swiss_minimal .login-submit-btn,
.login-theme-nordic_studio .login-submit-btn,
.login-theme-minimal_luxury .login-submit-btn {
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 13px !important;
    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.15);
}"""

new_btn_css = """.login-theme-nordic_studio .login-submit-btn,
.login-theme-minimal_luxury .login-submit-btn {
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: 800 !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 13px !important;
    box-shadow: 0 4px 15px rgba(255, 255, 255, 0.15);
}
.login-theme-swiss_minimal .login-submit-btn {
    background: #ffffff !important;
    color: #000000 !important;
    font-weight: 400 !important;
    font-family: -apple-system, sans-serif !important;
    border: none !important;
    border-radius: 0 !important;
    padding: 14px !important;
    box-shadow: none !important;
}"""
c = c.replace(old_btn_css, new_btn_css)

# Fix the inner html
old_inner = """{% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 400; padding: 12px 0;">
                                ورود
                            </div>"""

new_inner = """{% elif active_style == 'swiss_minimal' %}
                            <span style="font-size: 1.15rem;">ورود</span>"""
c = c.replace(old_inner, new_inner)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED BTN")
