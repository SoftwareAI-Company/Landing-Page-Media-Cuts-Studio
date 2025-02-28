
document.addEventListener('DOMContentLoaded', function() {
const fontSelector = document.getElementById('font-selector');
// Exemplo: atualiza a fonte de um elemento de preview
const previewElement = document.querySelector('.focusing-on-digital2'); 

if (fontSelector) {
    fontSelector.addEventListener('change', function() {
    const selectedFont = fontSelector.value;
    if (previewElement) {
        previewElement.style.fontFamily = selectedFont;
    }
    });
}
});
