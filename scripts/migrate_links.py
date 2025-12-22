#!/usr/bin/env python3
"""
Script de migration pour mettre à jour les intégrations de liens dans les writeups existants.
Format cible : Ligne unique avec Favicon + Titre de la page.
"""

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

# Racines du projet
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WRITEUPS_DIR = PROJECT_ROOT / "writeups"

def get_domain(url):
    try:
        return urlparse(url).netloc
    except:
        return ""

def migrate_file(file_path):
    print(f"Checking {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    
    # Regex pour trouver les liens isolés dans un paragraphe
    # <p><a href="URL" ...>TITRE</a></p>
    # On capture l'URL (groupe 1) et le TITRE (groupe 2)
    # On ignore les liens relatifs (../../ etc) pour ne pas casser la nav
    
    pattern = r'(<p[^>]*>)\s*<a href="(http[^"]+)"[^>]*>([^<]+)</a>\s*</p>'
    
    def replacement(match):
        url = match.group(2)
        title = match.group(3)
        domain = get_domain(url)
        
        # Check if already migrated (simple check)
        # Mais ici on match <p><a>...</a></p>, donc ce n'est pas le format cible qui a une classe
        
        print(f"  -> Migrating link: {title} ({domain})")
        
        return f'''<p class="link-integration">
                        <img src="https://www.google.com/s2/favicons?domain={domain}&sz=64" class="site-favicon" alt="">
                        <a href="{url}" target="_blank" rel="noopener">{title}</a>
                    </p>'''

    new_content = re.sub(pattern, replacement, content)
    
    if new_content != original_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"✅ Updated {file_path}")
    else:
        print(f"  No changes needed for {file_path}")

def main():
    if not WRITEUPS_DIR.exists():
        print(f"Error: {WRITEUPS_DIR} not found.")
        sys.exit(1)
        
    print("Starting migration...")
    
    # Iterate over all index.html files in subdirectories of writeups
    for index_file in WRITEUPS_DIR.glob("*/index.html"):
        migrate_file(index_file)
        
    print("Migration complete.")

if __name__ == "__main__":
    main()
