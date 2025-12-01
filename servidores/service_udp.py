"""
Servidor UDP – Serviço de Cálculo Remoto (Colorido)

Este servidor implementa o mesmo serviço matemático do servidor TCP, porém
utilizando o protocolo UDP, que é mais simples e sem conexão.

Como usar:

    python3 server_udp.py
ou
    python server_udp.py
ou
    ./server_udp.py

O servidor ficará escutando na porta configurada (default: 9999).
"""
__version__ = "1.0.0"
__author__ = "Rafael Silva Moura"

from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket

# Códigos de cores ANSI
RED = "\033[91m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
CYAN = "\033[96m"
RESET = "\033[0m"

calculadora = f"""
{CYAN}=== Calculadora Remota ==={RESET}
Escolha a operação matemática:
{YELLOW}1.{RESET} Soma (+)
{YELLOW}2.{RESET} Subtração (-)
{YELLOW}3.{RESET} Multiplicação (*)
{YELLOW}4.{RESET} Divisão (/)
{YELLOW}5.{RESET} Sair (Exit)
"""

# Criar socket UDP
server_port = socket(AF_INET, SOCK_DGRAM)
server_port.bind(("localhost", 9999))
print(f"{GREEN}Servidor UDP iniciado na porta 9999. Registrando no Servidor de Nomes...{RESET}")

# -----------------------------------------------------
# REGISTRAR SERVIÇO NO SERVIDOR DE NOMES (TCP)
# -----------------------------------------------------
try:
    name_server = socket(AF_INET, SOCK_STREAM)
    name_server.connect(("localhost", 7777))

    mensagem_registro = "calc_udp 127.0.0.1 9999"
    name_server.send(mensagem_registro.encode())

    resposta = name_server.recv(1024).decode()
    print(f"{BLUE}Resposta do Servidor de Nomes:{RESET} {resposta}")

    name_server.close()
except Exception as e:
    print(f"{RED}Erro ao registrar no servidor de nomes:{RESET} {e}")

print(f"{GREEN}Aguardando clientes UDP...{RESET}")

# -----------------------------------------------------
# LOOP PRINCIPAL DO SERVIDOR UDP
# -----------------------------------------------------
while True:
    # Receber qualquer mensagem inicial do cliente para obter o endereço
    msg, client_addr = server_port.recvfrom(1024)
    print(f"{CYAN}Cliente conectado:{RESET} {client_addr}")

    fim = False
    while not fim:
        # Envia menu
        server_port.sendto(calculadora.encode(), client_addr)

        # Recebe escolha
        escolha_msg, client_addr = server_port.recvfrom(1024)
        escolha = escolha_msg.decode()

        fim = (escolha == "5")

        if not fim:
            # Receber primeiro número
            server_port.sendto(f"{YELLOW}Digite o primeiro número:{RESET}".encode(), client_addr)
            num1_msg, client_addr = server_port.recvfrom(1024)
            num1 = float(num1_msg.decode())

            # Receber segundo número
            server_port.sendto(f"{YELLOW}Digite o segundo número:{RESET}".encode(), client_addr)
            num2_msg, client_addr = server_port.recvfrom(1024)
            num2 = float(num2_msg.decode())

            # Calcular resultado
            if escolha == "1":
                resultado = num1 + num2
            elif escolha == "2":
                resultado = num1 - num2
            elif escolha == "3":
                resultado = num1 * num2
            elif escolha == "4":
                resultado = f"{RED}Erro: divisão por zero{RESET}" if num2 == 0 else num1 / num2
            else:
                resultado = f"{RED}Escolha inválida{RESET}"

            # Enviar resultado
            server_port.sendto(str(resultado).encode(), client_addr)

    print(f"{CYAN}Cliente {client_addr} desconectado.{RESET}")
