import io

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

broken_captcha = """{% elif active_style == 'swiss_minimal' %}
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
        <span class="text-white opacity-50" style="font-size: 0.75rem;">کد امنیتی (Captcha)</span>
    </div>
</div>"""

c = c.replace(broken_captcha, "")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED SWISS")
