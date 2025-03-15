import subprocess
import os

# Adiciona o caminho do Docker Compose (caso necessário)
os.environ["PATH"] += r";C:\Program Files\Docker\Docker\resources\bin"

def executar_comando(comando):
    """Executa um comando sem abrir um novo terminal (funciona dentro do contêiner)."""
    subprocess.run(comando, shell=True)

# Executa o build apenas para o serviço internal_api
executar_comando("docker-compose build internal_celery_worker")

# Reinicia apenas o serviço internal_api com a nova build
executar_comando("docker-compose up -d internal_celery_worker")
