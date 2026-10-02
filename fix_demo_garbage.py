import io
import re

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
    c = f.read()

# We need to remove the garbage that was left over between the end of the newly injected tab-stealth
# and the beginning of the NEXT tab (tab-swiss).

new_stealth_end = '              </div>\n          </div>'
swiss_start = '          <!-- ۷. مینیمال سوئیسی -->'

if new_stealth_end in c and swiss_start in c:
    start_idx = c.find(new_stealth_end) + len(new_stealth_end)
    end_idx = c.find(swiss_start)
    
    # Check if there is garbage in between
    garbage = c[start_idx:end_idx]
    if 'stealth-input-wrapper' in garbage:
        # We need to wipe it out
        c = c[:start_idx] + "\n          \n" + c[end_idx:]

with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED DEMO FILE LEFTOVERS")
