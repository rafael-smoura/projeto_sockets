"""
Cliente de Consulta — Serviço Inexistente (client_notfound.py) (Colorido)

Este script testa o comportamento do Servidor de Nomes consultando um serviço
que não existe, exibindo mensagens coloridas para sucesso ou falha.
"""
__version__ = "1.0.0"
__author__ = "Rafael Silva Moura"

from socket import AF_INET, SOCK_STREAM, socket

# Códigos de cores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# Nome de um serviço INEXISTENTE
nome_servico = "servico_que_nao_existe"

print(f"{GREEN}Conectando ao servidor de nomes para consultar o serviço '{nome_servico}'...{RESET}")

# Conectar ao servidor de nomes
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# Enviar nome do serviço inexistente
ns.send(nome_servico.encode())

# Receber a resposta
resposta = ns.recv(1024).decode()
ns.close()

print(f"\n{CYAN}Consulta realizada:{RESET} {nome_servico}")
print(f"{BLUE}Resposta do Servidor de Nomes:{RESET} {resposta}")

if resposta == "NOT_FOUND":
    print(f"\n{GREEN}✔ Teste bem-sucedido! O servidor de nomes respondeu corretamente.{RESET}\n")
else:
    print(f"\n{RED}⚠ Algo errado: o servidor encontrou um serviço que não existe.{RESET}\n")
