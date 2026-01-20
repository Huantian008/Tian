(() => {
  const navbar = document.querySelector('.navbar');
  const backTop = document.querySelector('.back-to-top');
  const currentPage = document.body.dataset.page;
  const navLinks = document.querySelectorAll('.nav-links a');

  navLinks.forEach(link => {
    if (link.dataset.page === currentPage) {
      link.classList.add('active');
    }
  });

  const onScroll = () => {
    if (navbar) {
      navbar.classList.toggle('scrolled', window.scrollY > 40);
    }
    if (backTop) {
      backTop.classList.toggle('show', window.scrollY > 320);
    }
  };

  window.addEventListener('scroll', onScroll);
  onScroll();

  backTop?.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
})();
