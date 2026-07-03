#!/usr/bin/env python3
"""Gera um arquivo de áudio (fala) a partir de um texto.

Uso:
    python scripts/falar.py "Texto a ser falado" [caminho_saida]

Ordem de preferência:
  1. ElevenLabs (voz premium) — requer ELEVENLABS_API_KEY no ambiente e
     acesso de rede a api.elevenlabs.io. Saída em MP3.
  2. espeak-ng (voz offline) — instalado automaticamente se necessário.
     Saída em WAV.

Imprime no stdout o caminho do arquivo gerado.
"""
import os
import shutil
import subprocess
import sys

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
# Mesma voz padrão do jarvis.py (Daniel); sobrescreva com ELEVENLABS_VOICE_ID
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "onwK4e9ZLuTAKqWW03F9")


def falar_elevenlabs(texto: str, saida: str) -> str:
    import urllib.request

    url = (
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
        "?output_format=mp3_44100_128"
    )
    corpo = (
        '{"text": %s, "model_id": "eleven_turbo_v2_5", "language_code": "pt"}'
        % _json_string(texto)
    ).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=corpo,
        headers={
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        audio = resp.read()
    if not saida.endswith(".mp3"):
        saida = os.path.splitext(saida)[0] + ".mp3"
    with open(saida, "wb") as f:
        f.write(audio)
    return saida


def _json_string(texto: str) -> str:
    import json

    return json.dumps(texto, ensure_ascii=False)


def falar_espeak(texto: str, saida: str) -> str:
    if not shutil.which("espeak-ng"):
        subprocess.run(
            ["apt-get", "install", "-y", "-q", "espeak-ng"],
            check=True,
            capture_output=True,
        )
    if not saida.endswith(".wav"):
        saida = os.path.splitext(saida)[0] + ".wav"
    subprocess.run(
        ["espeak-ng", "-v", "pt-br", "-s", "150", "-w", saida, texto],
        check=True,
    )
    return saida


def main() -> None:
    if len(sys.argv) < 2:
        print("Uso: falar.py \"texto\" [saida]", file=sys.stderr)
        sys.exit(1)
    texto = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else "resposta.mp3"

    if ELEVENLABS_API_KEY:
        try:
            print(falar_elevenlabs(texto, saida))
            return
        except Exception as e:
            print(f"[ElevenLabs falhou: {e} — usando espeak-ng]", file=sys.stderr)
    print(falar_espeak(texto, saida))


if __name__ == "__main__":
    main()
