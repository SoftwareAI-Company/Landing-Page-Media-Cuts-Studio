import requests
# Extrai os campos do JSON
email = "freitasalexandre810@gmail.com"
subscription_plan = "content creator"
api_key = "apikey-content-creator-v9SK1GsZdFESjnyRK2hRQrguQ_jzv60jUsQNSL-S2NI"
API_URL_Shortify = "https://api.mediacutsstudio.com/api/Media_Cuts_Studio/Alfred/Mode/Gmail"
# data = {
#     "plan": subscription_plan,
#     "email": email,
#     "panelapikey": api_key
# }
# headers = {
#     "Content-Type": "application/json",
#     "X-API-KEY": api_key  
# }
# response = requests.post(API_URL_Shortify, json=data, headers=headers)
# responsejson = response.json()
# print(response.status_code)
# print(responsejson)
import base64
import os
import requests
import zipfile
import io

# URL do novo endpoint
url = "https://webhook.mediacutsstudio.com/webhook_video_zip"  # Atualizado para a nova rota

# Caminho da pasta contendo os vídeos
video_folder = "videos"  # Substitua pelo caminho correto da pasta com os vídeos
zip_filename = "videos.zip"

diretorio_script = os.path.dirname(os.path.abspath(__file__))
# Caminho da pasta contendo os vídeos
video_folder = os.path.abspath(
    os.path.join(diretorio_script,
                "videos"
                )
    )

zip_filename = os.path.abspath(
    os.path.join(diretorio_script,
                "videos.zip"
                )
    )
# Cria um buffer de memória para o ZIP
zip_buffer = io.BytesIO()

# Compacta os arquivos no buffer
with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zipf:
    for video_file in os.listdir(video_folder):
        video_path = os.path.join(video_folder, video_file)
        if os.path.isfile(video_path) and video_file.endswith(".mp4"):
            zipf.write(video_path, arcname=video_file)  # Adiciona ao ZIP

# Move o ponteiro para o início do buffer
zip_buffer.seek(0)

# Codifica o ZIP em Base64
zip_encoded = base64.b64encode(zip_buffer.getvalue()).decode("utf-8")

# Define a API key do usuário
api_key = "apikey-content-creator-oDNBpNMkfBJmnb2OEIdB_50WRO8yDT03UU4UGuh-Jk4"

# Monta o payload JSON
payload = {
    "arquivo_zip": zip_encoded,
    "api_key": api_key,
    "filename": zip_filename
}

# Envia a requisição POST com o JSON
response = requests.post(url, json=payload)

# Exibe a resposta do servidor
print("Status Code:", response.status_code)
print("Response:", response.json())