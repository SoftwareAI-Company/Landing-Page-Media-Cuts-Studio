document.addEventListener("DOMContentLoaded", function() {
    const urlParams = new URLSearchParams(window.location.search);
    const priceParam = urlParams.get("price");

    let plano;
    if (priceParam === "29") {
      plano = "content creator";
    } else if (priceParam === "139") {
      plano = "studio";
    } else {
      alert("Preço inválido na URL.");
      return;
    }

    const payNowButton = document.querySelector('.block-pay-now .button');
    
    if (payNowButton) {
      payNowButton.addEventListener("click", function() {
        const selectedOption = document.querySelector('.option.selected');
        
        if (selectedOption) {
          const paymentMethod = selectedOption.getAttribute("data-method");
          const email = document.querySelector('.email-input').value;
  
          if (!email) {
            alert("Por favor, insira seu email.");
            return; 
          }

          fetch("https://landing.mediacutsstudio.com/proxy-checkout", {
            method: "POST",
            headers: {
              "Content-Type": "application/json"
            },
            body: JSON.stringify({
              email: email,
              assinatura: true,
              plano: plano          
            }),
          })
          .then(response => {
            console.log("Resposta do servidor:", response);
          
            if (!response.ok) {
              throw new Error("Erro na requisição. Status: " + response.status);
            }
            return response.json()
              .catch(error => {
                console.error("Erro ao converter a resposta para JSON:", error);
                throw new Error("Erro ao converter a resposta para JSON");
              });
          })
          .then(data => {
            console.log("Dados recebidos:", data); 
          
            if (data.sessionId) {
              const stripe = Stripe("pk_test_51QpX90Cvm2cRLHtdoF7n2Ea4sRRjYBx8Csiii0e6M6ECTJJ8fKaQ1DKpJApfJZH5hIkWRojaMmaxY9sEcS50tspB00DF2IA12h");
              stripe.redirectToCheckout({ sessionId: data.sessionId })
              .then(() => {
                window.location.href = "https://mediacutsstudio.com/checkout/sucess"; 
              });
            } else {
              alert("Erro ao criar a sessão de pagamento.");
            }
          })
          .catch(error => {
            console.error("Erro ao enviar a requisição:", error);
            alert("Erro ao processar o pagamento.");
          });
        } else {
          // Caso nenhuma opção esteja selecionada, avise o usuário
          alert("Por favor, selecione um método de pagamento.");
        }
      });
    }
});
