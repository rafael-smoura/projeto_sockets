from socket import AF_INET, SOCK_DGRAM, socket

# Endereço do servidor
server_addr = ("localhost", 1235)

# Criar o socket UDP
client_port = socket(AF_INET, SOCK_DGRAM)

# Recebe o menu do servidor
mensagem, _ = client_port.recvfrom(1024)
print("Calculadora CIN-TOP", mensagem.decode())

# Escolha do usuário
escolha = input()
client_port.sendto(escolha.encode(), server_addr)

# Receber e enviar o primeiro número
mensagem, _ = client_port.recvfrom(1024)
print(mensagem.decode())
numero1 = input()
client_port.sendto(numero1.encode(), server_addr)

# Receber e enviar o segundo número
mensagem, _ = client_port.recvfrom(1024)
print(mensagem.decode())
numero2 = input()
client_port.sendto(numero2.encode(), server_addr)

# Receber o resultado
resultado, _ = client_port.recvfrom(1024)
print("Resultado:", resultado.decode())

# Fechar o socket
client_port.close()
