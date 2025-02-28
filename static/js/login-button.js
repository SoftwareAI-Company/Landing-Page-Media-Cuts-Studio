document.addEventListener("DOMContentLoaded", function() {
  const loginButton = document.getElementById("loginButton");
  
  if (loginButton) {
    loginButton.addEventListener("click", async function() {
      const inputs = document.querySelectorAll('.custom-input');
      
      if (inputs.length >= 2) {
        const username = inputs[0].value;
        const password = inputs[1].value;
        
        try {
          const response = await fetch('https://pure-poorly-fly.ngrok-free.app/proxy-login', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            credentials: 'include', 
            body: JSON.stringify({
              username: username,
              password: password
            })
          });

          const data = await response.json();

          if (response.ok) {
            alert('Login realizado com sucesso!');
            window.location.href = 'https://9b8f8a9c-586c-4bc4-8338-2d1a33f8235f-00-2gvd4cn9hpni2.picard.replit.dev/ControlPanel';
          } else {
            alert('Erro no login: ' + (data.message || data.error));
          }

        } catch (error) {
          console.error('Erro ao fazer login:', error);
          alert('Erro ao tentar fazer login. Por favor, tente novamente.');
        }

      } else {
        console.error("Os inputs não foram encontrados!");
        alert("Por favor, preencha usuário e senha.");
      }
    });
  }
});
