import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Update hidify_sync_delete_user definition
def_old = 'def hidify_sync_delete_user(uuid: str) -> dict:\n    """??? ????? ?? ???? ???????"""\n    if not uuid:\n        return {"error": "UUID ??????? ???."}\n    return hidify_sync_request("DELETE", f"/admin/user/{uuid}/")'
def_new = 'def hidify_sync_delete_user(uuid: str, reseller_id: int = None) -> dict:\n    """??? ????? ?? ???? ???????"""\n    if not uuid:\n        return {"error": "UUID ??????? ???."}\n    return hidify_sync_request("DELETE", f"/admin/user/{uuid}/", reseller_id=reseller_id)'

c = c.replace(def_old, def_new)

# 2. Update usages in reseller routes.
# Find instances where reseller calls it.

c = c.replace('hidify_sync_delete_user(uuid_val)', 'hidify_sync_delete_user(uuid_val, reseller_id=reseller_id)')
c = c.replace('hidify_sync_delete_user(sub["hidify_uuid"])', 'hidify_sync_delete_user(sub["hidify_uuid"], reseller_id=reseller_id)')

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("UPDATED DASHBOARD.PY")
