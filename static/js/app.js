document.addEventListener('DOMContentLoaded', () => {
  const currentPath = window.location.pathname;
  const navLinks = document.querySelectorAll('.nav a');

  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (href && currentPath.includes(href.replace(/\/$/, ''))) {
      link.style.color = '#4f46e5';
      link.style.fontWeight = '800';
    }
  });
});
