document.addEventListener('DOMContentLoaded', () => {
    const iconCircle = document.querySelector('.icon-circle');
    const video = document.querySelector('.hero-profile-video');

    if (iconCircle && video) {
        iconCircle.addEventListener('mouseenter', () => {
            video.currentTime = 0;
            video.play();
        });

        iconCircle.addEventListener('mouseleave', () => {
            video.pause();
        });
    }

    // Parallax Effect
    window.addEventListener('scroll', () => {
        const scrollTop = window.scrollY;
        const docHeight = document.body.scrollHeight - window.innerHeight;

        if (docHeight > 0) {
            const scrollPercent = scrollTop / docHeight;
            const bgPosY = scrollPercent * 100; // 0 to 100
            document.body.style.setProperty('--bg-pos-y', `${bgPosY}%`);
        }
    });

    // Initial call to set position
    window.dispatchEvent(new Event('scroll'));

    // Mobile Menu Toggle
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const navLinks = document.getElementById('nav-links');
    const overlay = document.getElementById('mobile-menu-overlay');

    function closeMenu() {
        mobileMenuToggle.classList.remove('active');
        navLinks.classList.remove('active');
        if (overlay) overlay.classList.remove('active');
    }

    if (mobileMenuToggle && navLinks) {
        mobileMenuToggle.addEventListener('click', () => {
            mobileMenuToggle.classList.toggle('active');
            navLinks.classList.toggle('active');
            if (overlay) overlay.classList.toggle('active');
        });

        // Fermer le menu au clic sur un lien
        navLinks.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', closeMenu);
        });

        // Fermer le menu au clic sur l'overlay
        if (overlay) {
            overlay.addEventListener('click', closeMenu);
        }
    }
});
