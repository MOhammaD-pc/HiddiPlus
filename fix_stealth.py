import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Background fix: Dark grid
css_bg_fix = """
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
"""

# Let's completely remove BOTH old CSS blocks for stealth_tactical and append this clean one.
c = re.sub(r"/\* 🔻 استایل ۶: تم نظامی زره‌پوش \(stealth_tactical\) 🔻 \*/.*?/\* 🔻 استایل ۷", "/* 🔻 استایل ۷", c, flags=re.DOTALL)
c = c.replace("/* NEUMORPHIC 3D RE-IMPLEMENTATION */", "/* STEALTH RE-IMPLEMENTATION */\n" + css_bg_fix + "\n/* NEUMORPHIC 3D RE-IMPLEMENTATION */")

# 2. Fix Logo area (Hide standard logo, we will inject custom one in the form)
# We already have:
# {% if active_style == 'stealth_tactical' %} ... {% elif active_style == 'ios_lockscreen' %}
# Wait, let's just use CSS to hide the default header for stealth_tactical
c = c.replace("/* STEALTH RE-IMPLEMENTATION */", "/* STEALTH RE-IMPLEMENTATION */\n.login-theme-stealth_tactical .login-card-header { display: none !important; }\n")


# 3. Form fields
# We need to replace the stealth_tactical blocks inside the form!
user_block = """{% if active_style == 'stealth_tactical' %}
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

c = re.sub(r"{% if active_style == 'stealth_tactical' %}.*?(?={% elif active_style == 'neumorphic_3d' %})", user_block + "\n                          ", c, flags=re.DOTALL, count=1)


pass_block = """{% if active_style == 'stealth_tactical' %}
                          <div class="stealth-input-wrapper mb-3 d-flex" dir="ltr" style="height: 64px; background: linear-gradient(to bottom, #4a4e59, #2b2e35); padding: 3px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                              <div class="stealth-hex-icon d-flex align-items-center justify-content-center" style="width: 65px; height: 100%; background: linear-gradient(to bottom, #3a3d45, #1c1e22); border-right: 2px solid #1c1e22; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 25% 100%, 0% 50%); flex-shrink: 0;">
                                  <i class="fas fa-lock" style="color: #f59e0b; font-size: 1.5rem; text-shadow: 0 0 10px rgba(245, 158, 11, 0.6);"></i>
                              </div>
                              <div class="flex-grow-1 d-flex flex-column justify-content-center px-3" style="background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 2px, transparent 2px, transparent 4px);">
                                  <div style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; margin-bottom: -2px; letter-spacing: 1px; text-align: left;">رمز عبور (PASSWORD)</div>
                                  <input type="password" name="password" id="loginPasswordInput" style="background: transparent; border: none; outline: none; color: #f59e0b; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 5px rgba(245, 158, 11, 0.4); width: 100%; direction: ltr; text-align: left; letter-spacing: 3px;" placeholder="••••••••••••" required>
                              </div>
                          </div>"""

# Find the second stealth_tactical block
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}.*?(?={% elif active_style == 'neumorphic_3d' %})", pass_block + "\n                          ", c, flags=re.DOTALL, count=1)


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

# Replace the third one
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}.*?(?={% elif active_style == 'neumorphic_3d' %})", captcha_block + "\n                          ", c, flags=re.DOTALL, count=1)


submit_block = """{% elif active_style == 'stealth_tactical' %}
                            <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="background: linear-gradient(to bottom, #7a8293, #434853); border-radius: 8px; clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px); padding: 12px 0;">
                                <span style="font-weight: 900; font-size: 1.4rem; letter-spacing: 4px; color: #111; text-shadow: 1px 1px 0px rgba(255,255,255,0.3);">تایید هویت</span>
                            </div>"""

# We need to replace the submit block content for stealth_tactical
c = re.sub(r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-btn-inner.*?</div>", submit_block, c, flags=re.DOTALL)

# Add custom CSS for the submit button for stealth_tactical to remove padding/border since inner div handles it
submit_css = """
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
c = c.replace("/* STEALTH RE-IMPLEMENTATION */", "/* STEALTH RE-IMPLEMENTATION */\n" + submit_css)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED STEALTH")
