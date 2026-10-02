import io
import os
import glob

def fix_all_buttons():
    for filepath in glob.glob('d:/GitHub/TGBot/templates/*.html'):
        with io.open(filepath, 'r', encoding='utf-8') as f:
            c = f.read()
            
        old_c = c
        
        c = c.replace('class="btn btn-link p-0 text-decoration-none sub-note-btn', 'class="border-0 bg-transparent p-0 sub-note-btn')
        
        if c != old_c:
            with io.open(filepath, 'w', encoding='utf-8') as f:
                f.write(c)
            print(f"Fixed {os.path.basename(filepath)}")

fix_all_buttons()
print("DONE")
