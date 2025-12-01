"""
Cliente TCP – Serviço de Cálculo Remoto (Colorido)

Este cliente se conecta ao servidor TCP e permite que o "usuário escolha" uma
operação matemática e envie os valores para processamento.

Como usar:

    python3 client_notfound.py
ou
    python client_notfound.py
ou
    ./client_notfound.py

Certifique-se de que o servidor TCP esteja em execução na porta configurada (default: 6666).
"""
__version__ = "1.0.0"
__author__ = "Rafael Silva Moura"

from socket import AF_INET, SOCK_STREAM, socket
import time

# Códigos de cores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

# -------------------------------------------
# 1) Consulta ao Servidor de Nomes
# -------------------------------------------

nome_do_servico = "calc_tcp"

print(f"{GREEN}Consultando servidor de nomes para o serviço '{nome_do_servico}'...{RESET}")

# conectar ao servidor de nomes via TCP
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# pedir o serviço
ns.send(nome_do_servico.encode())

# receber ip e porta do serviço TCP
resposta = ns.recv(1024).decode()
ns.close()

if resposta == "NOT_FOUND":
    print(f"{RED}Serviço não encontrado no servidor de nomes.{RESET}")
    exit()

ip, porta = resposta.split()
porta = int(porta)

print(f"{GREEN}Conectando ao serviço {nome_do_servico} em {ip}:{porta}...{RESET}\n")

# -------------------------------------------
# 2) Cliente TCP de cálculo
# -------------------------------------------

cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((ip, porta))

# operação automática
operacao = "1"   # 1. Soma (+) 2. Subtração (-) 3. Multiplicação (*) 4. Divisão (/)
num1 = "20"
num2 = "15"

print(f"{CYAN}Iniciando operação automática: {num1} + {num2}...{RESET}\n")

# medir tempo da operação
t_inicio = time.time()

# recebe menu
menu = cliente.recv(1024).decode()
print(f"{BLUE}Menu do servidor recebido.{RESET}")

# envia operação
cliente.send(operacao.encode())
print(f"{YELLOW}Operação escolhida: Soma (+){RESET}")

# recebe pedido do primeiro número
cliente.recv(1024)
cliente.send(num1.encode())
print(f"{YELLOW}Enviado primeiro número: {num1}{RESET}")

# recebe pedido do segundo número
cliente.recv(1024)
cliente.send(num2.encode())
print(f"{YELLOW}Enviado segundo número: {num2}{RESET}")

# recebe resultado final
resultado = cliente.recv(1024).decode()
t_fim = time.time()

print(f"{GREEN}Resultado recebido: {resultado}{RESET}")
print(f"{CYAN}Tempo total da operação: {t_fim - t_inicio:.6f} segundos{RESET}\n")

cliente.close()
