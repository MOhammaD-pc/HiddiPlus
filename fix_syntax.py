import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

bad_block = """                    {% if active_style == 'swiss_minimal' %}<!-- No Logo Icon -->{% elif branding.get('logo_url') %}
                        <div class="logo-wrapper d-inline-flex p-2 rounded-4 shadow-sm">
                            <img src="{{ branding.get('logo_url') }}" alt="????" style="max-height: 60px; max-width: 60px; object-fit: contain;">
                        </div>
                    {% else %}
                        <div class="logo-icon-wrapper d-inline-flex align-items-center justify-content-center rounded-4 shadow-sm" style="width: 64px; height: 64px;">
                            {% if active_style == 'cyber_neon' %}
                                <i class="fas fa-microchip fs-2 text-cyan"></i>
                            {% elif active_style == 'hacker_terminal' %}
                                <i class="fas fa-user-secret fs-2 text-success"></i>
                            {% elif active_style == 'ios_lockscreen' %}
                                <i class="fab fa-apple fs-2 text-secondary" style="color: #cbd5e1 !important; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));"></i>
                            {% elif active_style == 'neumorphic_3d' %}
                            <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; font-family: -apple-system, sans-serif;">
                                ورود به حساب کاربری
                            </div>
                        
                        {% elif active_style == 'swiss_minimal' %}<span style='font-weight: 400; font-size: 1.8rem; letter-spacing: 0.5px;'>AURA<br>Access</span>{% else %}{{ login_page_title or branding.get('brand_title') or 'پروکسی تلگرام VPN' }}{% endif %}
                </h4>"""

good_block = """                    {% if active_style == 'swiss_minimal' %}<!-- No Logo Icon -->{% elif branding.get('logo_url') %}
                        <div class="logo-wrapper d-inline-flex p-2 rounded-4 shadow-sm">
                            <img src="{{ branding.get('logo_url') }}" alt="لوگو" style="max-height: 60px; max-width: 60px; object-fit: contain;">
                        </div>
                    {% else %}
                        <div class="logo-icon-wrapper d-inline-flex align-items-center justify-content-center rounded-4 shadow-sm" style="width: 64px; height: 64px;">
                            {% if active_style == 'cyber_neon' %}
                                <i class="fas fa-microchip fs-2 text-cyan"></i>
                            {% elif active_style == 'hacker_terminal' %}
                                <i class="fas fa-user-secret fs-2 text-success"></i>
                            {% elif active_style == 'ios_lockscreen' %}
                                <i class="fab fa-apple fs-2 text-secondary" style="color: #cbd5e1 !important; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.3));"></i>
                            {% elif active_style == 'neumorphic_3d' %}
                                <div class="w-100 h-100 d-flex align-items-center justify-content-center" style="font-weight: 700; font-size: 1.1rem; color: #f8fafc; font-family: -apple-system, sans-serif;">
                                    ورود
                                </div>
                            {% else %}
                                <i class="fas fa-shield-alt fs-2 text-primary"></i>
                            {% endif %}
                        </div>
                    {% endif %}
                </div>
                
                <h4 class="fw-black mb-1 login-brand-title">
                    {% if active_style == 'hacker_terminal' %}
                        <span class="font-monospace text-success">[ AUTH_SYS_V2.0 ]</span>
                    {% elif active_style == 'swiss_minimal' %}<span style='font-weight: 400; font-size: 1.8rem; letter-spacing: 0.5px;'>AURA<br>Access</span>{% else %}{{ login_page_title or branding.get('brand_title') or 'پروکسی تلگرام VPN' }}{% endif %}
                </h4>"""

# Since utf-8 reading might have ??? for persian, we use regex with dotall
c = re.sub(r"{% if active_style == 'swiss_minimal' %}<!-- No Logo Icon -->.*?</h4>", good_block, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED SYNTAX")
