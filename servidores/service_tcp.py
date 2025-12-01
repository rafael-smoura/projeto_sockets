"""
Servidor TCP – Serviço de Cálculo Remoto

Este servidor implementa um serviço remoto simples utilizando o protocolo TCP.
Ele aguarda conexões de clientes e processa requisições de operações matemáticas
(Soma, Subtração, Multiplicação e Divisão).

Sobre o funcionamento:

- Utiliza TCP, garantindo entrega confiável e orientada a conexão.
- Cada cliente conectado é atendido individualmente.
- As mensagens seguem o formato definido no cliente TCP.

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

calculadora = """
=== Calculadora Remota ===
Escolha a operação matemática:
1. Soma (+)
2. Subtração (-)
3. Multiplicação (*)
4. Divisão (/)
5. Sair (Exit)
"""

# Criar socket do servidor uma vez
server_port = socket(AF_INET, SOCK_STREAM)
server_port.bind(("localhost", 6666))
server_port.listen(5)
print("Servidor TCP iniciado na porta 6666. Registrando no Servidor de Nomes...")

# -----------------------------
# REGISTRAR SERVIÇO NO NAME SERVER
# -----------------------------
try:
    name_server = socket(AF_INET, SOCK_STREAM)
    name_server.connect(("localhost", 7777))

    # formato: nome ip porta   (opção A que você escolheu)
    mensagem_registro = "calc_tcp 127.0.0.1 6666"
    name_server.send(mensagem_registro.encode())

    resposta = name_server.recv(1024).decode()
    print(f"Resposta do Servidor de Nomes: {resposta}")

    name_server.close()
except Exception as e:
    print("Erro ao registrar no servidor de nomes:", e)

print("Aguardando conexões de clientes...")

# -----------------------------
# LOOP PRINCIPAL DO SERVIDOR
# -----------------------------
while True:
    client_socket, client_addr = server_port.accept()
    print(f"Cliente conectado: {client_addr}")

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
        client_socket.send("Digite o primeiro número:".encode())
        num1 = float(client_socket.recv(1024).decode())

        client_socket.send("Digite o segundo número:".encode())
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
                resultado = "Erro: divisão por zero"
        else:
            resultado = "Escolha inválida"

        # Envia resultado
        client_socket.send(str(resultado).encode())

    client_socket.close()
    print(f"Cliente {client_addr} desconectado.")
