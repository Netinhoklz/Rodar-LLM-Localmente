# Assistente Pessoal Virtual

Este é um chatbot interativo em Python que atua como um assistente pessoal virtual. Ele utiliza a API do LM Studio para ajudar com informações, organização e lembretes diretamente pelo terminal.

## Funcionalidades

- **Chat Interativo:** Comunicação via terminal.
- **Registro de Log:** Todas as interações são registradas com data e hora.
- **Comandos Especiais:**
  - `reset`: Reinicia o histórico da conversa.
  - `exit`: Encerra a sessão.

## Requisitos

- Python 3.6+
- LM Studio rodando em `http://localhost:1234/v1`
- Biblioteca OpenAI (instale com `pip install openai`)

## Uso

Basta executar:

```bash
python assistente.py
