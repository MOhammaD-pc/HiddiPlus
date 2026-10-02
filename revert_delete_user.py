import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Revert signature
c = re.sub(
    r'def hidify_sync_delete_user\(uuid: str, reseller_id: int = None\) -> dict:',
    r'def hidify_sync_delete_user(uuid: str) -> dict:',
    c
)

c = re.sub(
    r'return hidify_sync_request\("DELETE", f"/admin/user/\{uuid\}/", reseller_id=reseller_id\)',
    r'return hidify_sync_request("DELETE", f"/admin/user/{uuid}/")',
    c
)

# 2. Revert calls
c = re.sub(r'hidify_sync_delete_user\(([^,]+),\s*reseller_id=[^\)]+\)', r'hidify_sync_delete_user(\1)', c)

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("REVERTED")
