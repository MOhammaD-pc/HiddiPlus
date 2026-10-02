import io
import re

def update_demo():
    with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # Apply same CSS
    css_old = """.theme-swiss-minimal {
            background: rgba(255, 255, 255, 0.95);"""
    # Wait, the demo file has standalone CSS classes like `.theme-swiss-minimal` instead of `.login-theme-swiss_minimal`.
    
update_demo()
