#!/usr/bin/env python3
"""
Script de conversion des writeups Notion HTML vers le format du site.

Usage: 
    python3 add_writeup.py <dossier_export_notion> <nom_writeup> [description]

Exemple: 
    python3 add_writeup.py "ExportBlock-173f88f7-a364-414c-833e-35a77a29b1e2-Part-1" trickster "PrestaShop XSS, changedetection.io SSTI"

Le script va :
1. Trouver le fichier HTML dans le dossier d'export
2. Extraire et nettoyer le contenu
3. Copier les images
4. Créer le writeup avec le template du site
5. Ajouter le writeup à l'index
6. Supprimer le dossier d'export (optionnel, avec --cleanup)
"""

import sys
import os
import re
import shutil
from pathlib import Path
from html import unescape

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
    <!-- Preload background image -->
    <link rel="preload" href="../../assets/labalsa.jpg" as="image">

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
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js" defer></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-php.min.js" defer></script>
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
                    <a href="../" class="nav-link active">Writeups</a>
                    <a href="../../Portfolio/" class="nav-link">Galerie</a>
                </div>
            </div>
        </div>
    </nav>

    <main class="min-h-screen">
        <div class="writeups-container">
            <a href="../" class="back-link">← Retour aux writeups</a>
            <div class="writeup-content">
                <header>
                    <h1 class="page-title">{title}</h1>
                </header>

                <div class="page-body">
{content}
                </div>
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
    (r"\bil ya\b", "il y a"),
    (r"\bducoup\b", "du coup"),
    (r"\bca sent\b", "ça sent"),
    (r"\bj'en ai trouvé\b", "j'en ai trouvé"),
    (r"\bje cat\b", "je cat"),
    (r"\bsoucis d'espace\b", "souci d'espace"),
    (r"\ben therme\b", "en termes"),
    (r"\btherme\b", "terme"),
]


def find_html_file(export_dir):
    """Trouve le fichier HTML dans le dossier d'export Notion."""
    export_path = Path(export_dir)
    html_files = list(export_path.glob("*.html"))
    if not html_files:
        return None
    # Retourne le premier fichier HTML trouvé
    return html_files[0]


def find_images(export_dir):
    """Trouve toutes les images dans le dossier d'export."""
    export_path = Path(export_dir)
    images = []
    for ext in ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp']:
        images.extend(export_path.glob(ext))
    return images


def find_all_assets(export_dir):
    """Trouve tous les fichiers assets dans le dossier d'export et ses sous-dossiers."""
    export_path = Path(export_dir)
    assets = []
    # Extensions de fichiers à copier (images + autres assets)
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.gif', '*.webp', '*.py', '*.pcap', 
                  '*.zip', '*.pdf', '*.txt', '*.json', '*.csv', '*.xml', '*.sql']
    
    for ext in extensions:
        # Cherche dans le dossier racine
        assets.extend(export_path.glob(ext))
        # Cherche dans les sous-dossiers
        assets.extend(export_path.glob(f'**/{ext}'))
    
    return assets


def fix_asset_paths(content, export_dir_name):
    """Corrige les chemins des assets dans le HTML pour pointer vers le dossier local."""
    from urllib.parse import unquote
    
    # Pattern pour les liens href avec le chemin du sous-dossier Notion
    # Ex: href="ARP%20Spoofing%20-%20L%E2%80%99homme%20du%20milieu/filtered_mitm1.pcap"
    def fix_href(match):
        href = match.group(1)
        # Décode l'URL
        decoded = unquote(href)
        # Extrait juste le nom du fichier
        filename = Path(decoded).name
        return f'href="{filename}"'
    
    # Corrige les href qui pointent vers des sous-dossiers
    content = re.sub(r'href="([^"]+/[^"]+\.(py|pcap|zip|pdf|txt|json|csv|xml|sql))"', 
                     fix_href, content)
    
    # Pattern pour les src d'images avec chemin
    def fix_src(match):
        src = match.group(1)
        decoded = unquote(src)
        filename = Path(decoded).name
        return f'src="{filename}"'
    
    content = re.sub(r'src="([^"]+/[^"]+\.(png|jpg|jpeg|gif|webp))"', 
                     fix_src, content)
    
    return content


def extract_title(html_content):
    """Extrait le titre de la page Notion."""
    match = re.search(r'<h1 class="page-title"[^>]*>(.*?)</h1>', html_content, re.DOTALL)
    if match:
        title = match.group(1).strip()
        # Supprime les tags HTML du titre
        title = re.sub(r'<[^>]+>', '', title).strip()
        return title
    # Fallback: cherche dans le <title>
    match = re.search(r'<title>(.*?)</title>', html_content)
    if match:
        return match.group(1).strip()
    return None


def clean_content(html_content):
    """Extrait et nettoie le contenu du writeup, retire le CSS Notion et adapte à la DA du site."""
    # Cherche le contenu du page-body
    match = re.search(r'<div class="page-body">(.*?)</div>\s*</article>', html_content, re.DOTALL)
    if match:
        content = match.group(1)
    else:
        # Fallback: cherche l'article entier
        match = re.search(r'<article[^>]*>(.*?)</article>', html_content, re.DOTALL)
        if match:
            content = match.group(1)
        else:
            # Dernier recours: prend le body
            match = re.search(r'<body[^>]*>(.*?)</body>', html_content, re.DOTALL)
            content = match.group(1) if match else html_content
    
    # ========== SUPPRESSION DU CSS NOTION ==========
    
    # Supprime les balises <style> complètes
    content = re.sub(r'<style[^>]*>.*?</style>', '', content, flags=re.DOTALL)
    
    # Supprime les scripts Prism inline (on les charge dans le head)
    content = re.sub(r'<script[^>]*prism[^>]*>.*?</script>', '', content, flags=re.DOTALL)
    content = re.sub(r'<link[^>]*prism[^>]*/?\s*>', '', content)
    
    # Supprime TOUS les attributs style inline
    content = re.sub(r'\s+style="[^"]*"', '', content)
    
    # Supprime les classes Notion de couleur/highlight (on utilise notre CSS)
    notion_color_classes = [
        'highlight-default', 'highlight-gray', 'highlight-brown', 'highlight-orange',
        'highlight-yellow', 'highlight-teal', 'highlight-blue', 'highlight-purple',
        'highlight-pink', 'highlight-red', 'highlight-default_background',
        'highlight-gray_background', 'highlight-brown_background', 'highlight-orange_background',
        'highlight-yellow_background', 'highlight-teal_background', 'highlight-blue_background',
        'highlight-purple_background', 'highlight-pink_background', 'highlight-red_background',
        'block-color-default', 'block-color-gray', 'block-color-brown', 'block-color-orange',
        'block-color-yellow', 'block-color-teal', 'block-color-blue', 'block-color-purple',
        'block-color-pink', 'block-color-red', 'block-color-default_background',
        'block-color-gray_background', 'block-color-brown_background', 'block-color-orange_background',
        'block-color-yellow_background', 'block-color-teal_background', 'block-color-blue_background',
        'block-color-purple_background', 'block-color-pink_background', 'block-color-red_background',
    ]
    for cls in notion_color_classes:
        content = re.sub(rf'\s*{cls}', '', content)
    
    # Supprime les classes Notion de structure qu'on n'utilise pas
    notion_struct_classes = [
        'sans', 'serif', 'mono', 'page-title', 'page-description', 'page-header-icon',
        'page-header-icon-with-cover', 'page-cover-image', 'collection-content',
        'collection-title', 'column-list', 'column', 'table_of_contents-item',
        'table_of_contents-indent-1', 'table_of_contents-indent-2', 'table_of_contents-indent-3',
        'table_of_contents-link', 'toggle', 'to-do-list', 'to-do-children-checked',
        'checkbox', 'checkbox-on', 'checkbox-off', 'user-icon', 'user-icon-inner',
        'text-icon', 'pdf-relative-link-path', 'selected-value', 'indented',
    ]
    for cls in notion_struct_classes:
        content = re.sub(rf'\s*{cls}', '', content)
    
    # ========== NETTOYAGE DE LA STRUCTURE HTML ==========
    
    # Supprime les div style="display:contents" en gardant le contenu
    content = re.sub(r'<div[^>]*display:\s*contents[^>]*>', '', content)
    content = re.sub(r'<div style="display:contents"[^>]*>', '', content)
    
    # Ferme les div orphelins (après avoir supprimé les ouvertures)
    # Compte les div ouverts/fermés pour équilibrer
    
    # Supprime les attributs dir
    content = re.sub(r'\s+dir="[^"]*"', '', content)
    
    # Nettoie les IDs Notion (longs UUIDs)
    content = re.sub(r'\s+id="[a-f0-9-]{36}"', '', content)
    
    # Supprime les classes vides après nettoyage
    content = re.sub(r'\s+class="\s*"', '', content)
    
    # ========== CONVERSION DES ÉLÉMENTS NOTION ==========
    
    # Helper to get domain
    def get_domain(url):
        from urllib.parse import urlparse
        try:
            return urlparse(url).netloc
        except:
            return ""

    # Convertit les bookmarks Notion en format standardisé (Favicon + Titre)
    def convert_bookmark(match):
        full_match = match.group(0)
        href_match = re.search(r'href="([^"]+)"', full_match)
        title_match = re.search(r'<div class="bookmark-title">([^<]+)</div>', full_match)
        
        if href_match:
            href = href_match.group(1)
            title = title_match.group(1) if title_match else href
            domain = get_domain(href)
            
            # Truncate title to 57 chars
            if len(title) > 57:
                title = title[:54] + "..."
            
            return f'''<p class="link-integration">
                        <img src="https://www.google.com/s2/favicons?domain={domain}&sz=64" class="site-favicon" alt="">
                        <a href="{href}" target="_blank" rel="noopener">{title}</a>
                    </p>'''
        return ''
    
    content = re.sub(r'<figure[^>]*>.*?<a[^>]*class="bookmark[^"]*"[^>]*>.*?</a>.*?</figure>', 
                     convert_bookmark, content, flags=re.DOTALL)
    
    # Simplifie les figures avec source (liens GitHub, etc.)
    def convert_source(match):
        source_match = re.search(r'<div class="source">([^<]+)</div>', match.group(0))
        if source_match:
            url = source_match.group(1).strip()
            # Si c'est une URL valide
            if url.startswith('http'):
                domain = get_domain(url)
                title = url
            # Truncate title to 57 chars
            if len(title) > 57:
                title = title[:54] + "..."
                    
                return f'''<p class="link-integration">
                            <img src="https://www.google.com/s2/favicons?domain={domain}&sz=64" class="site-favicon" alt="">
                            <a href="{url}" target="_blank" rel="noopener">{title}</a>
                        </p>'''
            return f'<p><a href="{url}" target="_blank" rel="noopener">{url}</a></p>'
        return ''
    
    content = re.sub(r'<figure[^>]*>\s*<div class="source">[^<]+</div>\s*</figure>', 
                     convert_source, content, flags=re.DOTALL)
    
    # Convertit les figures d'images en format simple
    def convert_image_figure(match):
        img_match = re.search(r'<img[^>]*src="([^"]+)"[^>]*>', match.group(0))
        if img_match:
            src = img_match.group(1)
            # Garde juste le nom de fichier
            src = re.sub(r'^.*/', '', src)
            return f'<figure class="image"><img src="{src}" alt="" style="max-width:100%;"></figure>'
        return ''
    
    content = re.sub(r'<figure[^>]*class="[^"]*image[^"]*"[^>]*>.*?</figure>', 
                     convert_image_figure, content, flags=re.DOTALL)
    
    # ========== NETTOYAGE DES BLOCS DE CODE ==========
    
    # Convertit les classes de code Notion en classes Prism (lowercase)
    content = re.sub(r'class="language-Bash"', 'class="language-bash"', content)
    content = re.sub(r'class="language-JSON"', 'class="language-json"', content)
    content = re.sub(r'class="language-SQL"', 'class="language-sql"', content)
    content = re.sub(r'class="language-Python"', 'class="language-python"', content)
    content = re.sub(r'class="language-PHP"', 'class="language-php"', content)
    content = re.sub(r'class="language-JavaScript"', 'class="language-javascript"', content)
    content = re.sub(r'class="language-HTML"', 'class="language-html"', content)
    content = re.sub(r'class="language-CSS"', 'class="language-css"', content)
    content = re.sub(r'class="language-Plain text"', 'class="language-text"', content)
    
    # Simplifie les blocs de code (garde pre > code avec la bonne classe)
    content = re.sub(r'<pre[^>]*class="code[^"]*"[^>]*>', '<pre class="code code-wrap">', content)
    
    # ========== NETTOYAGE DES LIENS ==========
    
    # Ajoute target="_blank" aux liens externes
    def add_target_blank(match):
        href = match.group(1)
        if href.startswith('http'):
            return f'<a href="{href}" target="_blank" rel="noopener"'
        return match.group(0)
    
    content = re.sub(r'<a href="([^"]+)"(?![^>]*target=)', add_target_blank, content)
    
    # Supprime les images cassées des bookmarks
    content = re.sub(r'<img[^>]*class="[^"]*bookmark-icon[^"]*"[^>]*/?\s*>', '', content)
    content = re.sub(r'<img[^>]*class="[^"]*bookmark-image[^"]*"[^>]*/?\s*>', '', content)
    content = re.sub(r'<img[^>]*class="[^"]*icon[^"]*"[^>]*/?\s*>', '', content)
    
    # ========== NETTOYAGE FINAL ==========
    
    # Supprime les header Notion (page-title est dans notre template)
    content = re.sub(r'<header>.*?</header>', '', content, flags=re.DOTALL)
    
    # Supprime les divs vides
    content = re.sub(r'<div>\s*</div>', '', content)
    
    # Supprime les paragraphes vides
    content = re.sub(r'<p[^>]*>\s*</p>', '', content)
    
    # Supprime les espaces multiples
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    # Supprime les </div> orphelins en trop (causés par la suppression des div display:contents)
    # On compte et équilibre
    open_divs = len(re.findall(r'<div[^>]*>', content))
    close_divs = len(re.findall(r'</div>', content))
    if close_divs > open_divs:
        # Supprime les </div> en trop à la fin
        for _ in range(close_divs - open_divs):
            content = re.sub(r'</div>\s*$', '', content.rstrip())
    
    return content.strip()


def fix_spelling(content):
    """Corrige les fautes d'orthographe courantes."""
    for pattern, replacement in SPELLING_FIXES:
        content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
    return content


def add_to_index(name, title, description):
    """Ajoute le writeup à la page d'index."""
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        index_content = f.read()
    
    # Vérifie si le writeup existe déjà
    if f'href="{name}/"' in index_content:
        print(f"⚠️  Le writeup '{name}' existe déjà dans l'index, mise à jour de la description...")
        # Met à jour la description existante
        pattern = rf'(<a href="{name}/" class="writeup-card">.*?<p>)(.*?)(</p>)'
        replacement = rf'\1{description}\3'
        index_content = re.sub(pattern, replacement, index_content, flags=re.DOTALL)
        with open(INDEX_FILE, 'w', encoding='utf-8') as f:
            f.write(index_content)
        return True
    
    # Crée la nouvelle carte
    new_card = f'''
                <a href="{name}/" class="writeup-card">
                    <span class="htb-badge">HACK THE BOX</span>
                    <h3>{title}</h3>
                    <p>{description}</p>
                </a>'''
    
    # Trouve la fin de la grille (avant </div></div></main>) et insère la carte
    pattern = r'(</div>\s*</div>\s*</main>)'
    replacement = new_card + r'\n            \1'
    
    new_index = re.sub(pattern, replacement, index_content, count=1)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(new_index)
    
    return True


def convert_writeup(export_dir, name, description=None, cleanup=False):
    """Convertit un export Notion en writeup intégré."""
    export_path = Path(export_dir)
    
    if not export_path.exists():
        print(f"❌ Dossier non trouvé: {export_dir}")
        return False
    
    # Trouve le fichier HTML
    html_file = find_html_file(export_path)
    if not html_file:
        print(f"❌ Aucun fichier HTML trouvé dans: {export_dir}")
        return False
    
    print(f"📄 Fichier HTML trouvé: {html_file.name}")
    
    # Lit le fichier source
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # Extrait le titre
    title = extract_title(html_content) or name.capitalize()
    print(f"📝 Titre: {title}")
    
    # Extrait et nettoie le contenu
    content = clean_content(html_content)
    content = fix_spelling(content)
    
    # Corrige les chemins des assets (avant de créer le fichier)
    content = fix_asset_paths(content, export_path.name)
    
    # Crée le dossier du writeup
    writeup_dir = WRITEUPS_DIR / name
    writeup_dir.mkdir(exist_ok=True)
    
    # Copie tous les assets (images, py, pcap, etc.)
    assets = find_all_assets(export_path)
    for asset in assets:
        dest = writeup_dir / asset.name
        # Évite d'écraser si déjà copié (cas de doublons)
        if not dest.exists():
            shutil.copy2(asset, dest)
            ext = asset.suffix.lower()
            if ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp']:
                print(f"📷 Image copiée: {asset.name}")
            elif ext == '.py':
                print(f"🐍 Script Python copié: {asset.name}")
            elif ext == '.pcap':
                print(f"📦 Capture réseau copiée: {asset.name}")
            else:
                print(f"📎 Fichier copié: {asset.name}")
    
    # Génère le HTML final
    # Indente le contenu correctement
    indented_content = '\n'.join('                    ' + line if line.strip() else '' 
                                   for line in content.split('\n'))
    final_html = HTML_TEMPLATE.format(title=title, content=indented_content)
    
    # Écrit le fichier
    output_path = writeup_dir / "index.html"
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Writeup créé: {output_path}")
    
    # Ajoute à l'index
    desc = description or f"Writeup {title}"
    if add_to_index(name, title, desc):
        print(f"✅ Ajouté/mis à jour dans l'index des writeups")
    
    # Nettoyage optionnel
    if cleanup:
        shutil.rmtree(export_path)
        print(f"🗑️  Dossier d'export supprimé: {export_dir}")
    
    return True


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        print("\nArguments:")
        print("  <dossier_export>   Chemin vers le dossier exporté de Notion")
        print("  <nom_writeup>      Nom du dossier (lowercase, sans espaces)")
        print("  [description]      Description optionnelle pour l'index")
        print("\nOptions:")
        print("  --cleanup          Supprime le dossier d'export après conversion")
        print("\nExemple:")
        print('  python3 add_writeup.py "ExportBlock-xxx" trickster "PrestaShop XSS, SSTI" --cleanup')
        sys.exit(1)
    
    # Parse les arguments
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    cleanup = '--cleanup' in sys.argv
    
    export_dir = args[0]
    name = args[1].lower().replace(' ', '-')
    description = args[2] if len(args) > 2 else None
    
    success = convert_writeup(export_dir, name, description, cleanup)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
