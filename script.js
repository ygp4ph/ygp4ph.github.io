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
});
