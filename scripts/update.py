import os
import json

# Configuration
folder = "gallery"
manifest_path = f"{folder}/manifest.json"
# Extensions d'images acceptées
valid_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg')

# Images épinglées en haut (dans l'ordre souhaité)
PINNED_IMAGES = [
    "ptero.webp",
    "cac0bc22-b010-4b12-a5d0-aba6d8a183cd (1).webp",
    "ef91247c-63d9-44f4-a5b6-3c794526b935 (1).webp",
    "ca1b9a76-eb03-4f3b-b5c8-53abbe9a242a (2).webp",
    "ac3bd402-06a7-499f-8c1f-ba9edaf4ada1 (1).webp",
    "12b2d8bf-b709-44a2-a49a-b15955c48fd2 (1).webp",
]

def update_manifest():
    # Vérifie si le dossier gallery existe
    if not os.path.exists(folder):
        print(f"❌ Erreur : Le dossier '{folder}' n'existe pas.")
        return

    # 1. Scanne le dossier et garde seulement les images
    all_files = [
        f for f in os.listdir(folder) 
        if f.lower().endswith(valid_extensions)
    ]
    
    # 2. Sépare les images épinglées des autres
    pinned = [f for f in PINNED_IMAGES if f in all_files]
    others = [f for f in all_files if f not in PINNED_IMAGES]
    
    # 3. Trie les autres par date de modification (les plus récentes en premier)
    others.sort(key=lambda f: os.path.getmtime(os.path.join(folder, f)), reverse=True)
    
    # 4. Combine : épinglées en haut + autres triées par date
    files = pinned + others

    # 5. Écrase le fichier manifest.json
    try:
        with open(manifest_path, 'w') as f:
            json.dump(files, f, indent=2)
        print(f"[+] Succès ! 'manifest.json' mis à jour avec {len(files)} images.")
        print(f"    - {len(pinned)} images épinglées en haut")
        print(f"    - {len(others)} autres images (triées par date, récentes en premier)")
        print(f"    N'oublie pas de faire : git add, git commit et git push")
    except Exception as e:
        print(f"[-] Erreur lors de l'écriture du fichier : {e}")

if __name__ == "__main__":
    update_manifest()