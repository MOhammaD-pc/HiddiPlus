import io
import re

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

# We use regex to replace the function definition securely.

pattern = r'def hidify_sync_delete_user\(uuid: str\) -> dict:\s*""".*?return hidify_sync_request\("DELETE", f"/admin/user/\{uuid\}/"\)'

replacement = '''def hidify_sync_delete_user(uuid: str, reseller_id: int = None) -> dict:
    """حذف کاربر از سرور هیدیفای"""
    if not uuid:
        return {"error": "UUID نامعتبر است."}
    return hidify_sync_request("DELETE", f"/admin/user/{uuid}/", reseller_id=reseller_id)'''

c = re.sub(pattern, replacement, c, flags=re.DOTALL)

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED SIGNATURE")
