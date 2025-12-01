"""
Servidor UDP – Serviço de Cálculo Remoto

Este servidor implementa o mesmo serviço matemático do servidor TCP, porém
utilizando o protocolo UDP, que é mais simples e sem conexão.

Sobre o funcionamento:

- Usa UDP (sem conexão, mais rápido, porém sem garantia de entrega).
- Recebe pacotes contendo operações matemáticas.
- Processa e envia a resposta diretamente ao cliente, usando o endereço recebido.

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

calculadora = """
=== Calculadora Remota ===
Escolha a operação matemática:
1. Soma (+)
2. Subtração (-)
3. Multiplicação (*)
4. Divisão (/)
5. Sair (Exit)
"""

# Criar socket UDP
server_port = socket(AF_INET, SOCK_DGRAM)
server_port.bind(("localhost", 9999))
print("Servidor UDP iniciado na porta 9999. Registrando no Servidor de Nomes...")

# -----------------------------------------------------
# REGISTRAR SERVIÇO NO SERVIDOR DE NOMES (TCP)
# -----------------------------------------------------
try:
    name_server = socket(AF_INET, SOCK_STREAM)
    name_server.connect(("localhost", 7777))

    mensagem_registro = "calc_udp 127.0.0.1 9999"
    name_server.send(mensagem_registro.encode())

    resposta = name_server.recv(1024).decode()
    print(f"Resposta do Servidor de Nomes: {resposta}")

    name_server.close()
except Exception as e:
    print("Erro ao registrar no servidor de nomes:", e)

print("Aguardando clientes UDP...")

# -----------------------------------------------------
# LOOP PRINCIPAL DO SERVIDOR UDP
# -----------------------------------------------------
while True:
    # Receber qualquer mensagem inicial do cliente para obter o endereço
    msg, client_addr = server_port.recvfrom(1024)
    print(f"Cliente conectado: {client_addr}")

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
            server_port.sendto("Digite o primeiro número:".encode(), client_addr)
            num1_msg, client_addr = server_port.recvfrom(1024)
            num1 = float(num1_msg.decode())

            # Receber segundo número
            server_port.sendto("Digite o segundo número:".encode(), client_addr)
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
                resultado = num1 / num2 if num2 != 0 else "Erro: divisão por zero"
            else:
                resultado = "Escolha inválida"

            # Enviar resultado
            server_port.sendto(str(resultado).encode(), client_addr)

    print(f"Cliente {client_addr} desconectado.")
