import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

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

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED CAPTCHA")
