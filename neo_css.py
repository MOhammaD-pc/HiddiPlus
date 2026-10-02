import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Hide generic toggles
c = c.replace("{% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal'] %}", 
              "{% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal', 'neumorphic_3d'] %}")

# 2. Add custom CSS at the end of style block
neo_css = """
/* NEUMORPHIC 3D RE-IMPLEMENTATION */
.login-theme-neumorphic_3d { background: #2a2d34 !important; }
.login-theme-neumorphic_3d .login-main-card {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    padding: 0 !important;
}
.login-theme-neumorphic_3d .login-card-header { display: none !important; }
.neo-wrapper {
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
}
.neo-submit:active {
    box-shadow: inset 4px 4px 8px rgba(0,0,0,0.4), inset -4px -4px 8px rgba(255,255,255,0.06);
    color: #cbd5e1;
}
</style>
"""
c = c.replace("</style>", neo_css)

# 3. HTML modifications
# Replace the form entirely for neumorphic_3d
# Wait, I need to inject the neo-wrapper BEFORE the form or wrap the form.
# The card has `login-main-card`. Inside it is the form.
# I will just write the custom blocks in the jinja template!

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
