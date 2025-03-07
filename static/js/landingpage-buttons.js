document.addEventListener("DOMContentLoaded", function() {
  // Botão do plano Studio
  const studioBtn = document.querySelector('.become-a-studio');
  if (studioBtn) {
    studioBtn.addEventListener("click", function() {
      const studioPrice = 139;
      window.location.href = "/plan/studio/checkout?price=" + encodeURIComponent(studioPrice);
    });
  }
  
  // Botão do plano Content Creator
  const contentCreatorBtn = document.querySelector('.start-creating-content');
  if (contentCreatorBtn) {
    contentCreatorBtn.addEventListener("click", function() {
      const contentCreatorPrice = 29;
      window.location.href = "/plan/content-creator/checkout?price=" + encodeURIComponent(contentCreatorPrice);
    });
  }
  
  // Botão do plano Startup
  const startupBtn = document.querySelector('.join-new-startup');
  if (startupBtn) {
    startupBtn.addEventListener("click", function() {
      const startupPrice = 0;
      window.location.href = "/plan/startup/checkout?price=" + encodeURIComponent(startupPrice);
    });
  }
});
