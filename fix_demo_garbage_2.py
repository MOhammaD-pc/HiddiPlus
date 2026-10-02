import io
import re

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Let's find where FORGOT CREDENTIALS is.
# That is the end of the NEW stealth block.
forgot_marker = "FORGOT CREDENTIALS? | CONTACT COMMAND</span>\n              </div>\n          </div>"
swiss_marker = "<!-- ۷. مینیمال سوئیسی -->"

if forgot_marker in c and swiss_marker in c:
    start_idx = c.find(forgot_marker) + len(forgot_marker)
    end_idx = c.find(swiss_marker)
    
    # Check if there is garbage (like 'stealth-captcha-wrapper')
    garbage = c[start_idx:end_idx]
    if 'stealth-captcha-wrapper' in garbage:
        c = c[:start_idx] + "\n          \n          " + c[end_idx:]

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED DEMO GARBAGE WITH BETTER SCRIPT")
