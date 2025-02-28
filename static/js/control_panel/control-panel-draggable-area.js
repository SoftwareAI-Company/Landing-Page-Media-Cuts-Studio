// Referências aos elementos
const dropArea = document.getElementById('drop-area');
const fileInput = document.getElementById('file-input');
const videoPreview = document.getElementById('video-preview');
const videoTitle = document.getElementById('video-title');

// Evento de arrastar e soltar
dropArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropArea.classList.add('dragover');
});

dropArea.addEventListener('dragleave', () => {
    dropArea.classList.remove('dragover');
});

dropArea.addEventListener('drop', (e) => {
    e.preventDefault();
    dropArea.classList.remove('dragover');
    const file = e.dataTransfer.files[0];
    if (file) {
    handleFileUpload(file);
    }
});

// Clique na área de upload
dropArea.addEventListener('click', () => {
    fileInput.click();
});

// Seleção de arquivo
fileInput.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
    handleFileUpload(file);
    }
});

// Função para carregar e exibir o arquivo
function handleFileUpload(file) {
    console.log("Arquivo enviado:", file.name);

    // Exibir nome do vídeo
    videoTitle.textContent = file.name; // Exibe o nome do arquivo
    videoTitle.style.visibility = 'visible'; // Tornar o nome do vídeo visível

    // Exibir o vídeo como capa
    const videoURL = URL.createObjectURL(file);
    videoPreview.src = videoURL;
    videoPreview.style.visibility = 'visible'; // Tornar o vídeo visível
    videoPreview.load();
    videoPreview.pause(); // Pausar o vídeo
    videoPreview.currentTime = 0; // Colocar o vídeo no início

    // Ocultar a área de upload
    dropArea.classList.add('hidden');
}