import subprocess
import os

# Adiciona o caminho do Docker Compose
os.environ["PATH"] += r";C:\Program Files\Docker\Docker\resources\bin"
os.chdir(os.path.join(os.path.dirname(__file__)))

def executar_comando(comando):
    """Executa um comando sem abrir um novo terminal (funciona dentro do contêiner)."""
    subprocess.run(comando, shell=True)

# Executa o comando docker-compose
executar_comando("docker-compose up --build")

# executar_comando("docker-compose build nginx_server")

# executar_comando("docker-compose up -d nginx_server")

