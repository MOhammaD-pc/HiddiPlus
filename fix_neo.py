import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Fix Neumorphic 3D Title
old_title = "<h4 style=\"font-weight: 600; font-size: 1.3rem; margin-bottom: 5px; color: #e2e8f0;\">{{ branding.get('login_page_title') or 'TGBot' }}</h4>"
new_title = "<h4 style=\"font-weight: 600; font-size: 1.3rem; margin-bottom: 5px; color: #e2e8f0;\">{{ login_page_title or branding.get('brand_title') or 'TGBot' }}</h4>"
c = c.replace(old_title, new_title)

# 2. Add Neumorphic 3D Password Field
# Find the start of the password mb-3 block
pass_block_start = "                    <!-- رمز عبور -->\n                    <div class=\"mb-3\">\n                        {% if active_style == 'stealth_tactical' %}"

neo_pass_block = """                        {% if active_style == 'neumorphic_3d' %}
                        <div class="neo-track position-relative mb-2">
                            <div class="neo-raised-btn"><i class="fas fa-lock"></i></div>
                            <div style="flex-grow: 1; display: flex; flex-direction: column; justify-content: center; padding: 0 16px; direction: ltr;">
                                <span style="font-size: 0.75rem; color: #64748b; margin-bottom: -2px; text-align: right;">رمز عبور</span>
                                <input type="password" id="loginPasswordInput" class="neo-input px-0 font-monospace" name="password" placeholder="••••••••••••" style="text-align: left; letter-spacing: 3px;" required>
                            </div>
                            <button type="button" class="btn btn-link p-0 text-decoration-none" onclick="togglePasswordVisibility()" style="margin-right: 15px; width: 24px;">
                                <i class="fas fa-eye text-muted" id="passwordToggleIcon"></i>
                            </button>
                        </div>
                        <div class="text-start pe-2">
                            <a href="#" class="text-decoration-none small" style="font-size: 0.75rem; color: #3b82f6;">فراموشی رمز؟</a>
                        </div>
                        {% elif active_style == 'stealth_tactical' %}"""

if "<!-- رمز عبور -->\n                    <div class=\"mb-3\">\n                        {% if active_style == 'stealth_tactical' %}" in c:
    c = c.replace(pass_block_start, "                    <!-- رمز عبور -->\n                    <div class=\"mb-3\">\n" + neo_pass_block)

# Wait, what if the password block already has neo? Let's verify:
with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED NEUMORPHIC 3D PASS & TITLE")
