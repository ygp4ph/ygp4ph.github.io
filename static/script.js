document.addEventListener('DOMContentLoaded', () => {
    // Feature specific: Home Profile Video
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

    // Dynamic Navbar Loading and Mobile Menu Initialization
    const navbarPlaceholder = document.getElementById('navbar-placeholder');

    function initMobileMenu() {
        const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
        const navLinks = document.getElementById('nav-links');
        const overlay = document.getElementById('mobile-menu-overlay');

        if (mobileMenuToggle && navLinks) {
            // Remove existing event listeners to avoid duplicates if re-initializing
            const newToggle = mobileMenuToggle.cloneNode(true);
            mobileMenuToggle.parentNode.replaceChild(newToggle, mobileMenuToggle);
            
            // We need to re-select after replacement or just attach if we assume fresh DOM
            // Since we clone, we need to re-select
            const toggleBtn = document.getElementById('mobile-menu-toggle');

            function closeMenu() {
                toggleBtn.classList.remove('active');
                navLinks.classList.remove('active');
                if (overlay) overlay.classList.remove('active');
            }

            toggleBtn.addEventListener('click', () => {
                toggleBtn.classList.toggle('active');
                navLinks.classList.toggle('active');
                if (overlay) overlay.classList.toggle('active');
            });

            navLinks.querySelectorAll('.nav-link').forEach(link => {
                link.addEventListener('click', closeMenu);
            });

            if (overlay) {
                overlay.addEventListener('click', closeMenu);
            }
        }
    }

    function highlightActiveLink() {
        const path = window.location.pathname;
        const links = document.querySelectorAll('.nav-link');
        links.forEach(link => {
            const href = link.getAttribute('href');
            link.classList.remove('active');
            if (href === '/' && (path === '/' || path === '/index.html' || path.endsWith('/'))) {
                 // Exact match for home, handled carefully
                 if (path === '/' || path === '/index.html') link.classList.add('active');
            } else if (href !== '/' && path.includes(href)) {
                link.classList.add('active');
            }
        });
        
        // Custom check: if we are in writeups (which we are if checking this script in that context)
        // ensure writeups link is active if path contains 'writeups'
        if (path.includes('/writeups/')) {
            const writeupsLink = document.querySelector('.nav-link[href="/writeups/"]');
            if (writeupsLink) writeupsLink.classList.add('active');
        }
    }

    if (navbarPlaceholder) {
        fetch('/writeups/navbar.html')
            .then(response => response.text())
            .then(html => {
                navbarPlaceholder.innerHTML = html;
                highlightActiveLink();
                initMobileMenu();
            })
            .catch(err => console.error('Failed to load navbar:', err));
    } else {
        // If navbar is already there (static), just init
        initMobileMenu();
        // optionally highlight active link if not hardcoded, but static usually has it hardcoded.
    }
});
