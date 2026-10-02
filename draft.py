import io
import re

def update_login_neo():
    with io.open('d:/GitHub/TGBot/templates/login.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # Disable theme toggle for neumorphic_3d
    c = c.replace("{% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal'] %}", 
                  "{% if active_style not in ['hacker_terminal', 'stealth_tactical', 'swiss_minimal', 'neumorphic_3d'] %}")

    # Remove the generic neumorphic CSS and inject specific ones.
    # To do this safely, I will append my new CSS block right before </style> if there is a style block, or just at the top of the file.
    # Actually, the CSS is in static/css/style.css or inline? It's inline in login.html.
    pass

update_login_neo()
