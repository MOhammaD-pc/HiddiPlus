import io
import re

with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Remove the top captcha block which got injected into the subtitle
# It is between:
#   </div>
#   {% elif active_style == 'stealth_tactical' %}
# and
#   {% elif active_style == 'swiss_minimal' %}

# Let's find the exact block:
subtitle_start = "                    {% elif active_style == 'stealth_tactical' %}"
swiss_start = "                    {% elif active_style == 'swiss_minimal' %}"

if subtitle_start in c:
    # There could be multiple subtitle_starts (e.g., in other places).
    # We want the one that has the wrong captcha inside it.
    # The wrong captcha has `<div class="stealth-captcha-hud p-2`
    
    # Let's just use regex to replace the subtitle stealth tactical block
    # We know the subtitle block is inside `<p class="small mb-2 login-brand-subtitle opacity-75">`
    p_start_idx = c.find('<p class="small mb-2 login-brand-subtitle opacity-75">')
    p_end_idx = c.find('</p>', p_start_idx)
    
    if p_start_idx != -1 and p_end_idx != -1:
        p_block = c[p_start_idx:p_end_idx]
        
        # Replace the bad stealth block inside p_block
        bad_stealth_pattern = r"{% elif active_style == 'stealth_tactical' %}.*?(?={% elif active_style == 'swiss_minimal' %})"
        good_stealth = "{% elif active_style == 'stealth_tactical' %}\n                        سیستم دسترسی مجاز پرسنل\n                    "
        
        new_p_block = re.sub(bad_stealth_pattern, good_stealth, p_block, flags=re.DOTALL)
        c = c[:p_start_idx] + new_p_block + c[p_end_idx:]

with io.open('d:/GitHub/TGBot/templates/login.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED TOP CAPTCHA")
