import io
import re

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace CSS
css_new = """/* ۳. سه‌بعدی نئومورفیک */
        .theme-neumorphic {
            background: #2a2d34;
            border-radius: 40px;
            padding: 40px 25px;
            box-shadow: 12px 12px 24px rgba(0,0,0,0.4), -12px -12px 24px rgba(255,255,255,0.06);
            color: #cbd5e1;
        }
        .neo-header { text-align: center; margin-bottom: 30px; }
        .neo-logo-icon {
            width: 60px; height: 60px; margin: 0 auto 15px auto;
            background: #2a2d34; border-radius: 15px;
            box-shadow: 6px 6px 12px rgba(0,0,0,0.4), -6px -6px 12px rgba(255,255,255,0.06);
            display: flex; align-items: center; justify-content: center; font-size: 1.8rem; color: #cbd5e1;
        }
        .neo-track {
            background: #2a2d34;
            border-radius: 20px;
            box-shadow: inset 6px 6px 12px rgba(0,0,0,0.4), inset -6px -6px 12px rgba(255,255,255,0.04);
            height: 64px;
            display: flex; align-items: center; padding: 8px; margin-bottom: 24px;
        }
        .neo-raised-btn {
            width: 48px; height: 48px;
            background: #2a2d34; border-radius: 14px;
            box-shadow: 4px 4px 8px rgba(0,0,0,0.4), -4px -4px 8px rgba(255,255,255,0.06);
            display: flex; align-items: center; justify-content: center; color: #94a3b8; flex-shrink: 0;
        }
        .neo-input {
            background: transparent; border: none; outline: none;
            color: #e2e8f0; font-size: 1rem; padding: 0 16px; width: 100%;
        }
        .neo-input::placeholder { color: #64748b; }
        .neo-submit {
            width: 100%; height: 60px; margin-top: 10px;
            background: #2a2d34; border-radius: 16px; border: none;
            box-shadow: 6px 6px 12px rgba(0,0,0,0.4), -6px -6px 12px rgba(255,255,255,0.06);
            color: #f8fafc; font-weight: 700; font-size: 1.1rem; cursor: pointer; transition: all 0.2s;
            display: flex; align-items: center; justify-content: center;
        }
        .neo-submit:active {
            box-shadow: inset 4px 4px 8px rgba(0,0,0,0.4), inset -4px -4px 8px rgba(255,255,255,0.06);
            color: #cbd5e1;
        }"""
c = re.sub(r"/\* \u06f3\. \u0633\u0647\u200c\u0628\u0639\u062f\u06cc \u0646\u0626\u0648\u0645\u0648\u0631\u0641\u06cc\u06a9 \*/.*?.neu-submit-btn:active \{.*?\}", css_new, c, flags=re.DOTALL)

# HTML Replace
html_new = """<!-- ۳. سه‌بعدی نئومورفیک -->
        <div class="theme-container theme-neumorphic" id="tab-neu" dir="ltr">
            <div class="neo-header">
                <div class="neo-logo-icon">
                    <i class="fas fa-cube"></i>
                </div>
                <h4 style="font-weight: 600; font-size: 1.3rem; margin-bottom: 5px; color: #e2e8f0;">NEXUS</h4>
                <div style="font-size: 1.15rem; font-weight: 500; margin-bottom: 5px;">ورود به حساب کاربری</div>
                <div style="font-size: 0.9rem; color: #64748b;">خوش آمدید</div>
            </div>
            
            <div class="neo-track">
                <div class="neo-raised-btn">
                    <i class="fas fa-user"></i>
                </div>
                <input type="text" class="neo-input font-monospace" placeholder="نام کاربری |" style="direction: rtl; text-align: left;">
            </div>
            
            <div class="neo-track">
                <div class="neo-raised-btn">
                    <i class="fas fa-lock"></i>
                </div>
                <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                    <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">رمز عبور</span>
                    <input type="password" class="neo-input px-0 font-monospace" placeholder="••••••••" style="text-align: left;">
                </div>
                <i class="fas fa-eye-slash" style="color: #64748b; margin-right: 15px; cursor: pointer;"></i>
            </div>
            
            <div style="display: flex; gap: 16px; margin-bottom: 24px;">
                <div class="neo-track" style="flex-grow: 1; position: relative; margin: 0; overflow: hidden; padding: 0;">
                    <div style="position: absolute; width: 100%; height: 100%; top: 0; left: 0; mix-blend-mode: multiply; opacity: 0.7; filter: contrast(1.5);">
                        <div style="width: 100%; height: 100%; background: #fff; display: flex; align-items: center; justify-content: center; font-family: monospace; font-size: 2rem; letter-spacing: 0.8rem; font-weight: bold; color: #000; padding-left: 0.8rem;">49271</div>
                    </div>
                    <input type="text" class="neo-input font-monospace text-center" style="position: relative; width: 100%; height: 100%; font-size: 2rem; letter-spacing: 1.2rem; font-weight: bold; text-shadow: -1px -1px 2px rgba(255,255,255,0.1), 1px 1px 2px rgba(0,0,0,0.8); background: transparent; padding-left: 1.2rem;" placeholder="     ">
                </div>
                <div class="neo-raised-btn" style="width: 64px; height: 64px; border-radius: 50%; margin: 0; cursor: pointer;">
                    <i class="fas fa-redo"></i>
                </div>
            </div>
            
            <button class="neo-submit">ورود</button>
            
            <div style="text-align: center; margin-top: 30px; font-size: 0.85rem; color: #64748b;">
                <div style="margin-bottom: 8px; cursor: pointer;">فراموشی رمز؟</div>
                <div>حساب کاربری ندارید؟ <span style="color: #cbd5e1; cursor: pointer;">ثبت نام</span></div>
            </div>
        </div>
"""
c = re.sub(r"<!-- \u06f3\. \u0633\u0647\u200c\u0628\u0639\u062f\u06cc \u0646\u0626\u0648\u0645\u0648\u0631\u0641\u06cc\u06a9 -->.*?</div>\s+</div>", html_new, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
