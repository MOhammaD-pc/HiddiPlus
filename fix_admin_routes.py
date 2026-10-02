import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

# I need to fix admin_trash_bulk
# Specifically, around line 9148.

pattern = r'def admin_trash_bulk\(\):.*?elif action == "purge":.*?hidify_sync_delete_user\(sub\["hidify_uuid"\], reseller_id=reseller_id\).*?db\.purge_subscription_permanently\(sub_id\)'

def replacer(m):
    return m.group(0).replace('reseller_id=reseller_id', 'reseller_id=sub.get("reseller_id")')

c = re.sub(pattern, replacer, c, flags=re.DOTALL)


# What about `admin_delete_subscription`? Does it use `reseller_id=reseller_id`?
pattern2 = r'def admin_delete_subscription\(\):.*?hidify_sync_delete_user\(uuid_val, reseller_id=reseller_id\)'
def replacer2(m):
    return m.group(0).replace('reseller_id=reseller_id', 'reseller_id=sub_row.get("reseller_id")' if 'sub_row' in m.group(0) else 'reseller_id=None')

c = re.sub(pattern2, replacer2, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED ADMIN ROUTES")
