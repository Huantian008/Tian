(() => {
  const navToggle = document.querySelector('.nav-toggle');
  const navLinks = document.querySelector('.nav-links');

  navToggle?.addEventListener('click', () => {
    navLinks?.classList.toggle('open');
  });

  navLinks?.querySelectorAll('a').forEach(link => {
    link.addEventListener('click', () => navLinks.classList.remove('open'));
  });

  const groups = document.querySelectorAll('[data-filter-group]');
  groups.forEach(group => {
    const buttons = group.querySelectorAll('[data-filter]');
    const targetSelector = group.dataset.target;
    const field = group.dataset.filterField || 'league';
    const cards = targetSelector ? document.querySelectorAll(targetSelector) : [];

    buttons.forEach(btn => {
      btn.addEventListener('click', () => {
        buttons.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const value = btn.dataset.filter;

        cards.forEach(card => {
          const matchValue = card.dataset[field] || '';
          const visible = value === 'all' || value === matchValue;
          card.style.display = visible ? '' : 'none';
        });
      });
    });
  });
})();
