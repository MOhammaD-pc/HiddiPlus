import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

bad_pattern = r"{% elif active_style == 'stealth_tactical' %}\s*<div class=\"stealth-captcha-wrapper\">.*?(?={% elif active_style == 'swiss_minimal' %})"

good_replacement = """{% elif active_style == 'stealth_tactical' %}
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
                          </div>
                          """

c = re.sub(bad_pattern, good_replacement, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED BOTTOM CAPTCHA")
