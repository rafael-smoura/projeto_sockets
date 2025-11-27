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
server_port.bind(("localhost", 1235))
server_port.listen(5)
print("Servidor iniciado. Aguardando conexões...")

while True:
    client_socket, client_addr = server_port.accept()
    print(f"Cliente conectado: {client_addr}")

    fim = False
    while not fim:
        # Envia menu
        client_socket.send(calculadora.encode())

        # Recebe escolha
        escolha = client_socket.recv(1024).decode()

        # Verificar se é opção de sair
        fim = False
        if escolha == "5":
            fim = True

        if not fim:
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

            # Enviar resultado
            client_socket.send(str(resultado).encode())

    # Fechar conexão do cliente
    client_socket.close()
    print(f"Cliente {client_addr} desconectado.")
