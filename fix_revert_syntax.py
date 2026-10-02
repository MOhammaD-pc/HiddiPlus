import io

with io.open('d:/GitHub/TGBot/dashboard.py', 'r', encoding='utf-8') as f:
    c = f.read()

c = c.replace('hidify_sync_delete_user(uuid_val))', 'hidify_sync_delete_user(uuid_val)')
c = c.replace('hidify_sync_delete_user(sub["hidify_uuid"]))', 'hidify_sync_delete_user(sub["hidify_uuid"])')
c = c.replace('hidify_sync_delete_user(uuid) if sub else None)', 'hidify_sync_delete_user(uuid)')

with io.open('d:/GitHub/TGBot/dashboard.py', 'w', encoding='utf-8') as f:
    f.write(c)

print("FIXED SYNTAX")
