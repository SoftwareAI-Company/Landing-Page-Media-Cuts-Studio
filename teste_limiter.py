import time
import numpy as np
from ctypes import cast, POINTER
import pythoncom
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume, IAudioMeterInformation

# Definir limite de decibéis
DB_LIMIT = -23
STABILITY_THRESHOLD = 20  
STABILITY_TIME = 30  

def list_chrome_sessions():
    """Lista as sessões de áudio do Chrome disponíveis."""
    sessions = AudioUtilities.GetAllSessions()
    chrome_sessions = []
    for session in sessions:
        if session.Process and session.Process.name().lower() == "chrome.exe":
            chrome_sessions.append(session)
    return chrome_sessions

def mute_chrome_session(session):
    """Silencia a sessão do Chrome usando pycaw."""
    session.SimpleAudioVolume.SetMute(1, None)
    print("🔇 Mutado devido ao excesso de volume!")

def unmute_chrome_session(session):
    """Desmuta a sessão do Chrome usando pycaw."""
    session.SimpleAudioVolume.SetMute(0, None)
    print("🔊 Desmutado após volume estabilizado.")

def monitor_chrome_volume(chrome_session):
    """Monitora o volume da sessão do Chrome e silencia se ultrapassar o limite, com detecção de estabilidade."""
    # Obtém a interface de medição de áudio da sessão
    audio_meter = chrome_session._ctl.QueryInterface(IAudioMeterInformation)

    # Variáveis para monitoramento da estabilidade
    stable_count = 0
    last_volume_db = None


    while True:
        peak = audio_meter.GetPeakValue()  # Valor entre 0.0 e 1.0
        if peak > 0:
            volume_db = 20 * np.log10(peak)
        else:
            volume_db = -100

        print(f"🔊 Volume Atual da sessão Chrome: {volume_db:.2f} dB (Peak: {peak:.2f})")

        # Verifica se o volume está dentro de um intervalo estável
        if last_volume_db is not None and abs(volume_db - last_volume_db) < STABILITY_THRESHOLD:
            stable_count += 1
        else:
            stable_count = 0
        
        if stable_count >= STABILITY_TIME:
            # Volume estabilizado, desmuta a sessão
            unmute_chrome_session(chrome_session)

        # Se ultrapassar o limite de volume, mute
        if volume_db > DB_LIMIT:
            mute_chrome_session(chrome_session)

        last_volume_db = volume_db
        time.sleep(1)

if __name__ == "__main__":
    print("🔊 Monitorando o volume de uma sessão do Chrome...")

    # Inicializa a COM antes de usar o pycaw
    pythoncom.CoInitialize()

    try:
        chrome_sessions = list_chrome_sessions()
        if not chrome_sessions:
            print("Nenhuma sessão do Chrome encontrada.")
        else:
            print("Sessões do Chrome encontradas:")
            for idx, session in enumerate(chrome_sessions):
                print(f"{idx}: {session.Process.name()} (PID: {session.Process.pid})")

            indice = int(input("Escolha o índice da sessão que deseja monitorar: "))
            if indice < 0 or indice >= len(chrome_sessions):
                print("Índice inválido.")
            else:
                monitor_chrome_volume(chrome_sessions[indice])
    finally:
        pythoncom.CoUninitialize()
