"""
============================================================
      Assistente Pessoal Virtual - Versão 2.0
============================================================

Descrição:
    Este script permite a comunicação com um modelo de linguagem via LM Studio,
    configurado para atuar como um assistente pessoal virtual. O assistente ajuda
    o usuário com informações gerais, organização, lembretes e tarefas diárias.

Funcionalidades:
  - Registro detalhado de todas as interações em um arquivo de log.
  - Comando para reiniciar o histórico da conversa ("reset").
  - Comando para encerrar a sessão ("exit").
  - Tratamento de exceções para uma experiência mais robusta.

Requisitos:
  - LM Studio deve estar rodando em 'http://localhost:1234/v1'
  - Biblioteca 'openai' instalada
  - Modelo configurado corretamente (substitua 'model-identifier' se necessário)
"""

import openai           # Biblioteca para interagir com a API do LM Studio
import datetime         # Biblioteca para trabalhar com data e hora

# Configuração da conexão com o LM Studio
# A variável 'api_conector' será utilizada para enviar requisições ao modelo
api_conector = openai.OpenAI(
    base_url='http://localhost:1234/v1',  # URL base do LM Studio
    api_key='lm-studio'                   # Chave de API (exemplo)
)

# Histórico da conversa, iniciado com uma mensagem de sistema definindo o contexto do assistente
historico_conversa = [
    {
        'role': 'system',
        'content': 'Você é um assistente pessoal virtual. Ajude o usuário com informações, organização e tarefas diárias.'
    }
]

def registrar_log(mensagem_log: str):
    """
    Registra uma mensagem no arquivo de log com a data e hora atual.

    Parâmetros:
      mensagem_log (str): A mensagem que será registrada no log.
    """
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log_conversa.txt", "a", encoding="utf-8") as arquivo:
        arquivo.write(f"[{timestamp}] {mensagem_log}\n")

def obter_resposta(texto_usuario: str) -> str:
    """
    Envia a mensagem do usuário para o modelo e retorna a resposta do assistente.

    Parâmetros:
      texto_usuario (str): A mensagem digitada pelo usuário.

    Retorna:
      str: Conteúdo da resposta gerada pelo assistente ou mensagem de erro.
    """
    global historico_conversa

    # Adiciona a mensagem do usuário ao histórico e registra no log
    historico_conversa.append({'role': 'user', 'content': texto_usuario})
    registrar_log(f"Usuário: {texto_usuario}")

    try:
        # Solicita a resposta ao modelo, enviando todo o histórico da conversa
        resposta_api = api_conector.chat.completions.create(
            model='model-identifier',   # Identificador do modelo (ajuste conforme necessário)
            messages=historico_conversa,
            temperature=1               # Controla a aleatoriedade da resposta
        )
    except Exception as erro_api:
        mensagem_erro = f"Erro ao comunicar com o modelo: {erro_api}"
        registrar_log(mensagem_erro)
        return mensagem_erro

    try:
        # Extrai a mensagem de resposta retornada pelo modelo
        mensagem_assistente = resposta_api.choices[0].message
    except Exception as erro_extracao:
        mensagem_erro = f"Erro ao processar a resposta do modelo: {erro_extracao}"
        registrar_log(mensagem_erro)
        return mensagem_erro

    # Atualiza o histórico com a resposta do assistente e registra no log
    historico_conversa.append({'role': mensagem_assistente.role, 'content': mensagem_assistente.content})
    registrar_log(f"Assistente: {mensagem_assistente.content}")

    return mensagem_assistente.content

def iniciar_conversa():
    """
    Gerencia o loop principal do chat, permitindo que o usuário interaja
    continuamente com o assistente pessoal virtual.

    Comandos especiais:
      - "exit": Encerra a sessão.
      - "reset": Reinicia o histórico da conversa.
    """
    print("=================================================")
    print("Bem-vindo ao Assistente Pessoal Virtual!")
    print("Digite 'exit' para encerrar ou 'reset' para reiniciar o histórico.")
    print("=================================================")

    while True:
        # Solicita a entrada do usuário e remove espaços desnecessários
        entrada = input("Você: ").strip()

        # Comando para encerrar a sessão
        if entrada.lower() == "exit":
            print("Encerrando a sessão. Até logo!")
            registrar_log("Sessão encerrada pelo usuário.")
            break

        # Comando para reiniciar o histórico da conversa
        if entrada.lower() == "reset":
            global historico_conversa
            historico_conversa = [
                {
                    'role': 'system',
                    'content': 'Você é um assistente pessoal virtual. Ajude o usuário com informações, organização e tarefas diárias.'
                }
            ]
            print("Histórico da conversa reiniciado.")
            registrar_log("Histórico reiniciado pelo usuário.")
            continue

        # Processa a resposta do assistente com base na entrada do usuário
        resposta_texto = obter_resposta(entrada)
        print("Assistente:", resposta_texto)

if __name__ == "__main__":
    iniciar_conversa()
