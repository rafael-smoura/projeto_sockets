"""
Cliente UDP – Serviço de Cálculo Remoto

Este cliente envia operações matemáticas para o servidor UDP e recebe a resposta
imediatamente, sem a necessidade de estabelecer conexão persistente.

Sobre o funcionamento:

- Envia um datagrama UDP com a operação e valores.
- Aguarda o pacote de resposta do servidor.
- Exibe o resultado para o usuário.

Como usar:

    python3 client_udp.py
ou
    python client_udp.py
ou
    ./client_udp.py

Certifique-se de que o servidor UDP esteja em execução na porta configurada (default: 9999).
"""
__version__ = "Full"
__author__ = "Rafael Silva Moura"
__license__ = "Unlicense"


from socket import AF_INET, SOCK_DGRAM, SOCK_STREAM, socket
import time

# -------------------------------------------
# 1) Consulta ao Servidor de Nomes
# -------------------------------------------

nome_do_servico = "calc_udp"

# conectar ao servidor de nomes via TCP
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# pedir o serviço
ns.send(nome_do_servico.encode())

# receber ip e porta do serviço UDP
resposta = ns.recv(1024).decode()
ns.close()

if resposta == "NOT_FOUND":
    print("Serviço não encontrado no servidor de nomes.")
    exit()

ip, porta = resposta.split()
porta = int(porta)

print(f"Conectando ao serviço {nome_do_servico} em {ip}:{porta}...\n")

# -------------------------------------------
# 2) Cliente UDP de cálculo
# -------------------------------------------

cliente = socket(AF_INET, SOCK_DGRAM)

# operação automática 
operacao = "1"   # soma
num1 = "20"
num2 = "15"

print(f"Iniciando operação automática (20 + 15)...\n")

# -------------------------------------------
# 3) Iniciar comunicação UDP
# -------------------------------------------

# manda só um pacote inicial para o servidor saber seu endereço
cliente.sendto("start".encode(), (ip, porta))

# medir tempo de operação
t_inicio = time.time()

# recebe menu
menu, _ = cliente.recvfrom(1024)

# envia operação (1=soma)
cliente.sendto(operacao.encode(), (ip, porta))

# recebe pedido do primeiro número
cliente.recvfrom(1024)
cliente.sendto(num1.encode(), (ip, porta))

# recebe pedido do segundo número
cliente.recvfrom(1024)
cliente.sendto(num2.encode(), (ip, porta))

# recebe resultado
resultado, _ = cliente.recvfrom(1024)
t_fim = time.time()

print("Resultado recebido:", resultado.decode())
print(f"Tempo total da operação: {t_fim - t_inicio:.6f} segundos\n")

cliente.close()
