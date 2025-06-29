document.addEventListener('DOMContentLoaded', function() {

    // --- Логіка для текстової каруселі в хедері ---
    try {
        const carouselData = JSON.parse(document.getElementById('header-carousel-data').textContent);
        const carouselTextElement = document.querySelector('#text-carousel span');
        if (carouselTextElement && carouselData.length > 0) {
            let carouselItems = carouselData;
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
    } catch (e) {
        console.info("Header carousel data not found, will use static data if available.");
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

    // --- Логіка для Акордеону (Алгоритм та FAQ) ---
    const accordionItems = document.querySelectorAll('.accordion-item');
    if (accordionItems.length > 0) {
        accordionItems.forEach(item => {
            const button = item.querySelector('.accordion-button');
            if (button) {
                button.addEventListener('click', () => {
                    const wasActive = item.classList.contains('active');
                    accordionItems.forEach(i => {
                        if (i !== item) {
                           i.classList.remove('active');
                        }
                    });
                    item.classList.toggle('active');
                });
            }
        });
    }

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
        if (slides.length <= 1) {
            nextButton.style.display = 'none';
            prevButton.style.display = 'none';
            dotsNav.style.display = 'none';
            return;
        };

        let slideWidth = slides.length > 0 ? slides[0].getBoundingClientRect().width : 0;
        let currentIndex = 0;
        let autoPlayInterval;

        dotsNav.innerHTML = '';
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
            slideWidth = slides.length > 0 ? slides[0].getBoundingClientRect().width : 0;
            moveToSlide(currentIndex);
        });
        
        resetAutoPlay();
    }

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

    // --- Логіка для ВІДПРАВКИ КОНТАКТНОЇ ФОРМИ ---
    const contactForm = document.getElementById('contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', function(event) {
            event.preventDefault();
            
            const feedbackElement = contactForm.parentElement.querySelector('.form-feedback');
            if (!feedbackElement) {
                console.error("Feedback element not found");
                return;
            }

            const submitButton = contactForm.querySelector('button[type="submit"]');
            const formData = {
                situation: contactForm.querySelector('#situation').value,
                name: contactForm.querySelector('#name').value,
                phone: contactForm.querySelector('#phone').value,
            };
            const csrfToken = contactForm.querySelector('[name=csrfmiddlewaretoken]').value;

            submitButton.disabled = true;
            submitButton.textContent = 'Відправка...';

            fetch('/api/submit-form/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(formData)
            })
            .then(response => {
                if (response.ok) return response.json();
                throw new Error('Network response was not ok.');
            })
            .then(data => {
                if (data.status === 'success') {
                    feedbackElement.style.color = 'var(--accent-color)';
                    feedbackElement.textContent = 'Дякуємо! Вашу заявку успішно відправлено.';
                    contactForm.reset();
                } else {
                    feedbackElement.style.color = 'red';
                    feedbackElement.textContent = 'Сталася помилка. Спробуйте ще раз.';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                feedbackElement.style.color = 'red';
                feedbackElement.textContent = 'Сталася помилка мережі. Перевірте з\'єднання.';
            })
            .finally(() => {
                submitButton.disabled = false;
                submitButton.textContent = 'Написати';
            });
        });
    }

    // --- Логіка для КНОПКИ "РОЗГОРНУТИ" (Опис послуг) ---
    const expandableWrappers = document.querySelectorAll('.expandable-text-wrapper');
    expandableWrappers.forEach(wrapper => {
        const textBlock = wrapper.querySelector('.expandable');
        const button = wrapper.querySelector('.read-more-btn');

        if (textBlock && button) {
            if (textBlock.scrollHeight <= 105) {
                button.style.display = 'none';
            }
            button.addEventListener('click', () => {
                textBlock.classList.toggle('expanded');
                button.textContent = textBlock.classList.contains('expanded') ? 'Згорнути' : 'Розгорнути';
            });
        }
    });
    
    // --- Логіка для РОЗГОРТАННЯ КАРТОК ПЕРЕВАГ ---
    const advantageCards = document.querySelectorAll('.advantage-card');
    advantageCards.forEach(card => {
        const button = card.querySelector('.advantage-read-more');
        if (button) {
            button.addEventListener('click', (event) => {
                event.stopPropagation(); 
                
                const isCurrentlyExpanded = card.classList.contains('is-expanded');

                advantageCards.forEach(c => {
                    c.classList.remove('is-expanded');
                    const otherButton = c.querySelector('.advantage-read-more');
                    if(otherButton) {
                        otherButton.textContent = 'Детальніше';
                    }
                });

                if (!isCurrentlyExpanded) {
                    card.classList.add('is-expanded');
                    button.textContent = 'Згорнути';
                }
            });
        }
    });

    // --- ОНОВЛЕНА ЛОГІКА ДЛЯ КНОПКИ "ПОКАЗАТИ ВСІ / ЗГОРНУТИ" В РІШЕННЯХ ---
    const resultsGrid = document.querySelector('.results-grid');
    const showAllBtn = document.getElementById('show-all-results-btn');

    if (resultsGrid && showAllBtn) {
        const cards = Array.from(resultsGrid.children);
        const initialShowCount = 3; 

        const originalButtonText = showAllBtn.textContent;

        const collapseList = () => {
            cards.forEach((card, index) => {
                if (index >= initialShowCount) {
                    card.classList.add('is-hidden');
                    card.classList.remove('is-visible');
                }
            });
            showAllBtn.textContent = originalButtonText;
            resultsGrid.classList.remove('is-all-showing');
        };

        const expandList = () => {
             cards.forEach(card => {
                card.classList.remove('is-hidden');
                card.classList.add('is-visible');
            });
            showAllBtn.textContent = 'Згорнути';
            resultsGrid.classList.add('is-all-showing');
        };

        if (cards.length > initialShowCount) {
            collapseList();
        } else {
            showAllBtn.style.display = 'none';
        }

        showAllBtn.addEventListener('click', () => {
            const isExpanded = resultsGrid.classList.contains('is-all-showing');
            if (isExpanded) {
                collapseList();
            } else {
                expandList();
            }
        });
    }

});