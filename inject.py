import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Username
old_user_if = "{% if active_style == 'stealth_tactical' %}"
new_user_block = """{% if active_style == 'neumorphic_3d' %}
                        <div class="neo-track">
                            <div class="neo-raised-btn"><i class="fas fa-user"></i></div>
                            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                                <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">نام کاربری</span>
                                <input type="text" class="neo-input px-0 font-monospace" name="username" placeholder="username" style="text-align: left;" required autofocus>
                            </div>
                            <i class="fas fa-user-check" style="color: #64748b; margin-right: 15px; opacity: 0;"></i>
                        </div>
                        {% elif active_style == 'stealth_tactical' %}"""
c = c.replace(old_user_if, new_user_block, 1)

# 2. Password
# The next one is for password. Let's find the string just before the if:
# "<!-- رمز عبور -->\n                      <div class=\"mb-3\">\n                          {% if active_style == 'stealth_tactical' %}"
old_pass = "<!-- رمز عبور -->\n                      <div class=\"mb-3\">\n                          {% if active_style == 'stealth_tactical' %}"
new_pass = """<!-- رمز عبور -->
                      <div class="mb-3">
                          {% if active_style == 'neumorphic_3d' %}
                          <div class="neo-track">
                              <div class="neo-raised-btn"><i class="fas fa-lock"></i></div>
                              <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                                  <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">رمز عبور</span>
                                  <input type="password" class="neo-input px-0 font-monospace" name="password" id="loginPasswordInput" placeholder="••••••••" style="text-align: left;" required>
                              </div>
                              <i class="fas fa-eye-slash" id="passwordToggleIcon" style="color: #64748b; margin-right: 15px; cursor: pointer;" onclick="togglePasswordVisibility()"></i>
                          </div>
                          {% elif active_style == 'stealth_tactical' %}"""
c = c.replace(old_pass, new_pass, 1)

# 3. Captcha
old_captcha = "<!-- کد امنیتی -->\n                      <div class=\"mb-3\">\n                          {% if active_style == 'stealth_tactical' %}"
new_captcha = """<!-- کد امنیتی -->
                      <div class="mb-3">
                          {% if active_style == 'neumorphic_3d' %}
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
                          </div>
                          {% elif active_style == 'stealth_tactical' %}"""
c = c.replace(old_captcha, new_captcha, 1)

# 4. Submit
old_submit = "{% elif active_style == 'swiss_minimal' %}\n                            <div class=\"w-100 bg-white"
new_submit = """{% elif active_style == 'neumorphic_3d' %}
                            <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; font-family: -apple-system, sans-serif;">
                                ورود به حساب کاربری
                            </div>
                        {% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white"""
c = c.replace(old_submit, new_submit, 1)


with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("INJECTED")
