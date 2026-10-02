import io
import re

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace CSS
c = re.sub(
    r"/\* \u2502 \u06f5\. \u0645\u06cc\u0646\u06cc\u0645\u0627\u0644 \u0633\u0648\u0626\u06cc\u0633\u06cc \u2502 \*/.*?\.swiss-btn:hover \{ opacity: 0\.9; \}",
    """/* 5. مینیمال سوئیسی */
        .theme-swiss {
            background: #111111;
            padding: 40px 20px;
            color: #ffffff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            text-align: left;
            border-radius: 40px;
        }
        .swiss-input-group {
            margin-bottom: 2rem;
            position: relative;
        }
        .swiss-label-row {
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 4px;
        }
        .swiss-label-row span {
            font-size: 0.85rem;
            letter-spacing: 0.5px;
            padding-bottom: 2px;
            padding-right: 12px;
            padding-left: 4px;
        }
        .swiss-input-row {
            display: flex;
            align-items: center;
            border-bottom: 1px solid rgba(255,255,255,0.3);
            padding-bottom: 2px;
        }
        .swiss-input-row.focused {
            border-bottom: 2px solid #ffffff;
        }
        .swiss-input-row input {
            background: transparent;
            border: none;
            color: #ffffff;
            font-size: 1.25rem;
            width: 100%;
            outline: none;
            font-family: monospace;
        }
        .swiss-input-row i {
            opacity: 0.75;
            margin-left: 8px;
            margin-right: 16px;
            font-size: 1.25rem;
        }
        .swiss-captcha-box {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding: 0 8px;
        }
        .swiss-captcha-display {
            height: 55px;
            background: transparent;
            font-size: 2rem;
            letter-spacing: 1.5rem;
            font-family: monospace;
            font-weight: bold;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .swiss-captcha-input-row {
            border: none;
            background-image: repeating-linear-gradient(to left, transparent 0, transparent 15px, rgba(255,255,255,0.3) 15px, rgba(255,255,255,0.3) 55px);
            background-size: 55px 1px;
            background-position: bottom center;
            background-repeat: repeat-x;
            padding-bottom: 5px;
        }
        .swiss-captcha-input-row input {
            text-align: center;
            font-size: 2.2rem;
            letter-spacing: 1.8rem;
            direction: ltr;
        }
        .swiss-btn {
            width: 100%;
            background: #ffffff;
            color: #000000;
            padding: 12px;
            font-size: 1.2rem;
            font-weight: 500;
            border: none;
            cursor: pointer;
        }""",
    c, flags=re.DOTALL
)

# Replace HTML
c = re.sub(
    r"<!-- \u06f5\. \u0645\u06cc\u0646\u06cc\u0645\u0627\u0644 \u0633\u0648\u0626\u06cc\u0633\u06cc -->.*?</div>\s+</div>",
    """<!-- ۵. مینیمال سوئیسی -->
        <div class="theme-container theme-swiss" id="tab-swiss" dir="ltr">
            <div style="margin-bottom: 40px;">
                <span style="font-size: 2.8rem; font-weight: 300; letter-spacing: 1px; display: block; margin-bottom: -5px;">AURA</span>
                <span style="font-size: 1.5rem; font-weight: 300;">Access</span>
                
                <div style="margin-top: 50px; font-size: 1.5rem;">Welcome back.</div>
                <div style="font-size: 1.1rem; color: rgba(255,255,255,0.7);">Sign in to continue.</div>
            </div>
            
            <div class="swiss-input-group">
                <div class="swiss-label-row">
                    <span>Username</span>
                    <div style="flex-grow: 1;"></div>
                </div>
                <div class="swiss-input-row focused">
                    <i class="far fa-user"></i>
                    <input type="text" placeholder="username">
                </div>
            </div>
            
            <div class="swiss-input-group" style="margin-bottom: 3rem;">
                <div class="swiss-label-row">
                    <span>Password</span>
                    <div style="flex-grow: 1;"></div>
                </div>
                <div class="swiss-input-row">
                    <i class="fas fa-lock" style="opacity: 0.5;"></i>
                    <input type="password" placeholder="••••••••">
                </div>
            </div>
            
            <div class="swiss-input-group">
                <div class="swiss-captcha-box">
                    <div class="swiss-captcha-display">
                        7 4 9 2 5
                    </div>
                    <i class="fas fa-rotate-right" style="font-size: 1.5rem; opacity: 0.5; font-weight: 300; cursor: pointer;"></i>
                </div>
                <div class="swiss-captcha-input-row">
                    <input type="text" placeholder="     " value="">
                </div>
                <div style="margin-top: 8px;">
                    <span style="font-size: 0.85rem; opacity: 0.5;">Captcha Code</span>
                </div>
            </div>
            
            <button class="swiss-btn" style="margin-top: 10px;">Sign In</button>
            
            <div style="text-align: center; margin-top: 25px;">
                <span style="font-size: 0.9rem; opacity: 0.5; cursor: pointer;">Forgot password?</span>
            </div>
        </div>
    </div>""",
    c, flags=re.DOTALL
)

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
