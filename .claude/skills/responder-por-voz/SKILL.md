---
name: responder-por-voz
description: >
  Responder o usuário com um arquivo de áudio (voz), no estilo JARVIS.
  Use quando o usuário pedir resposta "por voz", "por áudio", "falando",
  "modo JARVIS", ou quando o modo voz estiver ativo na conversa. Depois
  de ativado, TODAS as respostas seguintes devem incluir áudio até o
  usuário pedir para parar.
---

# Responder por voz

Gere um arquivo de áudio da sua resposta e envie ao usuário no chat.

## Como fazer

1. Escreva a resposta em texto normalmente (curta e natural, boa para ser
   ouvida — de uma a seis frases; evite listas, tabelas, código e emojis
   no texto que será falado).
2. Gere o áudio com o script do repositório, salvando no scratchpad:

   ```bash
   python scripts/falar.py "Texto da resposta aqui" <scratchpad>/resposta.mp3
   ```

   O script imprime o caminho do arquivo gerado (MP3 via ElevenLabs se
   `ELEVENLABS_API_KEY` estiver configurada e a rede permitir; senão WAV
   via espeak-ng offline).
3. Envie o arquivo ao usuário com a ferramenta `SendUserFile`, com uma
   legenda curta (ex.: "🔊 Resposta em áudio").
4. Inclua também a resposta em texto na mensagem final, para o usuário
   poder ler se preferir.

## Persistência do modo voz

- Quando o usuário ativar o modo voz, continue respondendo com áudio em
  TODOS os turnos seguintes, sem que ele precise pedir de novo.
- Desative apenas quando o usuário pedir (ex.: "pode parar com o áudio",
  "só texto").

## Voz premium (ElevenLabs)

Para usar a voz do JARVIS da conta ElevenLabs do usuário, o ambiente
precisa de:

- Variável `ELEVENLABS_API_KEY` (e opcionalmente `ELEVENLABS_VOICE_ID`)
  configurada nas variáveis de ambiente do Environment no Claude Code web.
- Política de rede do Environment liberando o domínio `api.elevenlabs.io`.

Sem isso, o script cai automaticamente na voz offline (espeak-ng).
