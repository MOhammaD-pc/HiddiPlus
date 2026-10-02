import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace gateway name logic to include cash_reseller
old_res_manual = 'elif g in ("reseller_manual", "manual_reseller"):'
new_res_manual = 'elif g in ("reseller_manual", "manual_reseller", "cash_reseller"):'
c = c.replace(old_res_manual, new_res_manual)

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
