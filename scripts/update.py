import os
import json
import random  # <-- Import nécessaire pour le mélange

# Configuration
folder = "gallery"
manifest_path = f"{folder}/manifest.json"
# Extensions d'images acceptées
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')

def update_manifest():
    # Vérifie si le dossier gallery existe
    if not os.path.exists(folder):
        print(f"❌ Erreur : Le dossier '{folder}' n'existe pas.")
        return

    # 1. Scanne le dossier et garde seulement les images
    files = [
        f for f in os.listdir(folder) 
        if f.lower().endswith(valid_extensions)
    ]
    
    # 2. Mélange aléatoire (Shuffle)
    random.shuffle(files)

    # 3. Écrase le fichier manifest.json avec la nouvelle liste mélangée
    try:
        with open(manifest_path, 'w') as f:
            json.dump(files, f, indent=2)
        print(f"[+] Succès ! 'manifest.json' mis à jour avec {len(files)} images.")
        print(f"    (Ordre : Aléatoire / Shuffle)")
        print(f"    N'oublie pas de faire : git add, git commit et git push")
    except Exception as e:
        print(f"[-] Erreur lors de l'écriture du fichier : {e}")

if __name__ == "__main__":
    update_manifest()