from socket import AF_INET, SOCK_DGRAM, socket

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
server_port.bind(("localhost", 1235))
print("Servidor UDP iniciado. Aguardando clientes...")

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

        # Verificar se é opção de sair
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
                if num2 != 0:
                    resultado = num1 / num2
                else:
                    resultado = "Erro: divisão por zero"
            else:
                resultado = "Escolha inválida"

            # Enviar resultado
            server_port.sendto(str(resultado).encode(), client_addr)

    print(f"Cliente {client_addr} desconectado.")
