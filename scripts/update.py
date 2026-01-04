#!/usr/bin/env python3
"""
Script pour ajouter une image à la galerie.
Usage: python update.py /chemin/absolu/vers/image.jpg
"""

import os
import sys
import json
import shutil
import subprocess

# Configuration - chemins relatifs au dossier Portfolio
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PORTFOLIO_DIR = os.path.join(SCRIPT_DIR, "..", "Portfolio")
GALLERY_DIR = os.path.join(PORTFOLIO_DIR, "gallery")
MANIFEST_PATH = os.path.join(GALLERY_DIR, "manifest.json")

# Extensions d'images acceptées
VALID_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg', '.bmp', '.tiff')


def convert_to_webp(source_path: str, dest_path: str, quality: int = 85) -> bool:
    """Convertit une image en WebP avec ImageMagick."""
    try:
        subprocess.run(
            ["magick", source_path, "-quality", str(quality), dest_path],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError as e:
        print(f"[-] Erreur de conversion: {e.stderr.decode()}")
        return False
    except FileNotFoundError:
        print("[-] ImageMagick n'est pas installe. Installe-le avec: sudo pacman -S imagemagick")
        return False


def add_image(image_path: str) -> None:
    """Ajoute une image à la galerie: copie, convertit en WebP, et met à jour le manifest."""
    
    # Vérifie que le fichier existe
    if not os.path.isfile(image_path):
        print(f"[-] Fichier non trouve: {image_path}")
        sys.exit(1)
    
    # Vérifie l'extension
    _, ext = os.path.splitext(image_path)
    if ext.lower() not in VALID_EXTENSIONS:
        print(f"[-] Extension non supportee: {ext}")
        print(f"   Extensions valides: {', '.join(VALID_EXTENSIONS)}")
        sys.exit(1)
    
    # Crée le dossier gallery si nécessaire
    os.makedirs(GALLERY_DIR, exist_ok=True)
    
    # Nom du fichier WebP final
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    webp_name = f"{base_name}.webp"
    webp_path = os.path.join(GALLERY_DIR, webp_name)
    
    # Vérifie si l'image existe déjà
    if os.path.exists(webp_path):
        print(f"[!] L'image {webp_name} existe deja dans la galerie.")
        response = input("   Écraser? [o/N] ").strip().lower()
        if response != 'o':
            print("   Annulé.")
            sys.exit(0)
    
    # Convertit en WebP
    print(f"[*] Conversion de {os.path.basename(image_path)} en WebP...")
    if not convert_to_webp(image_path, webp_path):
        sys.exit(1)
    
    # Taille du fichier
    original_size = os.path.getsize(image_path) / 1024
    webp_size = os.path.getsize(webp_path) / 1024
    reduction = ((original_size - webp_size) / original_size) * 100
    print(f"[+] Converti: {original_size:.1f}KB -> {webp_size:.1f}KB ({reduction:.1f}% de reduction)")
    
    # Met à jour le manifest
    print("[*] Mise a jour du manifest...")
    
    # Charge le manifest existant ou crée une liste vide
    if os.path.exists(MANIFEST_PATH):
        with open(MANIFEST_PATH, 'r') as f:
            manifest = json.load(f)
    else:
        manifest = []
    
    # Retire l'image si elle existe déjà (pour éviter les doublons)
    manifest = [img for img in manifest if img != webp_name]
    
    # Ajoute en haut du manifest
    manifest.insert(0, webp_name)
    
    # Sauvegarde le manifest
    with open(MANIFEST_PATH, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print(f"[+] {webp_name} ajoute en haut du manifest ({len(manifest)} images au total)")
    print(f"\n[*] N'oublie pas: git add . && git commit -m 'feat: add {base_name}' && git push")


def main():
    if len(sys.argv) != 2:
        print("Usage: python update.py /chemin/absolu/vers/image.jpg")
        print("\nExemple:")
        print("  python scripts/update.py ~/Images/photo.jpg")
        sys.exit(1)
    
    image_path = os.path.expanduser(sys.argv[1])  # Supporte ~/
    image_path = os.path.abspath(image_path)      # Convertit en chemin absolu
    
    add_image(image_path)


if __name__ == "__main__":
    main()