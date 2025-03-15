import time
import numpy as np
import wave
import pyaudio
from scipy.signal import correlate
from ctypes import cast, POINTER
import pythoncom
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation

# DB_LIMIT = -23
# STABILITY_THRESHOLD = 5  
# STABILITY_TIME = 10  
DB_LIMIT = -26.03
STABILITY_THRESHOLD = 2  
STABILITY_TIME = 5  

AUDIO_CHUNK_DURATION = 3  # Duração da gravação (segundos)
RECORDED_AUDIO_FILE = "sound_livepix.wav"  # Arquivo para armazenar áudio detectado

def list_chrome_sessions():
    """Lista as sessões de áudio do Chrome disponíveis."""
    sessions = AudioUtilities.GetAllSessions()
    return [s for s in sessions if s.Process and s.Process.name().lower() == "chrome.exe"]

def mute_chrome_session(session):
    """Silencia a sessão do Chrome."""
    session.SimpleAudioVolume.SetMute(1, None)
    print("🔇 Mutado devido ao excesso de volume!")

def unmute_chrome_session(session):
    """Desmuta a sessão do Chrome."""
    session.SimpleAudioVolume.SetMute(0, None)
    print("🔊 Desmutado após volume estabilizado.")

def record_audio(duration=AUDIO_CHUNK_DURATION, filename=RECORDED_AUDIO_FILE):
    """Grava um trecho de áudio do sistema."""
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=1024)
    frames = []
    print("🎙 Gravando trecho de áudio...")
    for _ in range(int(44100 / 1024 * duration)):
        frames.append(stream.read(1024))
    stream.stop_stream()
    stream.close()
    p.terminate()
    with wave.open(filename, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
        wf.setframerate(44100)
        wf.writeframes(b"".join(frames))
    print("✅ Trecho gravado com sucesso!")

def load_audio(filename):
    """Carrega um arquivo WAV e converte para array NumPy."""
    with wave.open(filename, "rb") as wf:
        frames = wf.readframes(wf.getnframes())
        return np.frombuffer(frames, dtype=np.int16)


def compare_audio(current_audio):
    """Compara o áudio atual com o trecho gravado."""
    recorded_audio = load_audio(RECORDED_AUDIO_FILE)
    if len(recorded_audio) > 0 and len(current_audio) > 0:
        correlation = correlate(recorded_audio, current_audio, mode='valid')
        similarity = np.max(np.abs(correlation)) / (np.linalg.norm(recorded_audio) * np.linalg.norm(current_audio))
        print(f"🔍 Similaridade do áudio detectado: {similarity:.12f}")
        return similarity > 0.5  # Reduzindo o limite para capturar variações
    return False


def monitor_chrome_volume(chrome_session):
    """Monitora o volume da sessão do Chrome e silencia padrões detectados."""
    audio_meter = chrome_session._ctl.QueryInterface(IAudioMeterInformation)
    stable_count = 0
    last_volume_db = None
    
    while True:
        peak = audio_meter.GetPeakValue()
        volume_db = 20 * np.log10(peak) if peak > 0 else -100
        print(f"🔊 Volume Atual: {volume_db:.2f} dB (Peak: {peak:.2f})")
        
        if last_volume_db is not None and abs(volume_db - last_volume_db) < STABILITY_THRESHOLD:
            stable_count += 1
        else:
            stable_count = 0
        
        if stable_count >= STABILITY_TIME:
            unmute_chrome_session(chrome_session)
        
        if volume_db > DB_LIMIT:
            mute_chrome_session(chrome_session)

        
        last_volume_db = volume_db
        time.sleep(1)

if __name__ == "__main__":
    print("🔊 Monitoramento de volume do Chrome...")
    pythoncom.CoInitialize()
    try:
        choice = input("Deseja gravar um trecho de áudio antes de monitorar? (s/n): ").strip().lower()
        if choice == 's':
            record_audio()
        
        chrome_sessions = list_chrome_sessions()
        if not chrome_sessions:
            print("Nenhuma sessão do Chrome encontrada.")
        else:
            for idx, session in enumerate(chrome_sessions):
                print(f"{idx}: {session.Process.name()} (PID: {session.Process.pid})")
            indice = int(input("Escolha a sessão para monitorar: "))
            if 0 <= indice < len(chrome_sessions):
                monitor_chrome_volume(chrome_sessions[indice])
    finally:
        pythoncom.CoUninitialize()
