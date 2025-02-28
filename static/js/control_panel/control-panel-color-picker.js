document.addEventListener('DOMContentLoaded', function() {
    // Seleciona todos os elementos que funcionam como botão para escolher a cor
    const colorButtons = document.querySelectorAll('.button-secondary');

    // Para cada botão encontrado, adiciona o evento de clique
    colorButtons.forEach(button => {
      button.addEventListener('click', function(e) {
        e.preventDefault();

        // Busca, dentro do botão, o elemento que exibe o código da cor e a elipse
        const colorCodeElement = button.querySelector('.confirm-copy-24');
        const ellipseElement = button.querySelector('.ellipse-19, .ellipse-192');

        // Cria um input do tipo "color" que será usado para disparar o seletor nativo
        const colorInput = document.createElement('input');
        colorInput.type = 'color';
        // Deixamos o input invisível, mas "clicável"
        colorInput.style.opacity = 0;
        colorInput.style.position = 'absolute';
        colorInput.style.border = 'none';

        // Posiciona o input sobre o botão (para que o seletor seja associado ao mesmo)
        const rect = button.getBoundingClientRect();
        colorInput.style.left = rect.left + window.scrollX + 'px';
        colorInput.style.top = rect.top + window.scrollY + 'px';

        // Se houver um código de cor já exibido, define-o como valor inicial do input
        if (colorCodeElement) {
          let initialColor = colorCodeElement.textContent.trim();
          if (!initialColor.startsWith('#')) {
            initialColor = '#' + initialColor;
          }
          colorInput.value = initialColor;
        }

        // Anexa o input temporário ao body
        document.body.appendChild(colorInput);

        // Ao alterar a cor, atualiza o texto e o fundo da elipse
        colorInput.addEventListener('input', function() {
          const selectedColor = colorInput.value;
          if (colorCodeElement) {
            colorCodeElement.textContent = selectedColor;
          }
          if (ellipseElement) {
            ellipseElement.style.backgroundColor = selectedColor;
          }
        });

        // Dispara o clique no input para abrir o seletor de cores
        colorInput.click();

        // Após a seleção (evento "change"), remove o input do DOM
        colorInput.addEventListener('change', function() {
          document.body.removeChild(colorInput);
        });
      });
    });
  });