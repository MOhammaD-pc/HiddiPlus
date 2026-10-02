import io

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's replace the content of tab-swiss
old_swiss_tab_content = """        <div class="theme-container theme-swiss" id="tab-swiss" dir="ltr">
            <div style="margin-bottom: 40px;">
                <span style="font-size: 2.8rem; font-weight: 300; letter-spacing: 1px; display: block; margin-bottom: -5px;">AURA</span>
                <span style="font-size: 1.5rem; font-weight: 300;">Access</span>
                
                <div style="margin-top: 50px; font-size: 1.5rem;">خوش آمدید.</div>
                <div style="font-size: 1.1rem; color: rgba(255,255,255,0.7);">جهت ورود مشخصات خود را وارد کنید.</div>
            </div>
            
            <div class="swiss-input-group">
                <div class="swiss-label-row">
                    <span>نام کاربری</span>
                    <div style="flex-grow: 1;"></div>
                </div>
                <div class="swiss-input-row focused">
                    <i class="far fa-user"></i>
                    <input type="text" placeholder="username">
                </div>
            </div>
            
            <div class="swiss-input-group" style="margin-bottom: 3rem;">
                <div class="swiss-label-row">
                    <span>رمز عبور</span>
                    <div style="flex-grow: 1;"></div>
                </div>
                <div class="swiss-input-row">
                    <i class="fas fa-lock" style="opacity: 0.5;"></i>
                    <input type="password" placeholder="••••••••">
                </div>
            </div>
            
            <button class="swiss-btn">ورود</button>
            <div style="text-align: center; margin-top: 30px;">
                <a href="#" style="color: rgba(255,255,255,0.5); text-decoration: none; font-size: 0.9rem;">فراموشی رمز؟</a>
            </div>
        </div>"""

new_swiss_tab_content = """        <div class="theme-container theme-swiss" id="tab-swiss" dir="ltr" style="background: #111111; padding: 40px 24px; min-height: 700px; color: #f8fafc; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
            <div style="margin-bottom: 30px; text-align: center;">
                <span style="font-weight: 400; font-size: 1.8rem; letter-spacing: 0.5px;">AURA<br>Access</span>
                <div class="text-start mt-5 mb-4" style="font-size: 1.15rem; font-weight: 400; letter-spacing: 0.2px; font-family: -apple-system, sans-serif; text-align: left;" dir="rtl">خوش آمدید.<br><span style="color: #a1a1aa; font-size: 0.95rem;">برای ادامه وارد شوید.</span></div>
            </div>
            
            <div class="position-relative mb-4" dir="ltr" style="margin-bottom: 1.5rem;">
                <div class="d-flex align-items-center mb-2" style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                    <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif; padding: 0 0.5rem; color: rgba(255,255,255,0.75);">نام کاربری</span>
                    <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                </div>
                <div class="d-flex align-items-center pb-2" style="display: flex; align-items: center; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);">
                    <i class="far fa-user text-white opacity-75 ms-2 me-3 fs-5" style="margin-right: 1rem; color: rgba(255,255,255,0.75);"></i>
                    <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" placeholder="username" style="background: transparent; border: none; color: #fff; flex-grow: 1; outline: none; font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 300;">
                </div>
            </div>
            
            <div class="position-relative mb-4" dir="ltr" style="margin-bottom: 2rem;">
                <div class="d-flex align-items-center mb-2" style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <div style="width: 30px; height: 1px; background: rgba(255,255,255,0.2);"></div>
                    <span class="text-white opacity-75 px-2" style="font-size: 0.85rem; font-family: -apple-system, sans-serif; padding: 0 0.5rem; color: rgba(255,255,255,0.75);">رمز عبور</span>
                    <div style="flex-grow: 1; height: 1px; background: rgba(255,255,255,0.2);"></div>
                </div>
                <div class="d-flex align-items-center pb-2" style="display: flex; align-items: center; padding-bottom: 0.5rem; border-bottom: 1px solid rgba(255,255,255,0.2);">
                    <i class="fas fa-lock text-white opacity-75 ms-2 me-3 fs-5" style="margin-right: 1rem; color: rgba(255,255,255,0.75);"></i>
                    <input type="password" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none px-0 fs-5" placeholder="••••••••" style="background: transparent; border: none; color: #fff; flex-grow: 1; outline: none; font-size: 1.2rem; letter-spacing: 2px;">
                </div>
            </div>
            
            <div class="position-relative mb-5" style="margin-top: 30px; margin-bottom: 3rem;" dir="ltr">
                <div class="d-flex align-items-center justify-content-center mb-2 px-4" style="display: flex; align-items: center; justify-content: center; margin-bottom: 0.5rem;">
                    <div class="captcha-img-box flex-grow-1" style="height: 40px; filter: invert(1) grayscale(1) brightness(2) contrast(4); cursor: pointer; flex-grow: 1;">
                        <img src="https://via.placeholder.com/150x50/ffffff/000000?text=7+4+9+2+5" alt="کپچا" class="w-100 h-100 d-block" style="width: 100%; height: 100%; object-fit: contain; transform: scale(1.2);">
                    </div>
                    <button type="button" class="btn btn-link text-white opacity-50 p-0 shadow-none text-decoration-none ms-2" style="background: transparent; border: none; color: rgba(255,255,255,0.5); cursor: pointer;">
                        <i class="fas fa-rotate-right fs-5" style="font-weight: 300;"></i>
                    </button>
                </div>
                <div class="d-flex align-items-center justify-content-center" style="display: flex; align-items: center; justify-content: center;">
                    <input type="text" class="form-control swiss-form-control bg-transparent border-0 text-white shadow-none text-center font-monospace px-0 mx-auto" placeholder="     " style="width: 250px; font-size: 2.2rem; letter-spacing: 1.5rem; background-image: repeating-linear-gradient(to right, transparent 0, transparent 10px, rgba(255,255,255,0.3) 10px, rgba(255,255,255,0.3) 40px); background-size: 50px 1px; background-position: bottom left; background-repeat: repeat-x; padding-bottom: 5px; direction: ltr; margin-left: 10px !important; background-color: transparent; border: none; color: #fff; outline: none; text-align: center;">
                </div>
                <div class="text-start mt-2" dir="ltr" style="text-align: left !important; margin-top: 0.5rem;">
                    <span class="text-white opacity-50" style="font-size: 0.8rem; font-family: -apple-system, sans-serif; color: rgba(255,255,255,0.5);">کد امنیتی (Captcha)</span>
                </div>
            </div>
            
            <button class="swiss-btn" style="width: 100%; background: #ffffff; color: #000000; font-weight: 400; font-family: -apple-system, sans-serif; border: none; border-radius: 0; padding: 14px; cursor: pointer; font-size: 1.15rem;">ورود</button>
            <div style="text-align: center; margin-top: 30px;">
                <a href="#" style="color: rgba(255,255,255,0.5); text-decoration: none; font-size: 0.9rem; font-family: -apple-system, sans-serif;">فراموشی رمز؟</a>
            </div>
        </div>"""

if old_swiss_tab_content in c:
    c = c.replace(old_swiss_tab_content, new_swiss_tab_content)
else:
    # Just a fallback if exact match fails
    pass

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED DEMO SWISS")
