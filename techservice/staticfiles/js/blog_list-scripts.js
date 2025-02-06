// blog-scripts.js
document.addEventListener('DOMContentLoaded', function() {
    // AOS Başlatma
    AOS.init({
        duration: 1000,
        once: true,
        offset: 100
    });

    // Arama kutusunu ve blog kartlarını seç
        const searchInput = document.querySelector('.form-control[placeholder="Blog ara..."]');
        const blogCards = document.querySelectorAll('.card');

        // Arama kutusunda yazı değiştiğinde çalıştır
        searchInput.addEventListener('input', function () {
            const searchTerm = searchInput.value.toLowerCase();

            // Her blog kartını kontrol et
            blogCards.forEach(card => {
                const title = card.querySelector('.card-title').textContent.toLowerCase();
                const content = card.querySelector('.card-text').textContent.toLowerCase();

                // Arama terimi başlıkta veya içerikte geçiyorsa kartı göster, değilse gizle
                if (title.includes(searchTerm) || content.includes(searchTerm)) {
                    card.style.display = "block";
                } else {
                    card.style.display = "none";
                }
            });
        });

    // Lazy Loading için Intersection Observer
    const images = document.querySelectorAll('.card-img-top');
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                observer.unobserve(img);
            }
        });
    });

    images.forEach(img => imageObserver.observe(img));

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