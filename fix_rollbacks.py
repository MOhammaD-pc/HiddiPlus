import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

pattern = r'def revoke_reseller_payment\(payment_id\):.*?rollback_sub_action == "delete":\s*hidify_sync_delete_user\(uuid\)'
# Wait, the route name might be different. Let's just find `hidify_sync_delete_user(uuid)` and see if it's in a reseller block.

c = c.replace('elif rollback_sub_action == "delete":\n            hidify_sync_delete_user(uuid)', 'elif rollback_sub_action == "delete":\n            hidify_sync_delete_user(uuid, reseller_id=sub.get("reseller_id") if sub else None)')

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED ROLLBACK DELETIONS")
