// Navigation entre les sections
document.addEventListener('DOMContentLoaded', function() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.section');

    // Fonction pour changer de section
    function switchSection(targetId) {
        sections.forEach(section => {
            section.classList.remove('active');
        });

        navLinks.forEach(link => {
            link.classList.remove('active');
        });

        const targetSection = document.querySelector(targetId);
        if (targetSection) {
            targetSection.classList.add('active');
        }

        const activeLink = document.querySelector(`a[href="${targetId}"]`);
        if (activeLink) {
            activeLink.classList.add('active');
        }

        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Écouter les clics sur les liens de navigation
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            switchSection(targetId);
            history.pushState(null, '', targetId);
        });
    });

    // Gérer le bouton retour du navigateur
    window.addEventListener('popstate', function() {
        const hash = window.location.hash || '#accueil';
        switchSection(hash);
    });

    // Charger la bonne section au chargement de la page
    const initialHash = window.location.hash || '#accueil';
    switchSection(initialHash);

    // Charger les write-ups depuis Notion
    loadWriteups();
});

// Fonction pour charger les write-ups depuis Notion
async function loadWriteups() {
    const writeupsGrid = document.getElementById('writeups-grid');
    
    // Pour l'instant, on va créer une structure statique car l'API Notion nécessite une clé d'API côté serveur
    // Voici comment vous pourriez structurer vos write-ups manuellement
    
    // Simuler un délai de chargement
    setTimeout(() => {
        // Remplacer le loading par les write-ups
        writeupsGrid.innerHTML = '';
        
        // Exemple de write-ups (à remplacer par vos données réelles)
        const writeups = [
            {
                title: "Example Challenge 1",
                platform: "ROOT-ME",
                difficulty: "FACILE",
                category: "WEB - SQL INJECTION",
                description: "Description du challenge et de la méthodologie utilisée pour le résoudre...",
                link: "https://ember-scilla-836.notion.site/votre-page"
            },
            {
                title: "Example Challenge 2",
                platform: "ROOT-ME",
                difficulty: "MOYEN",
                category: "CRYPTOGRAPHIE",
                description: "Description du challenge et de la méthodologie utilisée pour le résoudre...",
                link: "https://ember-scilla-836.notion.site/votre-page"
            }
        ];

        if (writeups.length === 0) {
            writeupsGrid.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-file-code"></i>
                    <h3>WRITE-UPS À VENIR</h3>
                    <p>JE SUIS EN TRAIN DE DOCUMENTER MES RÉSOLUTIONS DE CHALLENGES.<br>REVENEZ BIENTÔT !</p>
                </div>
            `;
        } else {
            writeups.forEach(writeup => {
                const card = createWriteupCard(writeup);
                writeupsGrid.appendChild(card);
            });
        }
    }, 1000);
}

// Fonction pour créer une carte de write-up
function createWriteupCard(writeup) {
    const card = document.createElement('div');
    card.className = 'writeup-card';
    
    const difficultyClass = writeup.difficulty.toLowerCase();
    
    card.innerHTML = `
        <div class="writeup-header">
            <span class="writeup-platform">${writeup.platform}</span>
            <span class="writeup-difficulty ${difficultyClass}">${writeup.difficulty}</span>
        </div>
        <h3>${writeup.title}</h3>
        <p class="writeup-category"><i class="fas fa-tag"></i> ${writeup.category}</p>
        <p class="writeup-description">${writeup.description}</p>
        <a href="${writeup.link}" target="_blank" class="writeup-link">LIRE LE WRITE-UP <i class="fas fa-arrow-right"></i></a>
    `;
    
    return card;
}

// Animation au scroll pour les cartes
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observer les cartes après le chargement du DOM
document.addEventListener('DOMContentLoaded', function() {
    setTimeout(() => {
        const cards = document.querySelectorAll('.link-card, .writeup-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    }, 100);
});
