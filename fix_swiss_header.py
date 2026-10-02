import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix the logo icon wrapper
# Find the swiss_minimal block inside the logo-icon-wrapper
old_logo = """{% elif active_style == 'swiss_minimal' %}
                            <div class="w-100 bg-white text-black d-flex align-items-center justify-content-center" style="font-size: 1.2rem; font-family: -apple-system, sans-serif; font-weight: 400; padding: 12px 0;">
                                ورود
                            </div>"""
c = c.replace(old_logo, "{% elif active_style == 'swiss_minimal' %}\n                            <div class=\"w-100 h-100 d-flex align-items-center justify-content-center\" style=\"color: #fff; font-size: 2rem;\"><i class=\"fas fa-fingerprint\"></i></div>")

# 2. Fix the login brand title for swiss_minimal
# It currently has: {% elif active_style == 'swiss_minimal' %}AURA<br>Access{% else %}
# This is fine, but maybe let's make it look like the mockup (not bold, thinner font)
# Actually, the user wants exact CSS matches. I'll add a class to target it in CSS.
c = c.replace("{% elif active_style == 'swiss_minimal' %}AURA<br>Access{% else %}", "{% elif active_style == 'swiss_minimal' %}<span class='swiss-title'>AURA<br>Access</span>{% else %}")

# 3. Fix the subtitle
# Currently: {% elif active_style == 'swiss_minimal' %} خوش آمدید.<br>جهت ورود مشخصات خود را وارد کنید. {% else %}
c = c.replace("{% elif active_style == 'swiss_minimal' %}\n                        خوش آمدید.<br>جهت ورود مشخصات خود را وارد کنید.", "{% elif active_style == 'swiss_minimal' %}\n                        <div class='swiss-subtitle text-start mt-4'>خوش آمدید.<br>برای ادامه وارد شوید.</div>")

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)
print("FIXED HEADER")
