document.addEventListener("DOMContentLoaded", function() {
    const paymentOptions = document.querySelectorAll('.option');
  
    paymentOptions.forEach(function(option) {
      option.addEventListener("click", function() {
        paymentOptions.forEach(function(opt) {
          opt.classList.remove("selected");
        });
        option.classList.add("selected");
        const selectedMethod = option.getAttribute("data-method");
        console.log("Método selecionado:", selectedMethod);
      });
    });
  });
  