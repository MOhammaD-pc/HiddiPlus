import io
import re

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

stealth_tab = """        <div class="theme-container theme-stealth" id="tab-stealth" dir="ltr" style="background: #0a0a0a; background-image: linear-gradient(rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(255, 255, 255, 0.03) 1px, transparent 1px); background-size: 10px 10px; padding: 40px 24px; min-height: 700px; color: #cbd5e1;">
            <div class="text-center mb-4 mt-2" style="text-align: center; margin-bottom: 2rem;">
                <h4 style="font-weight: 800; font-size: 1.4rem; letter-spacing: 2px; color: #e2e8f0; margin-bottom: 10px;">SECURE LOGIN</h4>
                <div style="display: inline-flex; align-items: center; justify-content: center; gap: 8px; border: 1px dashed rgba(255,255,255,0.2); padding: 5px 15px; border-radius: 4px; border-left: 2px solid #3b82f6; border-right: 2px solid #3b82f6;">
                    <i class="fas fa-fingerprint text-info" style="font-size: 1.25rem; color: #0dcaf0;"></i>
                    <div style="font-size: 0.75rem; color: #94a3b8; font-family: monospace; text-align: left; line-height: 1.2;">
                        ACCESS GRANTED ONLY TO<br>AUTHORIZED PERSONNEL
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 1rem; display: flex; height: 64px; background: linear-gradient(to bottom, #4a4e59, #2b2e35); padding: 3px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                <div style="width: 65px; height: 100%; display: flex; align-items: center; justify-content: center; background: linear-gradient(to bottom, #3a3d45, #1c1e22); border-right: 2px solid #1c1e22; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 25% 100%, 0% 50%); flex-shrink: 0;">
                    <i class="fas fa-user" style="color: #f59e0b; font-size: 1.5rem; text-shadow: 0 0 10px rgba(245, 158, 11, 0.6);"></i>
                </div>
                <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 2px, transparent 2px, transparent 4px);">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; margin-bottom: -2px; letter-spacing: 1px; text-align: left;">شناسه کاربری (USERNAME)</div>
                    <input type="text" placeholder="OPERATIVE-97" style="background: transparent; border: none; outline: none; color: #f59e0b; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 5px rgba(245, 158, 11, 0.4); width: 100%; direction: ltr; text-align: left;">
                </div>
            </div>
            
            <div style="margin-bottom: 1rem; display: flex; height: 64px; background: linear-gradient(to bottom, #4a4e59, #2b2e35); padding: 3px; border-radius: 8px; box-shadow: 0 5px 15px rgba(0,0,0,0.5); clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px);">
                <div style="width: 65px; height: 100%; display: flex; align-items: center; justify-content: center; background: linear-gradient(to bottom, #3a3d45, #1c1e22); border-right: 2px solid #1c1e22; clip-path: polygon(25% 0%, 100% 0%, 100% 100%, 25% 100%, 0% 50%); flex-shrink: 0;">
                    <i class="fas fa-lock" style="color: #f59e0b; font-size: 1.5rem; text-shadow: 0 0 10px rgba(245, 158, 11, 0.6);"></i>
                </div>
                <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; background: repeating-linear-gradient(45deg, rgba(0,0,0,0.05), rgba(0,0,0,0.05) 2px, transparent 2px, transparent 4px);">
                    <div style="font-size: 0.65rem; font-weight: 700; color: #94a3b8; margin-bottom: -2px; letter-spacing: 1px; text-align: left;">رمز عبور (PASSWORD)</div>
                    <input type="password" placeholder="••••••••••••" style="background: transparent; border: none; outline: none; color: #f59e0b; font-weight: 700; font-size: 1.1rem; text-shadow: 0 0 5px rgba(245, 158, 11, 0.4); width: 100%; direction: ltr; text-align: left; letter-spacing: 3px;">
                </div>
            </div>
            
            <div style="text-align: center; margin-bottom: 0.25rem; margin-top: 1.5rem;">
                <div style="font-size: 0.7rem; font-weight: 700; color: #94a3b8; letter-spacing: 2px;">کد امنیتی (VERIFICATION CODE)</div>
            </div>
            <div style="padding: 8px; position: relative; display: flex; flex-direction: column; align-items: center; border: 2px solid #f59e0b; box-shadow: 0 0 10px rgba(245, 158, 11, 0.2), inset 0 0 10px rgba(245, 158, 11, 0.2); border-radius: 4px; margin-bottom: 1.5rem; background: rgba(245, 158, 11, 0.05);">
                <div style="position: absolute; top: -2px; left: -2px; width: 15px; height: 15px; border-top: 3px solid #fff; border-left: 3px solid #fff;"></div>
                <div style="position: absolute; top: -2px; right: -2px; width: 15px; height: 15px; border-top: 3px solid #fff; border-right: 3px solid #fff;"></div>
                <div style="position: absolute; bottom: -2px; left: -2px; width: 15px; height: 15px; border-bottom: 3px solid #fff; border-left: 3px solid #fff;"></div>
                <div style="position: absolute; bottom: -2px; right: -2px; width: 15px; height: 15px; border-bottom: 3px solid #fff; border-right: 3px solid #fff;"></div>
                
                <div style="display: flex; width: 100%; justify-content: center; align-items: center; height: 50px; cursor: pointer;">
                    <img src="https://via.placeholder.com/150x50/ffffff/000000?text=4+B+7+X+9" style="height: 100%; filter: invert(1) sepia(1) saturate(5) hue-rotate(350deg) brightness(1.2) contrast(1.5);">
                    <i class="fas fa-rotate text-warning opacity-75 fs-5" style="margin-left: 1rem; color: #ffc107; opacity: 0.75; font-size: 1.25rem;"></i>
                </div>
                <div style="margin-top: 0.5rem; width: 100%; display: flex; justify-content: center; padding: 0 1rem; margin-bottom: 0.25rem;">
                    <input type="text" style="background: rgba(0,0,0,0.5); border: 1px solid rgba(245, 158, 11, 0.3); color: #fff; font-size: 1.5rem; font-family: monospace; letter-spacing: 10px; text-align: center; width: 100%; outline: none; padding: 2px;" placeholder="[ TYPE CODE ]">
                </div>
            </div>
            
            <button style="width: 100%; background: transparent; border: none; padding: 0; border-bottom: 4px solid #cc0000; border-radius: 8px; clip-path: polygon(15px 0, calc(100% - 15px) 0, 100% 15px, 100% calc(100% - 15px), calc(100% - 15px) 100%, 15px 100%, 0 calc(100% - 15px), 0 15px); box-shadow: 0 5px 15px rgba(0,0,0,0.6); cursor: pointer; margin-bottom: 1.5rem;">
                <div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; background: linear-gradient(to bottom, #7a8293, #434853); padding: 12px 0;">
                    <span style="font-weight: 900; font-size: 1.4rem; letter-spacing: 4px; color: #111; text-shadow: 1px 1px 0px rgba(255,255,255,0.3);">تایید هویت</span>
                </div>
            </button>
            
            <div style="text-align: center;">
                <span style="font-size: 0.8rem; font-weight: 700; color: #94a3b8; letter-spacing: 1px;">FORGOT CREDENTIALS? | CONTACT COMMAND</span>
            </div>
        </div>"""

c = re.sub(r'<div class="theme-container theme-stealth" id="tab-stealth">.*?</div>\s*</div>', stealth_tab, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED DEMO STEALTH")
