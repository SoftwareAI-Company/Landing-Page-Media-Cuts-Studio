document.addEventListener("DOMContentLoaded", function() {
  const inputContainers = document.querySelectorAll('.input, .input2');

  inputContainers.forEach((container, index) => {
    const frame = container.querySelector('.frame-11019');
    if (!frame) return;

    const inputElement = document.createElement('input');
    inputElement.className = "custom-input"; 

    if (index === 0) {
      inputElement.type = "text";
      inputElement.placeholder = "Enter your username";
    } else if (index === 1) {
      inputElement.type = "password";
      inputElement.placeholder = "Enter your password";
    }

    frame.innerHTML = "";
    frame.appendChild(inputElement);
  });
});
