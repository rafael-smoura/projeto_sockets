from socket import AF_INET, SOCK_STREAM, socket
from datetime import datetime

# =============================================================
#  SERVIDOR DE NOMES — Modelo Estético (Simples e Elegante)
# =============================================================

serviços = {} # Armazena serviços no formato:
# servicos[(nome, protocolo)] = (ip, porta)

def log(msg):
    agora = datetime.now().strftime("%H:%M:%S")
    print(f"[{agora}] {msg}")


# =============================================================
#  INICIALIZAÇÃO DO SERVIDOR
# =============================================================
dns_socket = socket(AF_INET, SOCK_STREAM) # Socket TCP
dns_socket.bind(("0.0.0.0", 9000)) # Escuta em todas as portas
dns_socket.listen(5) # Tamanho da fila

log("🔎 Servidor de Nomes iniciado na porta 9000.")
log("Aguardando registros e consultas...\n")

# =============================================================
#  LOOP PRINCIPAL
# =============================================================

while True:
    # Aceita conexão
    socket_client, addr_client = dns_socket.accept() # Descapsulamento 
    log(f"📥 Conexão recebida de {addr_client}")   

    dados = socket_client.recv(1024).decode().strip() # Dados do cliente
    log(f"📨 Mensagem recebida: '{dados}'")

    partes = dados.split()
    comando = partes[0].upper()
    
    socket_client.send("Dados recebidos\n".encode())
    socket_client.close()




