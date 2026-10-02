import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix card border and background for swiss_minimal
css_fix = """
.login-theme-swiss_minimal .login-main-card {
    background: #111111 !important;
    border: none !important;
    box-shadow: none !important;
}
/* Autofill fix to remove yellow/blue backgrounds */
.login-theme-swiss_minimal input:-webkit-autofill,
.login-theme-swiss_minimal input:-webkit-autofill:hover, 
.login-theme-swiss_minimal input:-webkit-autofill:focus, 
.login-theme-swiss_minimal input:-webkit-autofill:active{
    -webkit-box-shadow: 0 0 0 30px #111111 inset !important;
    -webkit-text-fill-color: white !important;
    transition: background-color 5000s ease-in-out 0s;
}
"""
c = c.replace(".login-theme-swiss_minimal .login-main-card {\n    background: transparent !important;\n    box-shadow: none !important;\n}", css_fix)

# 2. Hide logo icon wrapper entirely for swiss_minimal
c = c.replace("{% elif active_style == 'swiss_minimal' %}\n                            <div class=\"w-100 h-100 d-flex align-items-center justify-content-center\" style=\"color: #fff; font-size: 2rem;\"><i class=\"fas fa-fingerprint\"></i></div>", "")
c = re.sub(r"{% if branding\.get\('logo_url'\) and active_style != 'swiss_minimal' %}", r"{% if active_style == 'swiss_minimal' %}<!-- No Logo Icon -->{% elif branding.get('logo_url') %}", c)
# Actually, the logo block is:
# <div class="login-brand-logo mb-3"> ... </div>
# Let's just hide the whole login-brand-logo in CSS for swiss_minimal!
css_fix2 = "\n.login-theme-swiss_minimal .login-brand-logo { display: none !important; }\n"
c = c.replace("/* NEUMORPHIC 3D RE-IMPLEMENTATION */", css_fix2 + "\n/* NEUMORPHIC 3D RE-IMPLEMENTATION */")

# 3. Fix the title text
c = c.replace("<span class='swiss-title'>AURA<br>Access</span>", "<span style='font-weight: 400; font-size: 1.8rem; letter-spacing: 0.5px;'>AURA<br>Access</span>")

# 4. Fix subtitle text
c = c.replace("<div class='swiss-subtitle text-start mt-4'>خوش آمدید.<br>برای ادامه وارد شوید.</div>", "<div class='text-center mt-5 mb-4' style='font-size: 1.1rem; font-weight: 400; letter-spacing: 0.2px;' dir='ltr'>Welcome back.<br><span style='color: #a1a1aa; font-size: 0.95rem;'>Sign in to continue.</span></div>")
# The user wants Persian but CSS and appearance like mockup!
# Mockup says "Welcome back. Sign in to continue." 
# The user specifically said: "دقت کن استایل css و ظاهر شبیه تصویر نهایی در بیاری"
# So let's make it Persian but same font sizes and weights!
persian_subtitle = "<div class='text-start mt-5 mb-4' style='font-size: 1.15rem; font-weight: 400; letter-spacing: 0.2px; font-family: -apple-system, sans-serif;' dir='rtl'>خوش آمدید.<br><span style='color: #a1a1aa; font-size: 0.95rem;'>برای ادامه وارد شوید.</span></div>"
c = re.sub(r"<div class='text-center mt-5 mb-4'.*?</div>", persian_subtitle, c) # If already replaced
c = c.replace("{% elif active_style == 'swiss_minimal' %}\n                        <div class='swiss-subtitle text-start mt-4'>خوش آمدید.<br>برای ادامه وارد شوید.</div>", "{% elif active_style == 'swiss_minimal' %}\n                        " + persian_subtitle)


with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED CSS AND HEADER")
