     AOS.init({
            duration: 1000,
            once: true
        });

        function toggleCard(element) {
            const cardBody = element.nextElementSibling;
            const cardHeader = element;
            const plusSign = element.querySelector('.float-end');

            if (cardBody.style.display === 'block') {
                cardBody.style.display = 'none';
                cardHeader.classList.remove('active');
                plusSign.textContent = '+';
            } else {
                cardBody.style.display = 'block';
                cardHeader.classList.add('active');
                plusSign.textContent = '-';
            }
        }

        // Smooth scroll
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
     const carouselInner = document.querySelector('.carousel-inner');
    const nextBtn = document.getElementById('nextBtn');
    const prevBtn = document.getElementById('prevBtn');

    let currentIndex = 0;

    // Slide to the next testimonial
    nextBtn.addEventListener('click', () => {
      const totalItems = carouselInner.children.length;
      currentIndex = (currentIndex + 1) % totalItems;
      updateCarousel();
    });

    // Slide to the previous testimonial
    prevBtn.addEventListener('click', () => {
      const totalItems = carouselInner.children.length;
      currentIndex = (currentIndex - 1 + totalItems) % totalItems;
      updateCarousel();
    });

    // Update the carousel position
    function updateCarousel() {
      const width = carouselInner.clientWidth;
      carouselInner.style.transform = `translateX(-${currentIndex * width}px)`;
    }
