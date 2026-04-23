(() => {
  const heroSlides = Array.from(document.querySelectorAll('.hero-slide'));
  const carouselSlides = Array.from(document.querySelectorAll('.carousel-slide'));
  const slides = heroSlides.length ? heroSlides : carouselSlides;
  if (!slides.length) return;

  const dots = heroSlides.length ? Array.from(document.querySelectorAll('.hero-dots button')) : [];
  const prevBtn = document.querySelector('.carousel-arrow.left');
  const nextBtn = document.querySelector('.carousel-arrow.right');

  let index = 0;
  let timer;

  const showSlide = (i) => {
    index = (i + slides.length) % slides.length;
    slides.forEach((slide, idx) => slide.classList.toggle('active', idx === index));
    dots.forEach((dot, idx) => dot.classList.toggle('active', idx === index));
  };

  const next = () => showSlide(index + 1);
  const prev = () => showSlide(index - 1);

  const resetTimer = () => {
    clearInterval(timer);
    timer = setInterval(next, 5000);
  };

  dots.forEach((dot, i) => {
    dot.addEventListener('click', () => {
      showSlide(i);
      resetTimer();
    });
  });

  prevBtn?.addEventListener('click', () => {
    prev();
    resetTimer();
  });

  nextBtn?.addEventListener('click', () => {
    next();
    resetTimer();
  });

  resetTimer();
})();
