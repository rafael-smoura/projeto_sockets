"""
Servidor TCP – Serviço de Cálculo Remoto (Colorido)

Este servidor implementa um serviço remoto simples utilizando o protocolo TCP.
Ele aguarda conexões de clientes e processa requisições de operações matemáticas
(Soma, Subtração, Multiplicação e Divisão).

Como usar:

Basta executar:

    python3 server_tcp.py
ou
    python server_tcp.py
ou
    ./server_tcp.py

O servidor ficará escutando na porta configurada (default: 6666).
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

calculadora = f"""
{CYAN}=== Calculadora Remota ==={RESET}
Escolha a operação matemática:
{YELLOW}1.{RESET} Soma (+)
{YELLOW}2.{RESET} Subtração (-)
{YELLOW}3.{RESET} Multiplicação (*)
{YELLOW}4.{RESET} Divisão (/)
{YELLOW}5.{RESET} Sair (Exit)
"""

# Criar socket do servidor
server_port = socket(AF_INET, SOCK_STREAM)
server_port.bind(("localhost", 6666))
server_port.listen(5)
print(f"{GREEN}Servidor TCP iniciado na porta 6666. Registrando no Servidor de Nomes...{RESET}")

# -----------------------------
# REGISTRAR SERVIÇO NO NAME SERVER
# -----------------------------
try:
    name_server = socket(AF_INET, SOCK_STREAM)
    name_server.connect(("localhost", 7777))

    mensagem_registro = "calc_tcp 127.0.0.1 6666"
    name_server.send(mensagem_registro.encode())

    resposta = name_server.recv(1024).decode()
    print(f"{BLUE}Resposta do Servidor de Nomes:{RESET} {resposta}")

    name_server.close()
except Exception as e:
    print(f"{RED}Erro ao registrar no servidor de nomes:{RESET} {e}")

print(f"{GREEN}Aguardando conexões de clientes...{RESET}")

# -----------------------------
# LOOP PRINCIPAL DO SERVIDOR
# -----------------------------
while True:
    client_socket, client_addr = server_port.accept()
    print(f"{CYAN}Cliente conectado:{RESET} {client_addr}")

    fim = False
    while not fim:
        # Envia menu
        client_socket.send(calculadora.encode())

        # Recebe escolha
        escolha = client_socket.recv(1024).decode()

        if escolha == "5":
            fim = True
            break

        # Receber números
        client_socket.send(f"{YELLOW}Digite o primeiro número:{RESET}".encode())
        num1 = float(client_socket.recv(1024).decode())

        client_socket.send(f"{YELLOW}Digite o segundo número:{RESET}".encode())
        num2 = float(client_socket.recv(1024).decode())

        # Calcular resultado
        if escolha == "1":
            resultado = num1 + num2
        elif escolha == "2":
            resultado = num1 - num2
        elif escolha == "3":
            resultado = num1 * num2
        elif escolha == "4":
            if num2 != 0:
                resultado = num1 / num2
            else:
                resultado = f"{RED}Erro: divisão por zero{RESET}"
        else:
            resultado = f"{RED}Escolha inválida{RESET}"

        # Envia resultado
        client_socket.send(str(resultado).encode())

    client_socket.close()
    print(f"{CYAN}Cliente {client_addr} desconectado.{RESET}")
