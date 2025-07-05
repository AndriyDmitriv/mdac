document.addEventListener('DOMContentLoaded', function() {

    // --- Логіка для текстової каруселі в хедері ---
    const carouselDataElement = document.getElementById('header-carousel-data');
    if (carouselDataElement) {
        const carouselItems = JSON.parse(carouselDataElement.textContent);
        const carouselTextElement = document.querySelector('#text-carousel span');
        if (carouselTextElement && carouselItems.length > 0) {
            let currentItemIndex = 0;
            setInterval(() => {
                if (carouselTextElement.parentElement) {
                    carouselTextElement.parentElement.classList.add('fade-out');
                }
                setTimeout(() => {
                    currentItemIndex = (currentItemIndex + 1) % carouselItems.length;
                    carouselTextElement.textContent = carouselItems[currentItemIndex];
                    if (carouselTextElement.parentElement) {
                        carouselTextElement.parentElement.classList.remove('fade-out');
                    }
                }, 500);
            }, 3000);
        }
    }

    // --- Логіка для висувного меню ---
    const menuToggle = document.getElementById('menu-toggle');
    const sideMenu = document.getElementById('side-menu');
    if (menuToggle && sideMenu) {
        const menuLinks = sideMenu.querySelectorAll('a');
        const closeMenu = () => sideMenu.classList.remove('active');
        const toggleMenu = () => sideMenu.classList.toggle('active');
        menuToggle.addEventListener('click', (event) => {
            event.stopPropagation();
            toggleMenu();
        });
        menuLinks.forEach(link => link.addEventListener('click', closeMenu));
        document.addEventListener('click', (event) => {
            if (sideMenu.classList.contains('active') && !sideMenu.contains(event.target) && !menuToggle.contains(event.target)) {
                closeMenu();
            }
        });
    }

    // --- Логіка для Акордеону ---
    const accordionItems = document.querySelectorAll('.accordion-item');
    if (accordionItems.length > 0) {
        accordionItems.forEach(item => {
            const button = item.querySelector('.accordion-button');
            if (button) {
                button.addEventListener('click', () => {
                    const wasActive = item.classList.contains('active');
                    accordionItems.forEach(i => i.classList.remove('active'));
                    if (!wasActive) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }

    // --- Логіка для розгортання тексту ---
    const readMoreButtons = document.querySelectorAll('.read-more-btn');
    readMoreButtons.forEach(button => {
        button.addEventListener('click', () => {
            const wrapper = button.closest('.expandable-text-wrapper');
            const expandableText = wrapper.querySelector('.expandable');
            if (wrapper.classList.contains('expanded')) {
                wrapper.classList.remove('expanded');
                button.textContent = 'Розгорнути';
            } else {
                wrapper.classList.add('expanded');
                button.textContent = 'Згорнути';
            }
        });
    });

    // --- Логіка для карток переваг ---
    const advantageReadMoreButtons = document.querySelectorAll('.advantage-read-more');
    advantageReadMoreButtons.forEach(button => {
        button.addEventListener('click', () => {
            const card = button.closest('.advantage-card');
            if (card.classList.contains('expanded')) {
                card.classList.remove('expanded');
                button.textContent = 'Детальніше';
            } else {
                card.classList.add('expanded');
                button.textContent = 'Згорнути';
            }
        });
    });

    // --- УНІВЕРСАЛЬНА функція для ініціалізації каруселей ---
    function initCarousel(wrapperSelector) {
        const wrapper = document.querySelector(wrapperSelector);
        if (!wrapper) return;

        const track = wrapper.querySelector('.testimonial-carousel-track, .bonus-carousel-track');
        const nextButton = wrapper.querySelector('.carousel-button.next');
        const prevButton = wrapper.querySelector('.carousel-button.prev');
        const dotsNav = wrapper.querySelector('.carousel-dots');
        
        if (!track || !nextButton || !prevButton || !dotsNav) return;
        
        const slides = Array.from(track.children);
        if (slides.length === 0) return;

        let slideWidth = slides[0].getBoundingClientRect().width;
        let currentIndex = 0;
        let autoPlayInterval;

        dotsNav.innerHTML = ''; // Очищуємо, щоб не було дублів
        slides.forEach((slide, index) => {
            const dot = document.createElement('button');
            dot.classList.add('carousel-dot');
            if (index === 0) dot.classList.add('active');
            dotsNav.appendChild(dot);
            dot.addEventListener('click', () => {
                moveToSlide(index);
                resetAutoPlay();
            });
        });
        const dots = Array.from(dotsNav.children);

        const moveToSlide = (targetIndex) => {
            if (!track || !dots[currentIndex] || !dots[targetIndex]) return;
            track.style.transform = 'translateX(-' + slideWidth * targetIndex + 'px)';
            dots[currentIndex].classList.remove('active');
            dots[targetIndex].classList.add('active');
            currentIndex = targetIndex;
        };

        const resetAutoPlay = () => {
            clearInterval(autoPlayInterval);
            autoPlayInterval = setInterval(() => {
                nextButton.click();
            }, 5000);
        };

        nextButton.addEventListener('click', () => {
            moveToSlide((currentIndex + 1) % slides.length);
            resetAutoPlay();
        });

        prevButton.addEventListener('click', () => {
            moveToSlide((currentIndex - 1 + slides.length) % slides.length);
            resetAutoPlay();
        });

        window.addEventListener('resize', () => {
            slideWidth = slides[0].getBoundingClientRect().width;
            moveToSlide(currentIndex);
        });
        
        resetAutoPlay(); // Запускаємо автопрокрутку
    }

    // --- Ініціалізуємо ОБИДВІ каруселі ---
    initCarousel('.bonus-carousel-wrapper');
    initCarousel('.testimonial-carousel-wrapper');

    // --- Логіка для плаваючої кнопки ---
    const fabToggle = document.getElementById('fab-toggle');
    const fabWrapper = document.querySelector('.fab-wrapper');

    if (fabToggle && fabWrapper) {
        fabToggle.addEventListener('click', () => {
            fabWrapper.classList.toggle('active');
        });
    }

    // --- Логіка для контактної форми ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            
            const formData = new FormData(contactForm);
            const data = {
                situation: formData.get('situation'),
                name: formData.get('name'),
                phone: formData.get('phone')
            };

            try {
                const response = await fetch('/api/submit-form/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                    },
                    body: JSON.stringify(data)
                });

                const result = await response.json();
                
                const feedback = document.querySelector('.form-feedback');
                if (result.status === 'success') {
                    feedback.innerHTML = '<div class="thank-you-message"><h4>Дякуємо за заявку!</h4><p>Ми зв\'яжемося з вами найближчим часом.</p></div>';
                    contactForm.reset();
                } else {
                    feedback.innerHTML = '<div class="error-message"><p>Помилка: ' + result.message + '</p></div>';
                }
            } catch (error) {
                const feedback = document.querySelector('.form-feedback');
                feedback.innerHTML = '<div class="error-message"><p>Помилка з\'єднання. Спробуйте ще раз.</p></div>';
            }
        });
    }

    // --- Логіка для кнопки "Показати всі результати" ---
    const showAllResultsBtn = document.getElementById('show-all-results-btn');
    if (showAllResultsBtn) {
        showAllResultsBtn.addEventListener('click', () => {
            const resultsGrid = document.querySelector('.results-grid');
            if (resultsGrid) {
                resultsGrid.style.maxHeight = 'none';
                resultsGrid.style.overflow = 'visible';
                showAllResultsBtn.style.display = 'none';
            }
        });
    }

});