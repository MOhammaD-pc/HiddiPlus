import io
import re

def update_login():
    with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update CSS for swiss_minimal
    css_old = """.login-theme-swiss_minimal .login-card-header,
.login-theme-nordic_studio .login-card-header,
.login-theme-minimal_luxury .login-card-header {
    background: transparent;
    border-bottom: 1px solid rgba(255, 255, 255, 0.05);
}"""
    css_new = """.login-theme-swiss_minimal .login-card-header,
.login-theme-nordic_studio .login-card-header,
.login-theme-minimal_luxury .login-card-header {
    background: transparent;
    border-bottom: none;
    padding-bottom: 0 !important;
}
.login-theme-swiss_minimal {
    background: #111111 !important;
}
.login-theme-swiss_minimal .login-main-card {
    background: transparent !important;
    box-shadow: none !important;
}
.swiss-form-control:focus {
    outline: none !important;
    box-shadow: none !important;
}
"""
    if css_old in c:
        c = c.replace(css_old, css_new)
        
    # 2. Update Header
    header_old = """<h4 class="fw-black mb-1 login-brand-title">
                    {% if active_style == 'stealth_tactical' %}ورود امن{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}
                </h4>"""
    header_new = """<h4 class="fw-black mb-1 login-brand-title">
                    {% if active_style == 'stealth_tactical' %}ورود امن{% elif active_style == 'swiss_minimal' %}<span style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 2.8rem; font-weight: 300; letter-spacing: 1px; color: #fff; display: block; margin-bottom: -5px;'>AURA</span><span style='font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; font-size: 1.5rem; font-weight: 300; color: #fff;'>Access</span>{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}
                </h4>"""
    c = c.replace(header_old, header_new)

    sub_old = """{% if active_style == 'hacker_terminal' %}
                        AUTHENTICATION // ENCRYPTED ACCESS ONLY
                    {% elif active_style == 'stealth_tactical' %}
                        دسترسی فقط برای پرسنل مجاز
                    {% else %}
                        {{ login_page_subtitle or 'ورود مدیران و همکاران فروش' }}
                    {% endif %}"""
    sub_new = """{% if active_style == 'hacker_terminal' %}
                        AUTHENTICATION // ENCRYPTED ACCESS ONLY
                    {% elif active_style == 'stealth_tactical' %}
                        دسترسی فقط برای پرسنل مجاز
                    {% elif active_style == 'swiss_minimal' %}
                        <div class='text-start mt-5' style='font-size: 1.5rem; color: #fff; font-family: -apple-system, sans-serif;'>خوش آمدید.</div><div class='text-start mb-2' style='font-size: 1.1rem; color: rgba(255,255,255,0.7); font-family: -apple-system, sans-serif;'>برای ادامه وارد شوید.</div>
                    {% else %}
                        {{ login_page_subtitle or 'ورود مدیران و همکاران فروش' }}
                    {% endif %}"""
    c = c.replace(sub_old, sub_new)

    # hide logo icon for swiss minimal
    c = c.replace("{% if branding.get('logo_url') %}", "{% if branding.get('logo_url') and active_style != 'swiss_minimal' %}")
    c = c.replace("{% if not branding.get('logo_url') %}", "{% if not branding.get('logo_url') and active_style != 'swiss_minimal' %}")

    # hide version badge
    c = c.replace("""<div class="d-inline-flex align-items-center gap-1 px-3 py-1 rounded-pill login-version-badge font-monospace" style="font-size: 0.72rem;">""", """<div class="d-inline-flex align-items-center gap-1 px-3 py-1 rounded-pill login-version-badge font-monospace" style="font-size: 0.72rem; {% if active_style == 'swiss_minimal' %}display: none !important;{% endif %}">""")

    # We will replace the entire form by splitting the string.
    start = c.find('<form method="POST"')
    end = c.find('</form>') + 7
    
    new_form = """<form method="POST" autocomplete="on" id="mainLoginForm">
                    <!-- نام کاربری -->
                    <div class="mb-3">
                        {% if active_style == 'stealth_tactical' %}
                        <div class="stealth-input-wrapper d-flex align-items-stretch" style="height: 64px;">
                            <div class="stealth-hexagon-icon flex-shrink-0 d-flex align-items-center justify-content-center">
                                <i class="fas fa-user"></i>
                            </div>
                            <div class="stealth-input-body-wrap flex-grow-1 d-flex">
                                <div class="stealth-input-body flex-grow-1 d-flex flex-column justify-content-center">
                                    <span class="stealth-floating-label">شناسه کاربری (OPERATIVE)</span>
                                    <input type="text" class="stealth-form-control font-monospace" name="username" placeholder="OPERATIVE-97" required autofocus style="direction: ltr; text-align: left;">
                                </div>
                            </div>
                        </div>
                        {% elif active_style == 'swiss_minimal' %}
                        <div class="position-relative mb-4">
                            <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">Username</span>
                                <div class="flex-grow-1"></div>
                            </div>
                            <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left;">
                            </div>
                        </div>
                        {% else %}
                        <label class="form-label small fw-bold mb-1">
                            {% if active_style == 'hacker_terminal' %}
                                <span class="font-monospace text-success">[USER_ID] نام کاربری:</span>
                            {% else %}
                                <i class="fas fa-user-circle me-1 opacity-75"></i> نام کاربری:
                            {% endif %}
                        </label>
                        <div class="input-group login-input-group">
                            <span class="input-group-text border-start-0">
                                {% if active_style == 'hacker_terminal' %}<i class="fas fa-terminal text-success"></i>
                                {% elif active_style == 'ios_lockscreen' %}<i class="fas fa-expand text-secondary fs-5"></i>
                                {% else %}<i class="fas fa-user text-muted"></i>
                                {% endif %}
                            </span>
                            <input type="text" class="form-control border-start-0 ps-1 font-monospace" name="username" placeholder="{% if active_style == 'hacker_terminal' %}root_user{% elif active_style == 'ios_lockscreen' %}Your Name{% else %}Username{% endif %}" required autofocus style="direction: ltr; text-align: left;">
                            {% if active_style == 'ios_lockscreen' %}
                            <span class="input-group-text border-start-0 bg-transparent text-secondary">
                                <i class="fas fa-user-circle fs-5"></i>
                            </span>
                            {% endif %}
                        </div>
                        {% endif %}
                    </div>

                    <!-- رمز عبور -->
                    <div class="mb-3">
                        {% if active_style == 'stealth_tactical' %}
                        <div class="stealth-input-wrapper d-flex align-items-stretch" style="height: 64px;">
                            <div class="stealth-hexagon-icon flex-shrink-0 d-flex align-items-center justify-content-center">
                                <i class="fas fa-lock"></i>
                            </div>
                            <div class="stealth-input-body-wrap flex-grow-1 d-flex">
                                <div class="stealth-input-body flex-grow-1 position-relative d-flex flex-column justify-content-center">
                                    <span class="stealth-floating-label">رمز دسترسی (ACCESS KEY)</span>
                                    <input type="password" name="password" id="loginPasswordInput" class="stealth-form-control pe-5 font-monospace" placeholder="            " required style="direction: ltr; text-align: left;">
                                    <button type="button" class="position-absolute start-0 top-50 translate-middle-y bg-transparent border-0 text-warning opacity-75 ms-3 cursor-pointer" onclick="togglePasswordVisibility()">
                                        <i class="fas fa-eye" id="passwordToggleIcon"></i>
                                    </button>
                                </div>
                            </div>
                        </div>
                        {% elif active_style == 'swiss_minimal' %}
                        <div class="position-relative mb-5">
                            <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">Password</span>
                                <div class="flex-grow-1"></div>
                            </div>
                            <div class="d-flex align-items-center" style="border-bottom: 1px solid rgba(255,255,255,0.3); padding-bottom: 2px;">
                                <i class="fas fa-lock text-white opacity-50 ms-2 me-3 fs-5"></i>
                                <input type="password" name="password" id="loginPasswordInput" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" placeholder="••••••••" required style="direction: ltr; text-align: left;">
                            </div>
                        </div>
                        {% else %}
                        <label class="form-label small fw-bold mb-1 d-flex justify-content-between align-items-center">
                            <span>
                                {% if active_style == 'hacker_terminal' %}
                                    <span class="font-monospace text-success">[AUTH_KEY] رمز عبور:</span>
                                {% else %}
                                    <i class="fas fa-key me-1 opacity-75"></i> رمز عبور:
                                {% endif %}
                            </span>
                            <a href="#" class="text-decoration-none small" style="font-size: 0.75rem;">فراموشی رمز؟</a>
                        </label>
                        <div class="input-group login-input-group">
                            <span class="input-group-text border-start-0">
                                {% if active_style == 'hacker_terminal' %}<i class="fas fa-asterisk text-success"></i>
                                {% elif active_style == 'ios_lockscreen' %}<i class="fas fa-lock text-secondary fs-5"></i>
                                {% else %}<i class="fas fa-lock text-muted"></i>
                                {% endif %}
                            </span>
                            <input type="password" id="loginPasswordInput" class="form-control border-start-0 border-start-0 px-1 font-monospace" name="password" placeholder="        " required style="direction: ltr; {% if active_style == 'ios_lockscreen' %}text-align: left;{% endif %}">
                            <button type="button" class="input-group-text border-start-0 bg-transparent cursor-pointer" onclick="togglePasswordVisibility()" title="نمایش/مخفی‌سازی رمز">
                                <i class="fas fa-eye {% if active_style == 'ios_lockscreen' %}text-secondary fs-5{% else %}text-muted{% endif %}" id="passwordToggleIcon"></i>
                            </button>
                        </div>
                        {% endif %}
                    </div>

                    <!-- کد تایید امنیتی -->
                    <div class="mb-4">
                        {% if active_style == 'ios_lockscreen' %}
                        <div class="input-group login-input-group align-items-center p-1" style="height: 56px;">
                            <span class="input-group-text border-0 bg-transparent ps-3 pe-2 text-secondary">
                                <i class="fas fa-key fs-5"></i>
                            </span>
                            <input type="text" inputmode="numeric" pattern="[0-9]*" class="form-control border-0 bg-transparent font-monospace fs-5 text-white" name="captcha" id="captchaInputField" placeholder="کد ۵ رقمی" maxlength="5" autocomplete="off" required style="letter-spacing: 4px; text-align: left;">
                            <div class="captcha-img-box rounded-pill overflow-hidden border border-secondary border-opacity-25 ms-1 me-1 cursor-pointer" onclick="refreshCaptcha()" style="height: 38px; width: 110px; flex-shrink: 0; background: rgba(0,0,0,0.2) !important;">
                                <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: cover; filter: invert(0.9) hue-rotate(180deg);">
                            </div>
                            <button type="button" class="input-group-text border-0 bg-transparent text-secondary pe-3 ps-2 cursor-pointer" onclick="refreshCaptcha()">
                                <i class="fas fa-rotate fs-5"></i>
                            </button>
                        </div>
                        {% elif active_style == 'stealth_tactical' %}
                        <div class="stealth-captcha-wrapper">
                            <div class="text-center mb-1">
                                <span class="stealth-floating-label" style="position: static; font-size: 0.8rem; letter-spacing: 2px;">کد تایید امنیتی (HUD)</span>
                            </div>
                            <div class="stealth-captcha-hud p-3 position-relative d-flex flex-column align-items-center gap-2">
                                <div class="stealth-hud-corners"></div>
                                <div class="d-flex align-items-center justify-content-center gap-3 w-100 px-3">
                                    <div class="captcha-img-box stealth-captcha-img cursor-pointer flex-grow-1 border border-warning" onclick="refreshCaptcha()" style="height: 48px; filter: invert(1) sepia(1) saturate(5) hue-rotate(350deg) brightness(1.2) contrast(1.2);">
                                        <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: cover;">
                                    </div>
                                    <button type="button" class="btn btn-warning rounded-1 stealth-rotate-btn d-flex align-items-center justify-content-center" onclick="refreshCaptcha()" style="height: 48px; width: 48px;">
                                        <i class="fas fa-rotate fs-5 text-dark"></i>
                                    </button>
                                </div>
                                <input type="text" inputmode="numeric" pattern="[0-9]*" class="stealth-captcha-input text-center font-monospace w-100 mt-2" name="captcha" id="captchaInputField2" placeholder="[ ورود کد ]" maxlength="5" autocomplete="off" required>
                            </div>
                        </div>
                        {% elif active_style == 'swiss_minimal' %}
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
                                <span class="text-white opacity-50" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">Captcha Code</span>
                            </div>
                        </div>
                        {% else %}
                        <label class="form-label small fw-bold mb-1 d-flex justify-content-between align-items-center">
                            <span>
                                {% if active_style == 'hacker_terminal' %}
                                    <span class="font-monospace text-success">[VERIFICATION_TOKEN] کد امنیتی:</span>
                                {% else %}
                                    <i class="fas fa-shield-check me-1 opacity-75"></i> کد امنیتی (کپچا):
                                {% endif %}
                            </span>
                            {% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal'] %}
                            <small class="text-muted cursor-pointer" onclick="refreshCaptcha()" style="font-size: 0.75rem;">
                                <i class="fas fa-rotate fs-6"></i>
                            </small>
                            {% endif %}
                        </label>
                        <div class="d-flex align-items-center gap-2 mb-2">
                            <div class="captcha-img-box flex-grow-1 rounded-3 overflow-hidden shadow-sm border p-0 d-flex align-items-center justify-content-center cursor-pointer" onclick="refreshCaptcha()" title="تغییر کد امنیتی" style="height: 48px;">
                                <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: cover;">
                            </div>
                            <button type="button" class="btn btn-outline-secondary rounded-3 d-flex align-items-center justify-content-center flex-shrink-0" onclick="refreshCaptcha()" title="تغییر کد امنیتی" style="width: 48px; height: 48px;">
                                <i class="fas fa-rotate"></i>
                            </button>
                        </div>
                        <input type="text" inputmode="numeric" pattern="[0-9]*" class="form-control text-center font-monospace fs-4 fw-bold login-captcha-input py-2" name="captcha" id="captchaInputField3" placeholder="کد ۵ رقمی" maxlength="5" autocomplete="off" required style="letter-spacing: 6px;">
                        {% endif %}
                    </div>

                    <!-- دکمه ورود -->
                    <button type="submit" class="btn w-100 py-2 fw-bold login-submit-btn d-flex align-items-center justify-content-center gap-2">
                        {% if active_style == 'hacker_terminal' %}
                            <i class="fas fa-terminal"></i>
                            <span class="font-monospace">[ {{ _('ورود') if _ else 'ورود' }} // {{ _('تایید هویت') if _ else 'تایید هویت' }} ]</span>
                        {% elif active_style == 'stealth_tactical' %}
                            <div class="stealth-btn-inner w-100 h-100 d-flex align-items-center justify-content-center">
                                <span style="letter-spacing: 2px; font-weight: 900; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.8);">تایید هویت</span>
                            </div>
                        {% elif active_style == 'ios_lockscreen' %}
                            <span>ورود</span>
                        {% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 400; padding: 12px 0;">
                                Sign In
                            </div>
                        {% else %}
                            <i class="fas fa-arrow-right-to-bracket"></i>
                            <span>ورود به حساب کاربری</span>
                        {% endif %}
                    </button>
                    
                    {% if active_style == 'swiss_minimal' %}
                    <div class="text-center mt-4">
                        <a href="#" class="text-decoration-none text-white opacity-50" style="font-size: 0.9rem; font-family: -apple-system, sans-serif;">Forgot password?</a>
                    </div>
                    {% endif %}
                </form>"""
    c = c[:start] + new_form + c[end:]

    with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
        f.write(c)
        
    print("SUCCESS")
    
update_login()
