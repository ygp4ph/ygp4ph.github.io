# 🔐 Portfolio Cybersécurité - Raphaël Couvert

Site personnel moderne pour présenter mes liens professionnels et mes write-ups de challenges CTF.

## 🚀 Comment mettre en ligne sur GitHub Pages

### Étape 1 : Créer le repository sur GitHub

1. Va sur [GitHub](https://github.com)
2. Clique sur **"New repository"** (bouton vert en haut à droite)
3. Nom du repository : **`ygp4ph.github.io`** (important : utilise exactement ton pseudo GitHub)
4. Mets le repository en **Public**
5. ❌ **NE COCHE PAS** "Add a README file" (on va uploader nos fichiers)
6. Clique sur **"Create repository"**

### Étape 2 : Uploader les fichiers

Tu as 2 options :

#### Option A : Upload direct (le plus simple)
1. Sur la page de ton nouveau repository, clique sur **"uploading an existing file"**
2. Glisse-dépose ces 3 fichiers :
   - `index.html`
   - `style.css`
   - `script.js`
3. Écris un message de commit : "Initial commit - Portfolio website"
4. Clique sur **"Commit changes"**

#### Option B : Via Git (si tu connais)
```bash
# Dans le dossier où tu as téléchargé les fichiers
git init
git add index.html style.css script.js
git commit -m "Initial commit - Portfolio website"
git branch -M main
git remote add origin https://github.com/ygp4ph/ygp4ph.github.io.git
git push -u origin main
```

### Étape 3 : Activer GitHub Pages

1. Dans ton repository, va dans **Settings** (⚙️ en haut)
2. Dans le menu de gauche, clique sur **Pages**
3. Dans "Source", sélectionne :
   - Branch : **main**
   - Folder : **/ (root)**
4. Clique sur **Save**

### ✅ C'est fini !

Ton site sera disponible à cette adresse dans 1-2 minutes :
**https://ygp4ph.github.io**

GitHub va te montrer un message vert avec l'URL une fois que c'est en ligne.

---

## 📝 Comment ajouter des write-ups

### Méthode 1 : Modifier directement dans GitHub
1. Va dans ton repository
2. Clique sur `index.html`
3. Clique sur le crayon ✏️ (Edit)
4. Trouve la section "Write-ups" (ligne ~105)
5. Copie-colle ce template pour chaque write-up :

```html
<div class="writeup-card">
    <div class="writeup-header">
        <span class="writeup-platform">Root Me</span>
        <span class="writeup-difficulty easy">Facile</span>
    </div>
    <h3>Titre du challenge</h3>
    <p class="writeup-category"><i class="fas fa-tag"></i> Catégorie - Type</p>
    <p class="writeup-description">Description courte du challenge...</p>
    <a href="lien-vers-ton-writeup.html" class="writeup-link">Lire le write-up <i class="fas fa-arrow-right"></i></a>
</div>
```

6. Change la difficulté : `easy`, `medium` ou `hard`
7. Commit les changements

### Méthode 2 : Créer une page dédiée pour chaque write-up
1. Crée un dossier `writeups/` dans ton repository
2. Pour chaque write-up, crée un fichier HTML (ex: `sql-injection.html`)
3. Lie-le depuis la page d'accueil

---

## 🎨 Personnalisation

### Changer les couleurs
Édite `style.css`, lignes 9-11 :
```css
--primary-color: #10b981;  /* Vert principal */
--primary-dark: #059669;   /* Vert foncé */
```

### Ajouter ta photo
Remplace l'icône par une vraie photo :
1. Upload une image dans ton repository (ex: `photo.jpg`)
2. Dans `index.html`, ligne 26, remplace :
```html
<div class="avatar">
    <img src="photo.jpg" alt="Raphaël Couvert" style="width:100%; height:100%; border-radius:50%; object-fit:cover;">
</div>
```

### Ajouter d'autres liens
Dans `index.html`, section "links-grid" (ligne ~41), ajoute :
```html
<a href="TON_LIEN" target="_blank" class="link-card">
    <div class="link-icon">
        <i class="fas fa-terminal"></i> <!-- Change l'icône -->
    </div>
    <div class="link-content">
        <h4>Plateforme</h4>
        <p>Description</p>
    </div>
    <i class="fas fa-external-link-alt"></i>
</a>
```

### Icônes disponibles
Utilise [Font Awesome](https://fontawesome.com/icons) :
- `fa-envelope` : Email
- `fa-github` : GitHub  
- `fa-linkedin` : LinkedIn
- `fa-terminal` : Root Me / Plateformes CTF
- `fa-trophy` : HackTheBox
- `fa-flag` : TryHackMe
- `fa-code` : Projets de code
- `fa-file-pdf` : CV

---

## 🆘 Problèmes courants

### Le site ne s'affiche pas
- Attends 2-3 minutes après l'activation de GitHub Pages
- Vérifie que le nom du repository est bien `ygp4ph.github.io`
- Vérifie que les fichiers sont à la racine (pas dans un sous-dossier)

### Les styles ne s'appliquent pas
- Vérifie que `style.css` et `script.js` sont bien au même niveau que `index.html`
- Vide le cache de ton navigateur (Ctrl+F5)

### Je veux ajouter un lien vers mon CV
1. Upload ton CV en PDF dans le repository
2. Dans `index.html`, trouve le lien CV (ligne ~82)
3. Change `href="#"` par `href="CV_Raphael_Couvert.pdf"`
4. Enlève `class="disabled"`

---

## 📧 Contact

Des questions ? Écris-moi : faphaelcouvert2007@gmail.com

Bon courage pour ton stage ! 💪
