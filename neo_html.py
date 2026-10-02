import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# I need to wrap the contents of login-main-card with .neo-wrapper for neumorphic_3d
# Or just put the header inside the form for neumorphic_3d.

# Let's insert the neumorphic custom header just before the form
# Actually, the existing header is hidden by `.login-theme-neumorphic_3d .login-card-header { display: none !important; }`
# I'll add the new header inside the form.

form_start = '<form method="POST" autocomplete="on" id="mainLoginForm">'
neo_form_start = """<form method="POST" autocomplete="on" id="mainLoginForm">
                    {% if active_style == 'neumorphic_3d' %}
                    <div class="neo-wrapper" dir="ltr">
                        <div class="neo-header">
                            <div class="neo-logo-icon">
                                <i class="fas fa-cube"></i>
                            </div>
                            <h4 style="font-weight: 600; font-size: 1.3rem; margin-bottom: 5px; color: #e2e8f0;">NEXUS</h4>
                            <div style="font-size: 1.15rem; font-weight: 500; margin-bottom: 5px;">ورود به حساب کاربری</div>
                            <div style="font-size: 0.9rem; color: #64748b;">خوش آمدید</div>
                        </div>
                    {% endif %}
"""
c = c.replace(form_start, neo_form_start)

# USERNAME field
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    """{% elif active_style == 'swiss_minimal' %}
                        <div class="position-relative mb-4">
                            <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">نام کاربری</span>
                                <div class="flex-grow-1"></div>
                            </div>
                            <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left;">
                            </div>
                        </div>
                        {% elif active_style == 'neumorphic_3d' %}
                        <div class="neo-track">
                            <div class="neo-raised-btn">
                                <i class="fas fa-user"></i>
                            </div>
                            <input type="text" class="neo-input font-monospace" name="username" placeholder="نام کاربری |" required autofocus style="direction: rtl; text-align: left;">
                        </div>
                        {% else %}""",
    c, count=1, flags=re.DOTALL
)

# PASSWORD field
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    """{% elif active_style == 'swiss_minimal' %}
                        <div class="position-relative mb-5">
                            <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">رمز عبور</span>
                                <div class="flex-grow-1"></div>
                            </div>
                            <div class="d-flex align-items-center" style="border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 2px;">
                                <i class="fas fa-lock text-white opacity-50 ms-2 me-3 fs-5"></i>
                                <input type="password" name="password" id="loginPasswordInput" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" placeholder="••••••••" required style="direction: ltr; text-align: left;">
                            </div>
                        </div>
                        {% elif active_style == 'neumorphic_3d' %}
                        <div class="neo-track">
                            <div class="neo-raised-btn">
                                <i class="fas fa-lock"></i>
                            </div>
                            <div class="flex-grow-1 d-flex flex-column justify-content-center px-3" style="direction: ltr;">
                                <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">رمز عبور</span>
                                <input type="password" name="password" id="loginPasswordInput" class="neo-input px-0 font-monospace" placeholder="••••••••" required style="text-align: left;">
                            </div>
                            <i class="fas fa-eye-slash" style="color: #64748b; margin-right: 15px; cursor: pointer;" onclick="togglePasswordVisibility()" id="passwordToggleIcon"></i>
                        </div>
                        {% else %}""",
    c, count=1, flags=re.DOTALL
)

# CAPTCHA field
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    """{% elif active_style == 'swiss_minimal' %}
                        <div class="position-relative mb-5" style="margin-top: 30px;">
                            <div class="d-flex align-items-center justify-content-between mb-2 px-2">
                                <div class="captcha-img-box flex-grow-1 mx-3" style="height: 55px; filter: invert(1) grayscale(1) brightness(3) contrast(3); cursor: pointer;" onclick="refreshCaptcha()">
                                    <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: contain;">
                                </div>
                                <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none" onclick="refreshCaptcha()">
                                    <i class="fas fa-rotate-right fs-4" style="font-weight: 300;"></i>
                                </button>
                            </div>
                            <div class="d-flex align-items-center px-2">
                                <input type="text" inputmode="numeric" pattern="[0-9]*" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none text-center font-monospace px-0" name="captcha" id="captchaInputField" placeholder="     " maxlength="5" autocomplete="off" required style="font-size: 2.2rem; letter-spacing: 1.8rem; background-image: repeating-linear-gradient(to left, transparent 0, transparent 15px, rgba(255,255,255,0.3) 15px, rgba(255,255,255,0.3) 55px); background-size: 55px 1px; background-position: bottom center; background-repeat: repeat-x; padding-bottom: 5px; direction: ltr;">
                            </div>
                            <div class="text-start mt-2">
                                <span class="text-white opacity-50" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">شناسه امنیتی (Captcha)</span>
                            </div>
                        </div>
                        {% elif active_style == 'neumorphic_3d' %}
                        <div class="d-flex gap-3 mb-4">
                            <div class="neo-track flex-grow-1 position-relative m-0" style="overflow: hidden; padding: 0;">
                                <div class="position-absolute w-100 h-100 top-0 start-0" style="mix-blend-mode: multiply; opacity: 0.7; filter: contrast(1.5);">
                                    <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100" style="object-fit: cover; cursor: pointer;" onclick="refreshCaptcha()">
                                </div>
                                <input type="text" inputmode="numeric" pattern="[0-9]*" class="neo-input position-relative font-monospace text-center w-100 h-100" name="captcha" id="captchaInputField" placeholder="     " maxlength="5" autocomplete="off" required style="font-size: 2rem; letter-spacing: 1.2rem; font-weight: bold; text-shadow: -1px -1px 2px rgba(255,255,255,0.1), 1px 1px 2px rgba(0,0,0,0.8);">
                            </div>
                            <button type="button" class="neo-raised-btn m-0" style="height: 64px; width: 64px; border-radius: 50%;" onclick="refreshCaptcha()">
                                <i class="fas fa-redo"></i>
                            </button>
                        </div>
                        {% else %}""",
    c, count=1, flags=re.DOTALL
)

# BUTTON
c = re.sub(
    r"{% elif active_style == 'swiss_minimal' %}.*?{% else %}",
    """{% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 400; padding: 12px 0;">
                                ورود
                            </div>
                        {% elif active_style == 'neumorphic_3d' %}
                            <div class="neo-submit">
                                ورود
                            </div>
                        {% else %}""",
    c, count=1, flags=re.DOTALL
)

# Forgot password links and wrapper close
c = c.replace("""</form>""", """
                    {% if active_style == 'neumorphic_3d' %}
                        <div class="text-center" style="margin-top: 30px; font-size: 0.85rem; color: #64748b;">
                            <div class="mb-2 cursor-pointer">فراموشی رمز؟</div>
                            <div>حساب کاربری ندارید؟ <span style="color: #cbd5e1; cursor: pointer;">ثبت نام</span></div>
                        </div>
                    </div>
                    {% endif %}
                </form>""")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
