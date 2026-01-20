(() => {
  const items = document.querySelectorAll('.fade-in');
  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.15 });
    items.forEach(el => io.observe(el));
  } else {
    items.forEach(el => el.classList.add('visible'));
  }

  const ticker = document.querySelector('.ticker-inner');
  if (ticker) {
    ticker.innerHTML = `${ticker.innerHTML} · ${ticker.innerHTML}`;
  }
})();
