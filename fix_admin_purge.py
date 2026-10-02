import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'def admin_subscription_purge\(sub_id\):.*?hidify_sync_delete_user\(uuid_val, reseller_id=reseller_id\)'

def replacer(m):
    return m.group(0).replace('reseller_id=reseller_id', 'reseller_id=sub.get("reseller_id")')

c = re.sub(pattern, replacer, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED admin_subscription_purge")
