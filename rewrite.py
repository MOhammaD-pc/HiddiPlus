import io
import re

def rewrite_swiss_minimal(file_path):
    with io.open(file_path, 'r', encoding='utf-8') as f:
        c = f.read()

    # Disable theme toggle for swiss_minimal
    c = c.replace("{% if active_style not in ['hacker_terminal', 'stealth_tactical'] %}", "{% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal'] %}")
    
    # Hide header and change text for swiss_minimal
    header_old = '''{% if active_style == 'stealth_tactical' %}ورود امن{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}'''
    header_new = '''{% if active_style == 'stealth_tactical' %}ورود امن{% elif active_style == 'swiss_minimal' %}AURA<br>Access{% else %}{{ login_page_title or branding.get('brand_title') or 'سامانه هوشمند VPN' }}{% endif %}'''
    c = c.replace(header_old, header_new)

    sub_old = '''{% if active_style == 'hacker_terminal' %}
                        AUTHENTICATION // ENCRYPTED ACCESS ONLY
                    {% elif active_style == 'stealth_tactical' %}
                        دسترسی فقط برای پرسنل مجاز
                    {% else %}
                        {{ login_page_subtitle or 'ورود مدیران و همکاران فروش' }}
                    {% endif %}'''
    sub_new = '''{% if active_style == 'hacker_terminal' %}
                        AUTHENTICATION // ENCRYPTED ACCESS ONLY
                    {% elif active_style == 'stealth_tactical' %}
                        دسترسی فقط برای پرسنل مجاز
                    {% elif active_style == 'swiss_minimal' %}
                        خوش آمدید.<br>برای ادامه وارد شوید.
                    {% else %}
                        {{ login_page_subtitle or 'ورود مدیران و همکاران فروش' }}
                    {% endif %}'''
    c = c.replace(sub_old, sub_new)
    
    # Add custom classes for swiss_minimal inputs
    
    with io.open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)

rewrite_swiss_minimal('d:/GitHub/TGBot/templates/login.html')
print("SUCCESS")
