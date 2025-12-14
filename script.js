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
});
