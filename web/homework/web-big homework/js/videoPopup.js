(() => {
  const cards = document.querySelectorAll('[data-video]');

  const openVideo = (url) => {
    const overlay = document.createElement('div');
    overlay.className = 'video-overlay';
    overlay.innerHTML = `<iframe src="${url}" frameborder="0" allowfullscreen allow="autoplay"></iframe>`;
    document.body.appendChild(overlay);

    const close = () => overlay.remove();
    overlay.addEventListener('click', close);
    const handleEsc = (e) => e.key === 'Escape' && close();
    document.addEventListener('keydown', handleEsc, { once: true });
  };

  cards.forEach(card => {
    card.addEventListener('click', () => openVideo(card.dataset.video));
  });
})();
