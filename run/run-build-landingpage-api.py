import subprocess
import os

# Adiciona o caminho do Docker Compose (caso necessário)
os.environ["PATH"] += r";C:\Program Files\Docker\Docker\resources\bin"

def executar_comando(comando):
    """Executa um comando sem abrir um novo terminal (funciona dentro do contêiner)."""
    subprocess.run(comando, shell=True)

executar_comando("docker-compose build landingpage_api")

executar_comando("docker-compose up -d landingpage_api")

