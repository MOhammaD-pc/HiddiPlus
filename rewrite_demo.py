import io
import re

def update_demo():
    with io.open('d:/GitHub/TGBot/static/login_concepts_demo.html', 'r', encoding='utf-8') as f:
        c = f.read()

    # CSS Replace
    css_old = r"/\* \u2502 \u06f5\. \u0645\u06cc\u0646\u06cc\u0645\u0627\u0644 \u0633\u0648\u0626\u06cc\u0633\u06cc \u2502 \*/.*?\.swiss-btn:hover \{ opacity: 0\.9; \}"
    # Let's just find the block and replace it manually.
    pass

update_demo()
