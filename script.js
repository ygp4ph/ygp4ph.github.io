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
});

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
        const cards = document.querySelectorAll('.link-card');
        cards.forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    }, 100);
});