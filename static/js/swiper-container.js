
var swiper = new Swiper(".swiper-container", {
  loop: true, // Loop infinito
  autoplay: {
    delay: 3000, // Tempo entre slides
    disableOnInteraction: false, // Continua rodando após interação
  },
  navigation: {
    nextEl: ".swiper-button-next",
    prevEl: ".swiper-button-prev",
  },
  pagination: {
    el: ".swiper-pagination",
    clickable: true,
  },
});
