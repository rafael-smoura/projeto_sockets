"""
Servidor de Nomes (Service Name Server)
---------------------------------------

Este programa implementa um servidor de nomes simples utilizando o protocolo TCP.
O servidor permite registrar e consultar serviços dentro de uma rede local,
funcionando como um pequeno "DNS" interno do projeto.

Funcionamento:

- Usa um dicionário interno `services` para armazenar:
      nome_do_serviço  ->  (ip, porta)

- O servidor escuta na porta 7777 (localhost).
- Cada cliente se conecta via TCP, envia uma mensagem e recebe uma resposta.

Formato das mensagens:

1) Registro automático (3 partes)
        <nome> <ip> <porta>
    Exemplo:
        calculadora 127.0.0.1 6666

    O servidor registra o serviço se ele ainda não existir.
    Resposta: "OK"

2) Consulta (1 parte)
        <nome>
    Exemplo:
        calculadora

    Se o serviço existir:
        <ip> <porta>
    Caso contrário:
        NOT_FOUND

3) Entrada inválida
    Qualquer mensagem que não tenha 1 ou 3 partes dispara:
        ERROR

Como usar:

    python3 service_names.py
ou
    python service_names.py
ou
    ./service_names.py

O servidor permanecerá ativo aguardando conexões e exibindo no terminal
cada registro e cada consulta recebida.
"""
__version__ = "Full"
__author__ = "Rafael Silva Moura"
__license__ = "Unlicense"

from socket import AF_INET, SOCK_STREAM, socket

services = {}   # dicionário com: nome -> (ip, porta)

server_port = socket(AF_INET, SOCK_STREAM)
server_port.bind(("localhost", 7777))
server_port.listen(5)

print("Servidor de Nomes iniciado na porta 7777")

while True:
    client_socket, client_addr = server_port.accept()
    print(f"Conexão recebida de {client_addr}")

    # Recebe a mensagem
    mensagem = client_socket.recv(1024).decode().strip()
    print("Recebido:", mensagem)

    partes = mensagem.split()

    # ---------------------------------------------------
    # 1) REGISTRO AUTOMÁTICO (3 partes)
    # ---------------------------------------------------
    if len(partes) == 3:
        nome = partes[0]
        ip = partes[1]
        porta = int(partes[2])

        # Só adiciona se ainda não existe
        if nome not in services:
            services[nome] = (ip, porta)
            print(f"✔ Serviço registrado: {nome} -> {ip}:{porta}")
        else:
            print(f"ℹ Serviço '{nome}' já estava registrado.")

        client_socket.send("OK".encode())

    # ---------------------------------------------------
    # 2) CONSULTA (1 parte)
    # ---------------------------------------------------
    elif len(partes) == 1:
        nome = partes[0]

        if nome in services:
            ip, porta = services[nome]
            resposta = f"{ip} {porta}"
        else:
            resposta = "NOT_FOUND"

        client_socket.send(resposta.encode())

    # ---------------------------------------------------
    # 3) QUALQUER OUTRA COISA
    # ---------------------------------------------------
    else:
        client_socket.send("ERROR".encode())

    client_socket.close()
    print(f"Cliente {client_addr} desconectado.\n")
