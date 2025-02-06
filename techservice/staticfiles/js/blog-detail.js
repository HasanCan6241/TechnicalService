// blog-detail.js
document.addEventListener('DOMContentLoaded', function() {
    // AOS Başlatma
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });

    // Scroll Progress Bar
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const winScroll = document.body.scrollTop || document.documentElement.scrollTop;
        const height = document.documentElement.scrollHeight - document.documentElement.clientHeight;
        const scrolled = (winScroll / height) * 100;
        progressBar.style.width = scrolled + '%';
    });

    // Image Lightbox
    const contentImages = document.querySelectorAll('.blog-post-content img');
    contentImages.forEach(img => {
        img.addEventListener('click', () => {
            const lightbox = document.createElement('div');
            lightbox.className = 'lightbox';
            lightbox.innerHTML = `
                <div class="lightbox-content">
                    <img src="${img.src}" alt="${img.alt}">
                </div>
            `;
            document.body.appendChild(lightbox);

            lightbox.addEventListener('click', () => {
                lightbox.remove();
            });
        });
    });

    // Smooth Scroll
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            document.querySelector(this.getAttribute('href')).scrollIntoView({
                behavior: 'smooth'
            });
        });
    });
});

// social-share.js
function initSocialShares() {
    // Sayfa bilgilerini al
    const pageUrl = encodeURIComponent(window.location.href);
    const pageTitle = encodeURIComponent(document.title);

    // Sosyal medya paylaşım URLs
    const sharers = {
        facebook: `https://www.facebook.com/sharer/sharer.php?u=${pageUrl}`,
        twitter: `https://twitter.com/intent/tweet?url=${pageUrl}&text=${pageTitle}`,
        whatsapp: `https://api.whatsapp.com/send?text=${pageTitle}%20${pageUrl}`,
        linkedin: `https://www.linkedin.com/shareArticle?mini=true&url=${pageUrl}&title=${pageTitle}`,
        telegram: `https://t.me/share/url?url=${pageUrl}&text=${pageTitle}`,
    };

    // Paylaşım penceresini aç
    function openShareWindow(url) {
        window.open(
            url,
            'share-popup',
            'height=450, width=600, toolbar=no, menubar=no, scrollbars=no, resizable=no, location=no, directories=no, status=no'
        );
    }

    // Click event listeners ekle
    document.querySelectorAll('[data-share]').forEach(button => {
        button.addEventListener('click', (e) => {
            e.preventDefault();
            const platform = button.getAttribute('data-share');
            const url = sharers[platform];

            if (url) {
                openShareWindow(url);
            }
        });
    });
}

// Sayfa yüklendiğinde başlat
document.addEventListener('DOMContentLoaded', initSocialShares);