# J.A.R.V.I.S. Voice Assistant

> *"Good day, sir. J.A.R.V.I.S. online and fully operational."*

Um assistente de voz que combina **Claude (Anthropic)** com a personalidade do **J.A.R.V.I.S.** do Iron Man. Fale com ele, ele responde com a voz britânica e formal do assistente do Tony Stark.

## Como funciona

```
Microfone → Whisper (transcrição local) → Claude API (cérebro) → ElevenLabs (voz) → Caixas de som
```

## Pré-requisitos

- Python 3.10+
- Microfone funcionando
- [ffmpeg](https://ffmpeg.org/download.html) instalado (necessário para o Whisper)
- Conta na [Anthropic](https://console.anthropic.com) (obrigatório)
- Conta na [ElevenLabs](https://elevenlabs.io) (opcional, mas recomendado para a voz do JARVIS)

## Instalação

```bash
# 1. Clone o repositório
git clone <repo-url>
cd GustavoRodrigues

# 2. Crie um ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas chaves de API
```

## Configuração do `.env`

```env
ANTHROPIC_API_KEY=sk-ant-...        # Obrigatório
ELEVENLABS_API_KEY=sk_...           # Opcional (mas faz muita diferença na voz)
ELEVENLABS_VOICE_ID=onwK4e9ZLuTAKqWW03F9  # Voz padrão: Daniel (britânico)
```

## Como rodar

```bash
python jarvis.py
```

Pressione **ENTER** para falar. O JARVIS para de gravar automaticamente após 1.5 segundos de silêncio. Use **Ctrl+C** para encerrar.

## Escolhendo a melhor voz no ElevenLabs

Para uma experiência mais fiel ao JARVIS:

1. Acesse [elevenlabs.io/voice-library](https://elevenlabs.io/voice-library)
2. Pesquise por **"JARVIS"** ou **"British male"**
3. Copie o Voice ID da voz escolhida
4. Cole no `.env` como `ELEVENLABS_VOICE_ID`

Vozes recomendadas do catálogo padrão:
- **Daniel** (`onwK4e9ZLuTAKqWW03F9`) — britânico, formal ✓
- **George** (`JBFqnCBsd6RMkjVDRZzb`) — britânico, maduro

## Sem ElevenLabs?

Se você não definir `ELEVENLABS_API_KEY`, o JARVIS usa **pyttsx3** automaticamente — uma engine de TTS local, gratuita, sem necessidade de internet. A qualidade da voz é inferior, mas funciona.

## Tecnologias

| Componente | Tecnologia |
|---|---|
| Transcrição de voz | [OpenAI Whisper](https://github.com/openai/whisper) (roda localmente) |
| Inteligência | [Claude claude-sonnet-4-6](https://www.anthropic.com) via API |
| Síntese de voz | [ElevenLabs](https://elevenlabs.io) ou pyttsx3 |
| Captura de áudio | sounddevice + numpy |
