"""
Cliente de Consulta — Serviço Inexistente (client_notfound.py)

Este script testa o comportamento do Servidor de Nomes consultando um serviço
que **não existe**. É útil para validar que o servidor responde corretamente
com "NOT_FOUND" quando um serviço requisitado não está registrado.

Descrição:
- Conecta-se ao Servidor de Nomes via TCP (localhost:7777).
- Envia apenas o nome do serviço como mensagem.
- Recebe a resposta do servidor e imprime o resultado.
- Verifica automaticamente se a resposta é "NOT_FOUND" e informa o sucesso/falha do teste.

Como usar:
- Antes de rodar, certifique-se de que o servidor de nomes (service_names.py)
  esteja em execução e escutando em localhost:7777.

Execução:

    python3 client_notfound.py
ou
    python client_notfound.py
ou
    ./client_notfound.py

Personalização:
- Para testar outro serviço inexistente, altere a variável `nome_servico`.
- Para apontar a outro host/porta do servidor de nomes, modifique a chamada
  `ns.connect(("localhost", 7777))`.

Comportamento esperado:
- Se o servidor não encontrar o serviço, responde "NOT_FOUND" → o script
  exibirá "Teste bem-sucedido".
- Se o servidor responder algo diferente, o script sinaliza uma falha.

Observações:
- Este cliente é apenas para fins de teste/validação e não implementa lógica
  de reconexão, timeouts avançados ou autenticação.
"""

__version__ = "Full"
__author__ = "Rafael Silva Moura"
__license__ = "Unlicense"


from socket import AF_INET, SOCK_STREAM, socket

# Nome de um serviço INEXISTENTE
nome_servico = "servico_que_nao_existe"

# Conectar ao servidor de nomes
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# Enviar nome do serviço inexistente
ns.send(nome_servico.encode())

# Receber a resposta
resposta = ns.recv(1024).decode()
ns.close()

print("\nConsulta realizada:", nome_servico)
print("Resposta do Servidor de Nomes:", resposta)

if resposta == "NOT_FOUND":
    print("\n✔ Teste bem-sucedido! O servidor de nomes respondeu corretamente.\n")
else:
    print("\n⚠ Algo errado: o servidor encontrou um serviço que não existe.\n")
