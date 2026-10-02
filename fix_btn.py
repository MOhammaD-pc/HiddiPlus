import io

with io.open('d:/GitHub/TGBot/templates/payments.html', 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the classes on the tx note button
old_classes = 'class="btn btn-link p-0 text-decoration-none tx-note-btn {% if has_tx_note %}text-warning{% else %}text-muted opacity-50{% endif %}"'
new_classes = 'class="border-0 bg-transparent p-0 tx-note-btn {% if has_tx_note %}text-warning{% else %}text-muted opacity-50{% endif %}"'
c = c.replace(old_classes, new_classes)

with io.open('d:/GitHub/TGBot/templates/payments.html', 'w', encoding='utf-8') as f:
    f.write(c)

print("SUCCESS")
