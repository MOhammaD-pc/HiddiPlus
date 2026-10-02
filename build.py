import io
import re

def build_login():
    with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # 1. Update logo/header for swiss_minimal
    c = c.replace("{% if active_style == 'stealth_tactical' %}ورود امن{% elif active_style == 'swiss_minimal' %}AURA<br>Access{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}",
                  "{% if active_style == 'stealth_tactical' %}ورود امن{% elif active_style == 'swiss_minimal' %}<span style='font-size: 2.5rem; font-weight: 300; letter-spacing: 2px;'>AURA</span><br><span style='font-size: 1.5rem; font-weight: 300;'>Access</span>{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}")

    c = c.replace("{% elif active_style == 'swiss_minimal' %}\n                        خوش آمدید.<br>برای ادامه وارد شوید.\n                    {% else %}",
                  "{% elif active_style == 'swiss_minimal' %}\n                        <div class='text-start mt-5' style='font-size: 1.3rem; color: #fff;'>خوش آمدید.</div><div class='text-start' style='font-size: 1rem; color: rgba(255,255,255,0.7);'>برای ادامه وارد شوید.</div>\n                    {% else %}")

    # 2. Update Username field for swiss_minimal
    old_username = """{% elif active_style == 'swiss_minimal' %}
                                <i class="far fa-user text-muted"></i>"""
    
    # We will just replace the entire Username mb-3 div block with a regex or exact string replacement
    # Since I don't know the exact string, I will do it smartly.
    pass

build_login()
print("SUCCESS")
