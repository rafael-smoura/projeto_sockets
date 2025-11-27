from socket import AF_INET, SOCK_STREAM, socket

# 1️⃣ Criar o socket TCP
client_port = socket(AF_INET, SOCK_STREAM)
client_port.connect(("localhost", 1235))

# Recebe as escolhas do Servidor
mensagem = client_port.recv(1024).decode()
print(f"Calculadora CIN-TOP", mensagem)
escolha = input()

client_port.send(escolha.encode())

# Números para efetuar a operação
mensagem = client_port.recv(1024).decode()
print(mensagem)
numero1 = int(input())
client_port.send(numero1.encode())

mensagem = client_port.recv(1024).decode()
print(mensagem)
numero2 = int(input())
client_port.send(numero2.encode())

resultado = client_port.recv(1024).decode()
print(f"Resultado:", resultado)
client_port.close()