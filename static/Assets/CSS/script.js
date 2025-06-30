function scrollCarrossel(direcao) {
  const carrossel = document.querySelector('.carrossel');
  const scrollAmount = 220;
  carrossel.scrollBy({
    left: direcao * scrollAmount,
    behavior: 'smooth'
  });
}
