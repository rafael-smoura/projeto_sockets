"""
Cliente UDP – Serviço de Cálculo Remoto (Colorido)

Este cliente envia operações matemáticas para o servidor UDP e recebe a resposta
imediatamente, sem a necessidade de estabelecer conexão persistente.

Como usar:

    python3 client_udp.py
ou
    python client_udp.py
ou
    ./client_udp.py

Certifique-se de que o servidor UDP esteja em execução na porta configurada (default: 9999).
"""
__version__ = "1.0.0"
__author__ = "Rafael Silva Moura"

from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
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

nome_do_servico = "calc_udp"

print(f"{GREEN}Consultando servidor de nomes para o serviço '{nome_do_servico}'...{RESET}")

# conectar ao servidor de nomes via TCP
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# pedir o serviço
ns.send(nome_do_servico.encode())

# receber ip e porta do serviço UDP
resposta = ns.recv(1024).decode()
ns.close()

if resposta == "NOT_FOUND":
    print(f"{RED}Serviço não encontrado no servidor de nomes.{RESET}")
    exit()

ip, porta = resposta.split()
porta = int(porta)

print(f"{GREEN}Conectando ao serviço {nome_do_servico} em {ip}:{porta}...{RESET}\n")

# -------------------------------------------
# 2) Cliente UDP de cálculo
# -------------------------------------------

cliente = socket(AF_INET, SOCK_DGRAM)

# operação automática
operacao = "1"   # 1. Soma (+) 2. Subtração (-) 3. Multiplicação (*) 4. Divisão (/)
num1 = "20"
num2 = "15"

print(f"{CYAN}Iniciando operação automática: {num1} + {num2}...{RESET}\n")

# -------------------------------------------
# 3) Iniciar comunicação UDP
# -------------------------------------------

# manda só um pacote inicial para o servidor saber seu endereço
cliente.sendto("start".encode(), (ip, porta))

# medir tempo de operação
t_inicio = time.time()

# recebe menu
menu, _ = cliente.recvfrom(1024)
print(f"{BLUE}Menu do servidor recebido.{RESET}")

# envia operação (1=soma)
cliente.sendto(operacao.encode(), (ip, porta))
print(f"{YELLOW}Operação escolhida: Soma (+){RESET}")

# recebe pedido do primeiro número
cliente.recvfrom(1024)
cliente.sendto(num1.encode(), (ip, porta))
print(f"{YELLOW}Enviado primeiro número: {num1}{RESET}")

# recebe pedido do segundo número
cliente.recvfrom(1024)
cliente.sendto(num2.encode(), (ip, porta))
print(f"{YELLOW}Enviado segundo número: {num2}{RESET}")

# recebe resultado
resultado, _ = cliente.recvfrom(1024)
t_fim = time.time()

print(f"{GREEN}Resultado recebido: {resultado.decode()}{RESET}")
print(f"{CYAN}Tempo total da operação: {t_fim - t_inicio:.6f} segundos{RESET}\n")

cliente.close()
