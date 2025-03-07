function checkScreenSize() {
  if (window.innerWidth > 840 && window.location.pathname !== "/desktop") {
    window.location.href = "/desktop";
  } else if (window.innerWidth > 500 && window.innerWidth <= 840 && window.location.pathname !== "/tablet") {
    window.location.href = "/tablet";
  } else if (window.innerWidth <= 500 && window.location.pathname !== "/mobile") {
    window.location.href = "/mobile";
  }
}

// Verifica o tamanho da tela ao carregar a página
window.addEventListener("load", checkScreenSize);

// Verifica o tamanho da tela ao redimensionar a janela
window.addEventListener("resize", checkScreenSize);
