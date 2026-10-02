import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# -----------------
# SWISS MINIMAL
# -----------------

# 1. CSS
css_fix = """
.login-theme-swiss_minimal .login-main-card {
    background: #111111 !important;
    border: none !important;
    box-shadow: none !important;
}
.login-theme-swiss_minimal input:-webkit-autofill,
.login-theme-swiss_minimal input:-webkit-autofill:hover, 
.login-theme-swiss_minimal input:-webkit-autofill:focus, 
.login-theme-swiss_minimal input:-webkit-autofill:active{
    -webkit-box-shadow: 0 0 0 30px #111111 inset !important;
    -webkit-text-fill-color: white !important;
    transition: background-color 5000s ease-in-out 0s;
}
.login-theme-swiss_minimal .login-brand-logo { display: none !important; }
"""
c = c.replace(".login-theme-swiss_minimal .login-main-card {\n    background: transparent !important;\n    box-shadow: none !important;\n}", css_fix)

# 2. Subtitle
persian_subtitle = "<div class='text-start mt-5 mb-4' style='font-size: 1.15rem; font-weight: 400; letter-spacing: 0.2px; font-family: -apple-system, sans-serif;' dir='rtl'>خوش آمدید.<br><span style='color: #a1a1aa; font-size: 0.95rem;'>برای ادامه وارد شوید.</span></div>"
c = re.sub(r"{% elif active_style == 'swiss_minimal' %}\s*خوش آمدید.*?جهت ورود مشخصات خود را وارد کنید.", "{% elif active_style == 'swiss_minimal' %}\n                        " + persian_subtitle, c, flags=re.DOTALL)

# 3. Inputs
old_user = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">نام کاربری</span>
                                  <div class="flex-grow-1"></div>
                              </div>
                              <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                  <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left;">
                              </div>
                          </div>"""
new_user = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-2">
                                  <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                                  <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">نام کاربری</span>
                                  <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                              </div>
                              <div class="d-flex align-items-center pb-2" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" name="username" placeholder="username" required autofocus style="direction: ltr; text-align: left; font-family: -apple-system, sans-serif; font-weight: 300;">
                              </div>
                          </div>"""
c = c.replace(old_user, new_user)

old_pass = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-1" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <span class="text-white pe-3 ps-1 pb-1" style="font-size: 0.85rem; letter-spacing: 0.5px; font-family: -apple-system, sans-serif;">رمز عبور</span>
                                  <div class="flex-grow-1"></div>
                              </div>
                              <div class="d-flex align-items-center" style="border-bottom: 2px solid #fff; padding-bottom: 2px;">
                                  <i class="fas fa-lock text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="password" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 font-monospace fs-5" name="password" id="loginPasswordInput" placeholder="••••••••" required style="direction: ltr; text-align: left; letter-spacing: 2px;">
                                  <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none ms-2" onclick="togglePasswordVisibility()">
                                      <i class="fas fa-eye" id="passwordToggleIcon"></i>
                                  </button>
                              </div>
                          </div>"""
new_pass = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-4" dir="ltr">
                              <div class="d-flex align-items-center mb-2">
                                  <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                                  <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">رمز عبور</span>
                                  <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                              </div>
                              <div class="d-flex align-items-center pb-2" style="border-bottom: 1px solid rgba(255,255,255,0.2);">
                                  <i class="fas fa-lock text-white opacity-75 ms-2 me-3 fs-5"></i>
                                  <input type="password" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" name="password" id="loginPasswordInput" placeholder="••••••••" required style="direction: ltr; text-align: left; letter-spacing: 2px;">
                              </div>
                          </div>"""
c = c.replace(old_pass, new_pass)

# 4. Captcha
old_captcha = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-5" style="margin-top: 30px;" dir="ltr">
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
                              <div class="text-start mt-2" dir="ltr" style="text-align: left !important;">
                                  <span class="text-white opacity-50" style="font-size: 0.85rem; font-family: -apple-system, sans-serif;">کد امنیتی (Captcha)</span>
                              </div>
                          </div>"""
new_captcha = """                          {% elif active_style == 'swiss_minimal' %}
                          <div class="position-relative mb-5" style="margin-top: 30px;" dir="ltr">
                              <div class="d-flex align-items-center justify-content-center mb-2 px-4">
                                  <div class="captcha-img-box flex-grow-1" style="height: 40px; filter: invert(1) grayscale(1) brightness(2) contrast(4); cursor: pointer;" onclick="refreshCaptcha()">
                                      <img id="captchaImg" src="{{ url_for('captcha_image') }}" alt="کپچا" class="w-100 h-100 d-block" style="object-fit: contain; transform: scale(1.2);">
                                  </div>
                                  <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none ms-2" onclick="refreshCaptcha()">
                                      <i class="fas fa-rotate-right fs-5" style="font-weight: 300;"></i>
                                  </button>
                              </div>
                              <div class="d-flex align-items-center justify-content-center">
                                  <input type="text" inputmode="numeric" pattern="[0-9]*" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none text-center font-monospace px-0 mx-auto" name="captcha" id="captchaInputField" placeholder="     " maxlength="5" autocomplete="off" required style="width: 250px; font-size: 2.2rem; letter-spacing: 1.5rem; background-image: repeating-linear-gradient(to right, transparent 0, transparent 10px, rgba(255,255,255,0.3) 10px, rgba(255,255,255,0.3) 40px); background-size: 50px 1px; background-position: bottom left; background-repeat: repeat-x; padding-bottom: 5px; direction: ltr; margin-left: 10px !important;">
                              </div>
                              <div class="text-start mt-2" dir="ltr" style="text-align: left !important;">
                                  <span class="text-white opacity-50" style="font-size: 0.8rem; font-family: -apple-system, sans-serif;">کد امنیتی (Captcha)</span>
                              </div>
                          </div>"""
c = c.replace(old_captcha, new_captcha)

# 5. Button
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

old_inner = """{% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 400; padding: 12px 0;">
                                ورود
                            </div>"""
new_inner = """{% elif active_style == 'swiss_minimal' %}
                            <span style="font-size: 1.15rem;">ورود</span>"""
c = c.replace(old_inner, new_inner)

# 6. Footer
c = c.replace("{% if active_style == 'neumorphic_3d' %}style=\"display: none !important;\"{% endif %}", "{% if active_style in ['neumorphic_3d', 'swiss_minimal'] %}style=\"display: none !important;\"{% endif %}")


# -----------------
# STEALTH TACTICAL
# -----------------

# 1. Background
stealth_css = """/* STEALTH RE-IMPLEMENTATION */
.login-theme-stealth_tactical {
    background: #0a0a0a;
    background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px) !important;
    background-size: 10px 10px !important;
    color: #cbd5e1;
}
.login-theme-stealth_tactical .login-main-card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: #cbd5e1 !important;
}
.login-theme-stealth_tactical .login-card-header { display: none !important; }
.login-theme-stealth_tactical .login-submit-btn {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
    border-bottom: 4px solid #cc0000 !important;
    border-radius: 8px !important;
    clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px) !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.6) !important;
}
.login-theme-stealth_tactical .login-submit-btn:hover {
    filter: brightness(1.1);
}
"""
c = re.sub(r"/\* 🔻 استایل ۶: تم نظامی زره‌پوش \(stealth_tactical\) 🔻 \*/.*?/\* 🔻 استایل ۷", "/* 🔻 استایل ۷", c, flags=re.DOTALL)
c = c.replace("/* NEUMORPHIC 3D RE-IMPLEMENTATION */", stealth_css + "\n/* NEUMORPHIC 3D RE-IMPLEMENTATION */")

# 2. Form blocks
user_block = """{% elif active_style == 'stealth_tactical' %}
                          <div class="text-center mb-4 mt-2">
                              <h4 style="font-weight: 800; font-size: 1.4rem; letter-spacing: 2px; color: #e2e8f0; margin-bottom: 10px;">SECURE LOGIN</h4>
                              <div class="d-inline-flex align-items-center justify-content-center gap-2" style="border: 1px dashed rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 4px; border-left: 2px solid #3b82f6; border-right: 2px solid #3b82f6;">
                                  <i class="fas fa-fingerprint text-info fs-5"></i>
                                  <div style="font-size: 0.75rem; color: #94a3b8; font-family: monospace; text-align: left; line-height: 1.2;">
                                      ACCESS GRANTED ONLY TO<br>AUTHORIZED PERSONNEL
                                  </div>
                              </div>
                          </div>
                          <div class="stealth-input-wrapper mb-3 d-flex" dir="ltr" style="height: 64px; background: linear-gradient(to bottom, #4a4e59, #2b2e35); padding: 3px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                              <div class="stealth-hex-icon d-flex align-items-center justify-content-center" style="width: 65px; height: 100%; background: linear-gradient(to bottom, #3a3d45, #1c1e22); border-right: 2px solid #1c1e22; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 25% 100%, 0% 50%); flex-shrink: 0;">
                                  <i class="fas fa-user" style="color: #f59e0b; font-size: 1.5rem; text-shadow: 0 0 10px rgba(245, 158, 11, 0.6);"></i>
                              </div>
                              <div class="flex-grow-1 d-flex flex-column justify-content-center px-3" style="background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 2px, transparent 2px, transparent 4px);">
                                  <div style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; margin-bottom: -2px; letter-spacing: 1px; text-align: left;">شناسه کاربری (USERNAME)</div>
                                  <input type="text" name="username" style="background: transparent; border: none; outline: none; color: #f59e0b; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 5px rgba(245, 158, 11, 0.4); width: 100%; direction: ltr; text-align: left;" placeholder="OPERATIVE-97" required autofocus>
                              </div>
                          </div>"""
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-input-wrapper.*?</div>\s*</div>\s*</div>", user_block, c, flags=re.DOTALL, count=1)

pass_block = """{% elif active_style == 'stealth_tactical' %}
                          <div class="stealth-input-wrapper mb-3 d-flex" dir="ltr" style="height: 64px; background: linear-gradient(to bottom, #4a4e59, #2b2e35); padding: 3px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                              <div class="stealth-hex-icon d-flex align-items-center justify-content-center" style="width: 65px; height: 100%; background: linear-gradient(to bottom, #3a3d45, #1c1e22); border-right: 2px solid #1c1e22; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 25% 100%, 0% 50%); flex-shrink: 0;">
                                  <i class="fas fa-lock" style="color: #f59e0b; font-size: 1.5rem; text-shadow: 0 0 10px rgba(245, 158, 11, 0.6);"></i>
                              </div>
                              <div class="flex-grow-1 d-flex flex-column justify-content-center px-3" style="background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 2px, transparent 2px, transparent 4px);">
                                  <div style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; margin-bottom: -2px; letter-spacing: 1px; text-align: left;">رمز عبور (PASSWORD)</div>
                                  <input type="password" name="password" id="loginPasswordInput" style="background: transparent; border: none; outline: none; color: #f59e0b; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 5px rgba(245, 158, 11, 0.4); width: 100%; direction: ltr; text-align: left; letter-spacing: 3px;" placeholder="••••••••••••" required>
                              </div>
                          </div>"""
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-input-wrapper.*?</div>\s*</div>\s*</div>", pass_block, c, flags=re.DOTALL, count=1)

captcha_block = """{% elif active_style == 'stealth_tactical' %}
                          <div class="text-center mb-1 mt-4">
                              <div style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; letter-spacing: 2px;">کد امنیتی (VERIFICATION CODE)</div>
                          </div>
                          <div class="stealth-captcha-hud p-2 position-relative d-flex flex-column align-items-center" style="border: 2px solid #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.2), inset 0 0 10px rgba(245, 158, 11, 0.2); border-radius: 4px; margin-bottom: 25px; background: rgba(245, 158, 11, 0.05);">
                              <div class="corner top-left" style="position: absolute; top: -2px; left: -2px; width: 15px; height: 15px; border-top: 3px solid #fff; border-left: 3px solid #fff;"></div>
                              <div class="corner top-right" style="position: absolute; top: -2px; right: -2px; width: 15px; height: 15px; border-top: 3px solid #fff; border-right: 3px solid #fff;"></div>
                              <div class="corner bottom-left" style="position: absolute; bottom: -2px; left: -2px; width: 15px; height: 15px; border-bottom: 3px solid #fff; border-left: 3px solid #fff;"></div>
                              <div class="corner bottom-right" style="position: absolute; bottom: -2px; right: -2px; width: 15px; height: 15px; border-bottom: 3px solid #fff; border-right: 3px solid #fff;"></div>
                              
                              <div class="d-flex w-100 justify-content-center align-items-center" style="height: 50px; cursor: pointer;" onclick="refreshCaptcha()">
                                  <img id="captchaImg" src="{{ url_for('captcha_image') }}" style="height: 100%; filter: invert(1) sepia(1) saturate(5) hue-rotate(350deg) brightness(1.2) contrast(1.5);">
                                  <i class="fas fa-rotate ms-3 text-warning opacity-75 fs-5"></i>
                              </div>
                              <div class="mt-2 w-100 d-flex justify-content-center px-3 mb-1">
                                  <input type="text" name="captcha" id="captchaInputField2" maxlength="5" autocomplete="off" required style="background: rgba(0,0,0,0.5); border: 1px solid rgba(245, 158, 11, 0.3); color: #fff; font-size: 1.5rem; font-family: monospace; letter-spacing: 10px; text-align: center; width: 100%; outline: none; padding: 2px;" placeholder="[ TYPE CODE ]" onfocus="this.style.borderColor='#f59e0b'" onblur="this.style.borderColor='rgba(245, 158, 11, 0.3)'">
                              </div>
                          </div>"""
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-captcha-wrapper.*?</div>\s*</div>\s*</div>", captcha_block, c, flags=re.DOTALL, count=1)

submit_block = """{% elif active_style == 'stealth_tactical' %}
                            <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="background: linear-gradient(to bottom, #7a8293, #434853); border-radius: 8px; clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px); padding: 12px 0;">
                                <span style="font-weight: 900; font-size: 1.4rem; letter-spacing: 4px; color: #111; text-shadow: 1px 1px 0px rgba(255,255,255,0.3);">تایید هویت</span>
                            </div>"""
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-btn-inner.*?</div>", submit_block, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("ALL APPLIED SUCCESSFULLY!")
