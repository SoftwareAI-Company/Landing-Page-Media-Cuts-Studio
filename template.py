import requests
from datetime import datetime, timedelta
import pytz

# URL do endpoint da API Flask 
API_URL = " https://dynamic-supreme-jackal.ngrok-free.app/api/Media_Cuts_Studio/Shortify/Mode/Create"

api_key = "apikey-content-creator-B5BUpJgM47aMvKUsnwnGiLp3driRbHkhyPEGNFKeKUI"
# Adicione a API Key no header da requisição
headers = {
    "X-API-KEY": api_key  
}
def agendar_shortify():
    tz = pytz.timezone('America/Sao_Paulo')
    scheduled_time = (datetime.now(tz) + timedelta(minutes=1)).strftime('%Y-%m-%d %H:%M:%S')

    canal_do_yt = "felquinhas"
    SubtitleVerticalReference = "6"
    SubtitleFontsize = "39"
    SubtitleColor = "white"
    SubtitleAnimation = "Slow Fade-Out"
    SubtitleEffects = "Glow Effect"
    SubtitleFontName = "Future"

    CaptionsAlignment = "2"
    CaptionsColor = "aqua"
    CaptionsFontName = "Future"
    CaptionsFontsize = 8
    CaptionsPrimaryColour = "&HC0C0C0"
    CaptionsSecondaryColour = "&H8080"
    CaptionsOutlineColour = "&H0"
    CaptionsBackColour = "&H0"
    CaptionsBold = 1
    CaptionsItalic = 0
    CaptionsUnderline = 0
    CaptionsOutline = 3
    CaptionsShadow = 1
    CaptionsRevealEffectInitialColor = "&HCCCC33&"
    CaptionsRevealEffectFinalColor = "&H0099FF&"
    Cutting_seconds = 60

    watermark_image = "watermask.png"
    text_watermark = "@cortesdofelquinhas"
    

    # Cria o payload com todos os parâmetros necessários
    payload = {
        "date_time": scheduled_time,  # Data e hora no formato 'YYYY-MM-DD HH:MM:SS'
        "canal_do_yt": canal_do_yt,
        "watermark_image": watermark_image,
        "text_watermark": text_watermark,
        "Cutting_seconds": Cutting_seconds,
        "api_key": api_key,
        "SubtitleColor": SubtitleColor,
        "SubtitleAnimation": SubtitleAnimation,  
        "SubtitleFontName": SubtitleFontName,
        "SubtitleEffects": SubtitleEffects,
        "SubtitleFontsize": SubtitleFontsize,
        "SubtitleVerticalReference": SubtitleVerticalReference,
        "CaptionsColor": CaptionsColor,
        "CaptionsFontName": CaptionsFontName,
        "CaptionsAlignment": CaptionsAlignment,
        "CaptionsFontsize": CaptionsFontsize,
        "CaptionsPrimaryColour": CaptionsPrimaryColour,
        "CaptionsSecondaryColour": CaptionsSecondaryColour,
        "CaptionsOutlineColour": CaptionsOutlineColour,
        "CaptionsBackColour": CaptionsBackColour,
        "CaptionsBold": CaptionsBold,
        "CaptionsItalic": CaptionsItalic,
        "CaptionsUnderline": CaptionsUnderline,
        "CaptionsOutline": CaptionsOutline,
        "CaptionsShadow": CaptionsShadow,
        "CaptionsRevealEffectInitialColor": CaptionsRevealEffectInitialColor,
        "CaptionsRevealEffectFinalColor": CaptionsRevealEffectFinalColor
    }
    
    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        print(f"Resposta da API:{response.content}")
    except requests.exceptions.RequestException as err:
        print(f"Erro ao enviar a requisição: {err}")
