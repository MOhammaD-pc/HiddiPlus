import io
with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace HTML
i1 = c.find('<!-- ۴. استلث دارک زره‌پوش -->')
i2 = c.find('<!-- ۵. مینیمال سوئیسی -->')
if i1 != -1 and i2 != -1:
    html_replacement = """<!-- ۴. استلث دارک زره‌پوش -->
        <div class="theme-container theme-stealth" id="tab-stealth">
            <div style="text-align: center; margin-bottom: 22px;">
                <div style="font-size: 3rem; color: #9ca3af; margin-bottom: 0px;"><i class="fas fa-shield-halved"></i></div>
                <h3 style="font-family: 'Arial', sans-serif; font-weight: 900; letter-spacing: 2px; color: #f8fafc; margin-bottom: 4px;">ورود امن</h3>
                <p style="font-size: 0.75rem; color: #94a3b8; letter-spacing: 1px;">دسترسی فقط برای پرسنل مجاز</p>
            </div>
            
            <div class="stealth-input-wrapper" style="display: flex; align-items: stretch; height: 60px;">
                <div class="stealth-hexagon-icon" style="flex-shrink: 0;">
                    <i class="fas fa-user"></i>
                </div>
                <div class="stealth-input-body-wrap" style="flex-grow: 1; display: flex;">
                    <div class="stealth-input-body" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center;">
                        <span class="stealth-floating-label">USERNAME</span>
                        <input type="text" class="stealth-form-control" placeholder="OPERATIVE-97" style="direction: ltr; text-align: left;">
                    </div>
                </div>
            </div>
            
            <div class="stealth-input-wrapper" style="display: flex; align-items: stretch; height: 60px;">
                <div class="stealth-hexagon-icon" style="flex-shrink: 0;">
                    <i class="fas fa-lock"></i>
                </div>
                <div class="stealth-input-body-wrap" style="flex-grow: 1; display: flex;">
                    <div class="stealth-input-body" style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; position: relative;">
                        <span class="stealth-floating-label">PASSWORD</span>
                        <input type="password" class="stealth-form-control" placeholder="••••••••••••" style="direction: ltr; text-align: left;">
                        <i class="fas fa-eye" style="position: absolute; right: 15px; color: #f59e0b; opacity: 0.75;"></i>
                    </div>
                </div>
            </div>
            
            <div class="stealth-captcha-wrapper">
                <div class="text-center" style="text-align: center; margin-bottom: 4px;">
                    <span class="stealth-floating-label" style="font-size: 0.8rem; letter-spacing: 2px;">VERIFICATION CODE</span>
                </div>
                <div class="stealth-captcha-hud" style="padding: 12px; position: relative; display: flex; flex-direction: column; align-items: center; gap: 8px;">
                    <div class="stealth-hud-corners"></div>
                    <div style="display: flex; align-items: center; justify-content: center; gap: 12px; width: 100%; padding: 0 12px;">
                        <div class="stealth-captcha-img" style="flex-grow: 1; border: 1px solid #f59e0b; height: 48px; filter: contrast(1.5) sepia(1) hue-rotate(330deg) saturate(3); background: #111;">
                            <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #fff; font-family: monospace; font-size: 1.5rem; letter-spacing: 8px;">8W2J4</div>
                        </div>
                        <button style="background: #f59e0b; border: none; height: 48px; width: 48px; border-radius: 4px; display: flex; align-items: center; justify-content: center; cursor: pointer;">
                            <i class="fas fa-rotate fs-5" style="color: #000;"></i>
                        </button>
                    </div>
                    <input type="text" class="stealth-captcha-input" placeholder="[ ENTER CODE ]" style="text-align: center; width: 100%; margin-top: 8px;">
                </div>
            </div>
            
            <button class="stealth-btn" style="padding: 2px; border: none; background: #4a5568; margin-top: 20px; width: 100%; clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                <div style="background: linear-gradient(180deg, #9ca3af 0%, #4b5563 100%); clip-path: polygon(14px 0, calc(100% - 14px) 0, 100% 14px, 100% calc(100% - 14px), calc(100% - 14px) 100%, 14px 100%, 0 calc(100% - 14px), 0 14px); border-bottom: 2px solid #ef4444; width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; padding: 16px;">
                    <span style="letter-spacing: 2px; font-weight: 900; font-size: 1.2rem; text-shadow: 0 2px 4px rgba(0,0,0,0.8); color: #111827;">AUTHORIZE</span>
                </div>
            </button>
        </div>
        
        """
    c = c[:i1] + html_replacement + c[i2:]

# Now replace CSS
i3 = c.find('/* ─── ۴. استلث دارک زره‌پوش ─── */')
i4 = c.find('/* ─── ۵. مینیمال سوئیسی ─── */')
if i3 != -1 and i4 != -1:
    css_replacement = """/* ─── ۴. استلث دارک زره‌پوش ─── */
        .theme-stealth {
            background: #0a0a0a;
            background-image: radial-gradient(#2b3038 1px, transparent 1px), radial-gradient(#2b3038 1px, transparent 1px);
            background-position: 0 0, 10px 10px;
            background-size: 20px 20px;
            padding: 30px 24px;
            color: #cbd5e1;
            border-radius: 12px;
            border: 2px solid #1e293b;
        }
        .stealth-input-wrapper {
            filter: drop-shadow(0 10px 15px rgba(0,0,0,0.5));
            margin-bottom: 24px;
        }
        .stealth-hexagon-icon {
            width: 60px; height: 60px;
            background: #f59e0b;
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
            padding: 2px;
            margin-right: -10px;
            z-index: 2;
            display: flex; align-items: center; justify-content: center;
            position: relative;
        }
        .stealth-hexagon-icon::before {
            content: ''; position: absolute; top: 2px; left: 2px; right: 2px; bottom: 2px;
            background: linear-gradient(135deg, #374151 0%, #111827 100%);
            clip-path: polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%);
            z-index: -1;
        }
        .stealth-hexagon-icon i { color: #f59e0b; font-size: 1.2rem; }

        .stealth-input-body-wrap {
            background: #4a5568;
            clip-path: polygon(0 0, calc(100% - 15px) 0, 100% 15px, 100% 100%, 0 100%);
            padding: 2px 2px 2px 0;
        }
        .stealth-input-body {
            background: linear-gradient(to right, #374151 0%, #111827 100%);
            clip-path: polygon(0 0, calc(100% - 14px) 0, 100% 14px, 100% 100%, 0 100%);
            height: 100%;
            padding: 8px 15px 8px 30px;
        }
        .stealth-floating-label { font-size: 0.75rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 1px; }
        .stealth-form-control { background: transparent !important; border: none !important; color: #f59e0b !important; font-weight: 700; font-size: 1.1rem; outline: none; padding: 0; width: 100%; }
        .stealth-form-control::placeholder { color: #52525b !important; font-weight: 500; }

        .stealth-captcha-wrapper { margin-bottom: 30px; }
        .stealth-captcha-hud {
            background: rgba(245, 158, 11, 0.05);
            border: 1px solid rgba(245, 158, 11, 0.3);
            box-shadow: inset 0 0 20px rgba(245, 158, 11, 0.1);
        }
        .stealth-hud-corners::before, .stealth-hud-corners::after {
            content: ''; position: absolute; width: 15px; height: 15px; border: 2px solid #f59e0b;
        }
        .stealth-hud-corners::before { top: -1px; left: -1px; border-right: none; border-bottom: none; }
        .stealth-hud-corners::after { bottom: -1px; right: -1px; border-left: none; border-top: none; }
        .stealth-captcha-img { border-radius: 4px; }
        .stealth-captcha-input { background: rgba(0,0,0,0.5); border: 1px solid #f59e0b; color: #f59e0b; font-size: 1.5rem; letter-spacing: 8px; padding: 5px; outline: none; }
        .stealth-captcha-input:focus { box-shadow: 0 0 10px rgba(245, 158, 11, 0.5); }
        
        """
    c = c[:i3] + css_replacement + c[i4:]

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)
print('SUCCESS')
