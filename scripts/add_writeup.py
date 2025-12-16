#!/usr/bin/env python3
"""
Script de conversion des writeups Notion HTML vers le format du site.
Usage: python3 add_writeup.py <fichier_notion.html> <nom_writeup> [description]

Exemple: python3 add_writeup.py "Chemistry 2b6aa764c45c80738533d461802da0d5.html" chemistry "CVE pymatgen, SQLite exfiltration"
"""

import sys
import os
import re
from pathlib import Path

# Chemins relatifs au script
SCRIPT_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPT_DIR.parent
WRITEUPS_DIR = PROJECT_ROOT / "writeups"
INDEX_FILE = WRITEUPS_DIR / "index.html"

# Template HTML pour les writeups
HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="fr" class="dark">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>{title} - Writeup HTB</title>
    <meta name="description" content="Writeup Hack The Box - {title}">

    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Zalando+Sans:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Zalando+Sans+Expanded:ital,wght@0,200..900;1,200..900&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="../../styles.css">
    <link rel="stylesheet" href="../writeups.css">
    <link rel="icon" type="image/jpeg" href="../../assets/favi.png">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-python.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-sql.min.js" defer></script>
</head>

<body class="writeups-mode">
    <nav class="navbar">
        <div class="container">
            <div class="nav-content">
                <a href="../../" class="nav-logo-link">
                    <img src="../../assets/c8e38298-4426-4ed7-ab6b-1c8c5c263f64 (1).png" class="nav-logo"
                        alt="logo signature Raphaël">
                </a>
                <div class="nav-links">
                    <a href="../../" class="nav-link">Accueil</a>
                    <a href="../../Portfolio/" class="nav-link">Portfolio</a>
                    <a href="../" class="nav-link active">Writeups</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="min-h-screen">
        <div class="writeups-container">
            <a href="../" class="back-link">← Retour aux writeups</a>
            <div class="writeup-content">
{content}
            </div>
        </div>
    </main>
</body>

</html>
'''

# Corrections orthographiques
SPELLING_FIXES = [
    (r"\bIl y a peut de\b", "Il y a peu de"),
    (r"\bpannel admiin\b", "panel admin"),
    (r"\bpannel\b", "panel"),
    (r"\bdonctionne\b", "fonctionne"),
    (r"\bca renvoie\b", "ça renvoie"),
    (r"\bca marche\b", "ça marche"),
    (r"\bca me met\b", "ça me met"),
    (r"\bappart\b", "à part"),
    (r"\bconnectan\b", "connectant"),
    (r"\ba l'interieur\b", "à l'intérieur"),
    (r"\byavais\b", "y avait"),
    (r"\bc'etait\b", "c'était"),
    (r"\bgenere\b", "génère"),
    (r"\bdecouvre\b", "découvre"),
    (r"\bcrquer\b", "craquer"),
    (r"\bon voi\b", "on voit"),
    (r"\bparceque\b", "parce que"),
    (r"\btout les\b", "tous les"),
    (r"\ben remplacant\b", "en remplaçant"),
    (r"\bapres\b", "après"),
    (r"\bdeja\b", "déjà"),
]


def extract_content(html_content):
    """Extrait le contenu de l'article Notion."""
    # Cherche le contenu de l'article
    match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL)
    if match:
        content = match.group(1)
    else:
        # Fallback: prend le body
        match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
        content = match.group(1) if match else html_content
    
    # Supprime les scripts Prism inline
    content = re.sub(r'<script[^>]*prism[^>]*></script>', '', content)
    content = re.sub(r'<link[^>]*prism[^>]*/>', '', content)
    
    # Supprime les liens vers d'autres pages Notion
    content = re.sub(r'<figure[^>]*class="[^"]*link-to-page[^"]*"[^>]*>.*?</figure>', '', content, flags=re.DOTALL)
    
    # Supprime les images cassées des bookmarks
    content = re.sub(r'<img[^>]*class="[^"]*bookmark-icon[^"]*"[^>]*/?>','', content)
    content = re.sub(r'<img src="[a-zA-Z0-9_-]+\.(png|jpg|jpeg|gif|webp)"[^>]*/?>','', content)
    
    # Corrige les chemins d'images
    content = re.sub(r'src="([^"]+)/([^"/]+\.(png|jpg|jpeg|gif|webp))"', r'src="\2"', content)
    
    return content


def fix_spelling(content):
    """Corrige les fautes d'orthographe courantes."""
    for pattern, replacement in SPELLING_FIXES:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content


def extract_title(html_content):
    """Extrait le titre de la page Notion."""
    match = re.search(r'<h1 class="page-title"[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if match:
        title = match.group(1).strip()
        # Supprime les tags HTML du titre
        title = re.sub(r'<[^>]+>', '', title).strip()
        return title
    return None


def add_to_index(name, title, description):
    """Ajoute le writeup à la page d'index."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Vérifie si le writeup existe déjà
    if f'href="{name}/"' in index_content:
        print(f"⚠️  Le writeup '{name}' existe déjà dans l'index")
        return False
    
    # Crée la nouvelle carte
    new_card = f'''
                <a href="{name}/" class="writeup-card">
                    <span class="htb-badge">HACK THE BOX</span>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </a>'''
    
    # Trouve la fin de la grille et insère avant
    pattern = r'(</div>\s*</div>\s*</main>)'
    replacement = new_card + r'\n            \1'
    
    new_index = re.sub(pattern, replacement, index_content)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_index)
    
    return True


def convert_writeup(input_file, name, description=None):
    """Convertit un fichier HTML Notion en writeup intégré."""
    input_path = Path(input_file)
    
    if not input_path.exists():
        print(f"❌ Fichier non trouvé: {input_file}")
        return False
    
    # Lit le fichier source
    with open(input_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extrait le titre
    title = extract_title(html_content) or name.capitalize()
    
    # Extrait et nettoie le contenu
    content = extract_content(html_content)
    content = fix_spelling(content)
    
    # Crée le dossier du writeup
    writeup_dir = WRITEUPS_DIR / name
    writeup_dir.mkdir(exist_ok=True)
    
    # Copie les images associées s'il y en a (dossier avec le même nom)
    source_images_dir = input_path.parent / input_path.stem.split()[0]
    if source_images_dir.exists() and source_images_dir.is_dir():
        import shutil
        for img in source_images_dir.iterdir():
            if img.suffix.lower() in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                shutil.copy2(img, writeup_dir / img.name)
                print(f"📷 Image copiée: {img.name}")
    
    # Génère le HTML final
    final_html = HTML_TEMPLATE.format(title=title, content=content)
    
    # Écrit le fichier
    output_path = writeup_dir / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Writeup créé: {output_path}")
    
    # Ajoute à l'index
    desc = description or f"Writeup {title}"
    if add_to_index(name, title, desc):
        print(f"✅ Ajouté à l'index des writeups")
    
    return True


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nArguments:")
        print("  <fichier_notion.html>  Chemin vers le fichier HTML exporté de Notion")
        print("  <nom_writeup>          Nom du dossier (lowercase, sans espaces)")
        print("  [description]          Description optionnelle pour l'index")
        sys.exit(1)
    
    input_file = sys.argv[1]
    name = sys.argv[2].lower().replace(' ', '-')
    description = sys.argv[3] if len(sys.argv) > 3 else None
    
    success = convert_writeup(input_file, name, description)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
