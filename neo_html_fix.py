import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. First, remove the injected `neo-wrapper` from the top of the form, and the footer from the bottom.
# It looks like:
# {% if active_style == 'neumorphic_3d' %}
# <div class="neo-wrapper" dir="ltr">
#     ...
# {% endif %}

c = re.sub(
    r"{% if active_style == 'neumorphic_3d' %}\s*<div class=\"neo-wrapper\".*?{% endif %}",
    "",
    c,
    flags=re.DOTALL,
    count=1
)

# Also remove the footer injection
c = re.sub(
    r"{% if active_style == 'neumorphic_3d' %}\s*<div class=\"text-center\" style=\"margin-top: 30px; font-size: 0\.85rem; color: #64748b;\">\s*<div class=\"mb-2 cursor-pointer\">فراموشی رمز؟</div>.*?{% endif %}",
    "",
    c,
    flags=re.DOTALL,
    count=1
)

# 2. Now let's inject the `neo-wrapper` wrapping just inside the form?
# No, let's wrap the entire form body in `neo-wrapper` if active_style == 'neumorphic_3d', OR we can just add `neo-wrapper` class to `login-main-card` for neumorphic_3d!
# Actually, the user's screenshot has `neo-wrapper` design. Let's just put `neo-wrapper` inside the card body.

# Let's write the updated logic for the card-body:
# Right after: <form method="POST" autocomplete="on" id="mainLoginForm">
# We insert:
neo_header = """                    {% if active_style == 'neumorphic_3d' %}
                    <div class="neo-wrapper" dir="ltr">
                        <div class="neo-header">
                            <div class="neo-logo-icon">
                                {% if branding.get('logo_url') %}
                                    <img src="{{ branding.get('logo_url') }}" alt="لوگو" style="max-height: 40px; max-width: 40px; object-fit: contain;">
                                {% else %}
                                    <i class="fas fa-cube"></i>
                                {% endif %}
                            </div>
                            <h4 style="font-weight: 600; font-size: 1.3rem; margin-bottom: 5px; color: #e2e8f0;">{{ branding.get('login_page_title') or 'TGBot' }}</h4>
                            <div style="font-size: 0.9rem; color: #64748b;">{{ login_page_subtitle or 'ورود به حساب کاربری' }}</div>
                        </div>
                    {% endif %}
"""
c = c.replace('<form method="POST" autocomplete="on" id="mainLoginForm">', '<form method="POST" autocomplete="on" id="mainLoginForm">\n' + neo_header)


# 3. Inject username field for neumorphic_3d
neo_user = """                        {% elif active_style == 'neumorphic_3d' %}
                        <div class="neo-track">
                            <div class="neo-raised-btn"><i class="fas fa-user"></i></div>
                            <input type="text" class="neo-input font-monospace" name="username" placeholder="نام کاربری |" style="direction: rtl; text-align: left;" required autofocus>
                            <i class="fas fa-user" style="color: transparent; margin-right: 15px; pointer-events: none;"></i>
                        </div>"""
c = c.replace("{% elif active_style == 'swiss_minimal' %}", neo_user + "\n                        {% elif active_style == 'swiss_minimal' %}", 1)


# 4. Inject password field
neo_pass = """                        {% elif active_style == 'neumorphic_3d' %}
                        <div class="neo-track">
                            <div class="neo-raised-btn"><i class="fas fa-lock"></i></div>
                            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                                <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">رمز عبور</span>
                                <input type="password" class="neo-input px-0 font-monospace" name="password" id="loginPasswordInput" placeholder="••••••••" style="text-align: left;" required>
                            </div>
                            <i class="fas fa-eye-slash" id="passwordToggleIcon" style="color: #64748b; margin-right: 15px; cursor: pointer;" onclick="togglePasswordVisibility()"></i>
                        </div>"""
# Find the second swiss_minimal (which is for password)
c = c.replace("{% elif active_style == 'swiss_minimal' %}", neo_pass + "\n                        {% elif active_style == 'swiss_minimal' %}", 1)


# 5. Inject captcha field
neo_captcha = """                        {% elif active_style == 'neumorphic_3d' %}
                        <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                            <div class="neo-track" style="flex-grow: 1; position: relative; margin: 0; overflow: hidden; padding: 0;">
                                <div style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; mix-blend-mode: multiply; opacity: 0.7; filter: contrast(1.5); cursor: pointer;" onclick="refreshCaptcha()">
                                    <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" style="width: 100%; height: 100%; object-fit: cover;">
                                </div>
                                <input type="text" inputmode="numeric" pattern="[0-9]*" class="neo-input font-monospace text-center" name="captcha" id="captchaInputField" style="position: relative; width: 100%; height: 100%; font-size: 2rem; letter-spacing: 1.2rem; font-weight: bold; text-shadow: -1px -1px 2px rgba(255,255,255,0.1), 1px 1px 2px rgba(0,0,0,0.8); background: transparent; padding-left: 1.2rem;" placeholder="     " required autocomplete="off" maxlength="5">
                            </div>
                            <div class="neo-raised-btn" style="width: 64px; height: 64px; border-radius: 50%; margin: 0; cursor: pointer;" onclick="refreshCaptcha()">
                                <i class="fas fa-redo"></i>
                            </div>
                        </div>"""
# Find the third swiss_minimal (which is for captcha)
c = c.replace("{% elif active_style == 'swiss_minimal' %}", neo_captcha + "\n                        {% elif active_style == 'swiss_minimal' %}", 1)


# 6. Inject submit button text
# We need to replace the submit button inner HTML. Right now it is:
# {% elif active_style == 'swiss_minimal' %} <div class="w-100 bg-white...
neo_submit = """                        {% elif active_style == 'neumorphic_3d' %}
                            <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="font-weight: 700; font-size: 1.1rem;">
                                ورود به حساب کاربری
                            </div>"""
c = c.replace("{% elif active_style == 'swiss_minimal' %}", neo_submit + "\n                        {% elif active_style == 'swiss_minimal' %}", 1)

# We also need to add neo-submit class to the submit button
# The submit button is <button type="submit" class="btn w-100 py-2 fw-bold login-submit-btn ...
# We will do this in CSS instead by targeting .login-theme-neumorphic_3d .login-submit-btn


# 7. Close the neo-wrapper at the end of the form
c = c.replace("</form>", "                    {% if active_style == 'neumorphic_3d' %}</div>{% endif %}\n                </form>")

# 8. Hide card footer for neumorphic_3d
# It looks like: <div class="card-footer login-card-footer text-center py-3 border-0">
c = c.replace('<div class="card-footer login-card-footer text-center py-3 border-0">', '<div class="card-footer login-card-footer text-center py-3 border-0" {% if active_style == \'neumorphic_3d\' %}style="display: none !important;"{% endif %}>')

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
