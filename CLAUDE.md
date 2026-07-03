# GustavoRodrigues

Assistente JARVIS (voz, PT-BR) — `jarvis.py` roda localmente no Mac com
Claude + Whisper + ElevenLabs.

## Modo voz no Claude Code (web/celular)

O usuário gosta de receber respostas em áudio no chat. Quando ele pedir
resposta por voz/áudio (ou o modo voz já estiver ativo na conversa), use a
skill `responder-por-voz`: gere o áudio com `python scripts/falar.py
"texto" <scratchpad>/resposta.mp3` e envie com `SendUserFile`, além do
texto. Mantenha o modo voz ativo nos turnos seguintes até ele pedir para
parar.

O script usa ElevenLabs se `ELEVENLABS_API_KEY` estiver definida e a rede
permitir `api.elevenlabs.io`; caso contrário usa espeak-ng offline.
