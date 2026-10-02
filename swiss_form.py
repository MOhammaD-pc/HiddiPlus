import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# USERNAME
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    "{% elif active_style == 'swiss_minimal' %}\n<div class=\"mb-4 position-relative\">\n    <div class=\"d-flex align-items-center mb-1\" style=\"border-bottom: 1px solid rgba(255,255,255,0.2);\">\n        <span class=\"text-white pe-3 ps-1 pb-1\" style=\"font-size: 0.85rem; letter-spacing: 0.5px;\">Username</span>\n        <div class=\"flex-grow-1\"></div>\n    </div>\n    <div class=\"d-flex align-items-center\" style=\"border-bottom: 2px solid #fff; padding-bottom: 2px;\">\n        <i class=\"far fa-user text-white opacity-75 ms-2 me-3 fs-5\"></i>\n        <input type=\"text\" class=\"form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5\" name=\"username\" placeholder=\"username\" required autofocus style=\"direction: ltr; text-align: left;\">\n    </div>\n</div>\n{% else %}",
    c, count=1, flags=re.DOTALL
)

# PASSWORD
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    "{% elif active_style == 'swiss_minimal' %}\n<div class=\"mb-5 position-relative\">\n    <div class=\"d-flex align-items-center mb-1\" style=\"border-bottom: 1px solid rgba(255,255,255,0.2);\">\n        <span class=\"text-white pe-3 ps-1 pb-1\" style=\"font-size: 0.85rem; letter-spacing: 0.5px;\">Password</span>\n        <div class=\"flex-grow-1\"></div>\n    </div>\n    <div class=\"d-flex align-items-center\" style=\"border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 2px;\">\n        <i class=\"fas fa-lock text-white opacity-50 ms-2 me-3 fs-5\"></i>\n        <input type=\"password\" name=\"password\" id=\"loginPasswordInput\" class=\"form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5\" placeholder=\"••••••••\" required style=\"direction: ltr; text-align: left;\">\n    </div>\n</div>\n{% else %}",
    c, count=1, flags=re.DOTALL
)

# CAPTCHA
old_cap = """{% elif active_style == 'stealth_tactical' %}"""
new_cap = """{% elif active_style == 'swiss_minimal' %}
<div class="mb-5 position-relative">
    <div class="d-flex align-items-center justify-content-between mb-3 px-2">
        <div class="captcha-img-box flex-grow-1 mx-2" style="height: 55px; filter: invert(1) grayscale(1) brightness(2) contrast(3);">
            <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: contain;">
        </div>
        <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none" onclick="refreshCaptcha()">
            <i class="fas fa-rotate-right fs-4"></i>
        </button>
    </div>
    <div class="d-flex align-items-center">
        <input type="text" inputmode="numeric" pattern="[0-9]*" class="form-control bg-transparent border-0 text-white shadow-none text-center font-monospace px-0" name="captcha" id="captchaInputField" placeholder="     " maxlength="5" autocomplete="off" required style="font-size: 2rem; letter-spacing: 1.5rem; background-image: repeating-linear-gradient(to right, rgba(255,255,255,0.3) 0, rgba(255,255,255,0.3) 30px, transparent 30px, transparent 50px); background-size: 260px 1px; background-position: bottom center; background-repeat: no-repeat; padding-bottom: 5px;">
    </div>
    <div class="text-start mt-2 px-3">
        <span class="text-white opacity-50" style="font-size: 0.75rem;">Captcha Code</span>
    </div>
</div>
{% elif active_style == 'stealth_tactical' %}"""
c = c.replace(old_cap, new_cap)

# SUBMIT BUTTON
old_btn = """{% elif active_style == 'swiss_minimal' %}
                            <span>ورود</span>
                            <i class="fas fa-arrow-left"></i>
                        {% else %}"""
new_btn = """{% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black py-2 d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-weight: 500;">
                                Sign In
                            </div>
                        {% else %}"""
c = c.replace(old_btn, new_btn)

# Remove the default label rendering for swiss_minimal in username and password by hiding it if it shows up
c = c.replace("{% if active_style == 'swiss_minimal' %}\n                                <span>نام کاربری:</span>", "{% if active_style == 'swiss_minimal' %}\n                                <span class='d-none'>نام کاربری:</span>")
c = c.replace("{% if active_style == 'swiss_minimal' %}\n                                  <span>رمز عبور:</span>", "{% if active_style == 'swiss_minimal' %}\n                                  <span class='d-none'>رمز عبور:</span>")
c = c.replace("{% elif active_style == 'swiss_minimal' %}\n                                      <span>کد امنیتی:</span>", "{% elif active_style == 'swiss_minimal' %}\n                                      <span class='d-none'>کد امنیتی:</span>")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("SUCCESS")
