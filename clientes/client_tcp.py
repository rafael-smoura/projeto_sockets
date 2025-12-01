"""
Cliente TCP – Serviço de Cálculo Remoto

Este cliente se conecta ao servidor TCP e permite que o "usuário escolha" uma
operação matemática e envie os valores para processamento.

Sobre o funcionamento:

- Conecta-se ao servidor via socket TCP.
- Envia comandos no formato esperado pelo servidor.
- Recebe e exibe o resultado enviado pelo servidor.

Como usar:

    python3 client_notfound.py
ou
    python client_notfound.py
ou
    ./client_notfound.py

Certifique-se de que o servidor TCP esteja em execução na porta configurada (default: 6666).
"""
__version__ = "1.0.0"
__author__ = "Rafael Silva Moura"


from socket import AF_INET, SOCK_STREAM, socket
import time

# -------------------------------------------
# 1) Consulta ao Servidor de Nomes
# -------------------------------------------

nome_do_servico = "calc_tcp"

# conectar ao servidor de nomes via TCP
ns = socket(AF_INET, SOCK_STREAM)
ns.connect(("localhost", 7777))

# pedir o serviço
ns.send(nome_do_servico.encode())

# receber ip e porta do serviço TCP
resposta = ns.recv(1024).decode()
ns.close()

if resposta == "NOT_FOUND":
    print("Serviço não encontrado no servidor de nomes.")
    exit()

ip, porta = resposta.split()
porta = int(porta)

print(f"Conectando ao serviço {nome_do_servico} em {ip}:{porta}...\n")

# -------------------------------------------
# 2) Cliente TCP de cálculo
# -------------------------------------------

cliente = socket(AF_INET, SOCK_STREAM)
cliente.connect((ip, porta))

# operação automática
operacao = "1"   # 1. Soma (+) 2. Subtração (-) 3. Multiplicação (*) 4. Divisão (/)
num1 = "20"
num2 = "15"

print("Iniciando operação automática (20 + 15)...\n")

# medir tempo da operação
t_inicio = time.time()

# recebe menu
menu = cliente.recv(1024).decode()

# envia operação
cliente.send(operacao.encode())

# recebe pedido do primeiro número
cliente.recv(1024)
cliente.send(num1.encode())

# recebe pedido do segundo número
cliente.recv(1024)
cliente.send(num2.encode())

# recebe resultado final
resultado = cliente.recv(1024).decode()

t_fim = time.time()

print("Resultado recebido:", resultado)
print(f"Tempo total da operação: {t_fim - t_inicio:.6f} segundos\n")

cliente.close()
