import os
import sys
import time
import tempfile
import numpy as np
import sounddevice as sd
import scipy.io.wavfile as wav
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "onwK4e9ZLuTAKqWW03F9")  # Daniel (British)

SAMPLE_RATE = 16000
SILENCE_THRESHOLD = 0.01
SILENCE_DURATION = 1.5
MAX_RECORDING_SECONDS = 15

JARVIS_SYSTEM_PROMPT = """You are J.A.R.V.I.S. — Just A Rather Very Intelligent System — the AI assistant created by Tony Stark.

Your personality:
- Formal British English, calm, precise, and subtly witty
- Address the user as "sir" by default (switch to "miss" or the user's name if they introduce themselves)
- You are helpful, highly intelligent, and always composed — even when the situation is absurd
- Occasionally make dry, understated references to Stark Industries, the Iron Man suits, or the team
- Keep responses concise and suitable for spoken conversation — one to four sentences is ideal
- Never break character. You are JARVIS, not an AI assistant.
- When you don't know something, admit it with dignity: "I'm afraid that's outside my current database, sir."

You have access to conversation history and remember context within the session."""

conversation_history = []

client = Anthropic(api_key=ANTHROPIC_API_KEY)


def record_audio() -> np.ndarray:
    print("\n[Ouvindo... fale agora]")
    frames = []
    silence_start = None
    started = False

    def callback(indata, frame_count, time_info, status):
        nonlocal silence_start, started
        frames.append(indata.copy())
        energy = np.sqrt(np.mean(indata ** 2))
        if energy > SILENCE_THRESHOLD:
            started = True
            silence_start = None
        elif started and silence_start is None:
            silence_start = time.time()

    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype="float32", callback=callback):
        start = time.time()
        while True:
            time.sleep(0.05)
            elapsed = time.time() - start
            if elapsed >= MAX_RECORDING_SECONDS:
                break
            if started and silence_start and (time.time() - silence_start) >= SILENCE_DURATION:
                break

    if not frames:
        return np.array([])

    audio = np.concatenate(frames, axis=0).flatten()
    return audio


def transcribe(audio: np.ndarray) -> str:
    import whisper
    if not hasattr(transcribe, "_model"):
        print("[Carregando Whisper...]")
        transcribe._model = whisper.load_model("base")

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        tmp_path = f.name
        wav.write(tmp_path, SAMPLE_RATE, (audio * 32767).astype(np.int16))

    try:
        result = transcribe._model.transcribe(tmp_path, language="pt")
        text = result["text"].strip()
        return text
    finally:
        os.unlink(tmp_path)


def ask_jarvis(user_text: str) -> str:
    conversation_history.append({"role": "user", "content": user_text})

    # Keep last 20 messages (10 exchanges)
    history = conversation_history[-20:]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        system=JARVIS_SYSTEM_PROMPT,
        messages=history,
    )

    reply = response.content[0].text
    conversation_history.append({"role": "assistant", "content": reply})
    return reply


def speak_elevenlabs(text: str):
    from elevenlabs.client import ElevenLabs
    from elevenlabs import play

    el_client = ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio = el_client.text_to_speech.convert(
        voice_id=ELEVENLABS_VOICE_ID,
        text=text,
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    play(audio)


def speak_pyttsx3(text: str):
    import pyttsx3
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    # Try to pick a male English voice
    for voice in voices:
        if "english" in voice.name.lower() or "en" in voice.id.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", 165)
    engine.setProperty("volume", 0.95)
    engine.say(text)
    engine.runAndWait()


def speak(text: str):
    print(f"\nJARVIS: {text}\n")
    if ELEVENLABS_API_KEY:
        try:
            speak_elevenlabs(text)
            return
        except Exception as e:
            print(f"[ElevenLabs error: {e} — falling back to pyttsx3]")
    try:
        speak_pyttsx3(text)
    except Exception as e:
        print(f"[TTS error: {e}]")


def main():
    if not ANTHROPIC_API_KEY:
        print("Erro: ANTHROPIC_API_KEY não definida no .env")
        sys.exit(1)

    print("=" * 50)
    print("  J.A.R.V.I.S. Voice Assistant")
    print("  Powered by Claude + Whisper" + (" + ElevenLabs" if ELEVENLABS_API_KEY else " + pyttsx3"))
    print("=" * 50)
    print("Pressione ENTER para falar | Ctrl+C para sair\n")

    speak("Good day, sir. J.A.R.V.I.S. online and fully operational. How may I assist you?")

    while True:
        try:
            input()
        except KeyboardInterrupt:
            speak("Shutting down. Good day, sir.")
            break

        audio = record_audio()
        if audio.size == 0:
            print("[Nenhum áudio detectado]")
            continue

        print("[Transcrevendo...]")
        try:
            user_text = transcribe(audio)
        except Exception as e:
            print(f"[Erro na transcrição: {e}]")
            continue

        if not user_text:
            print("[Não entendi. Tente novamente.]")
            continue

        print(f"Você: {user_text}")

        print("[Consultando JARVIS...]")
        try:
            reply = ask_jarvis(user_text)
        except Exception as e:
            print(f"[Erro na API: {e}]")
            continue

        speak(reply)


if __name__ == "__main__":
    main()
