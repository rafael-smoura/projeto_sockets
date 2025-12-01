# 📘 Projeto de Comunicação Cliente-Servidor com TCP, UDP e Servidor de Nomes

Este projeto implementa uma arquitetura completa de comunicação distribuída utilizando **sockets**, com foco na comparação entre os protocolos **TCP** e **UDP**, incluindo um **Servidor de Nomes** capaz de registrar, gerenciar e disponibilizar serviços automaticamente. O sistema segue rigorosamente o modelo solicitado em atividades acadêmicas avançadas da área de Redes de Computadores.

<img width="1475" height="398" alt="3" src="https://github.com/user-attachments/assets/0c36bbf2-c267-4b26-b012-d4240c6066d8" />

---

<img width="1456" height="512" alt="6" src="https://github.com/user-attachments/assets/6f2c382e-7450-49fc-aef1-c89757099b87" />

---

# 📂 Estrutura Geral do Projeto

```
Projeto-Sockets/
│
├── servidores/
│   ├── service_tcp.py
│   ├── service_udp.py
│   └── name_server.py
│
├── clientes/
│   ├── client_tcp.py
│   ├── client_udp.py
│   └── client_notfound.py
│
├── documentos/
│   ├── fluxograma.pdf
│   ├── relatorio.pdf
│   └── diagrama_uml.pdf
│
└── README.md
```

---

# 🎯 Objetivo do Projeto

Criar um ambiente completo de comunicação cliente-servidor com:

* 📡 **Servidor TCP** funcionando em porta dedicada
* 📡 **Servidor UDP** funcionando em porta dedicada
* 🧠 **Servidor de Nomes** que registra e responde serviços automaticamente
* 👤 **Clientes TCP e UDP automáticos**, sem uso de input
* ⚠️ **Cliente NotFound**, que solicita um serviço inexistente
* ⏱️ **Medição de tempo** de envio/retorno em ambos os protocolos
* 📊 **Captura única do Wireshark** contendo todas as interações

O serviço implementado é uma **Calculadora Remota**, que processa operações matemáticas básicas.

---

# 🧠 Descrição dos Componentes

## 🔵 Servidor de Nomes

* Porta padrão: **7777**
* Mantém um dicionário de serviços no formato:

  ```
  nome_do_servico → (ip, porta)
  ```
* Recebe mensagens com dois propósitos:

  1. **Registro automático de serviços** (linha com 3 argumentos)
  2. **Consulta de serviços** (linha com 1 argumento)
* Retorna:

  * IP e porta caso o serviço exista
  * `NOT_FOUND` caso contrário

---

## 🟩 Servidor TCP

* Porta: **6666**
* Implementa o serviço de calculadora remota com menus interativos
* Ao iniciar, se registra automaticamente no Servidor de Nomes
* Recebe requisições de um cliente TCP e responde confiavelmente

---

## 🟦 Servidor UDP

* Porta: **9999**
* Também registra seu serviço automaticamente
* Processa pacotes de modo não orientado a conexão
* Responde rapidamente com datagramas

---

## 🟧 Cliente TCP

* Consulta o Servidor de Nomes pelo serviço `calc_tcp`
* Recebe IP e porta
* Estabelece conexão TCP com o servidor
* Envia operação matemáticas automaticamente
* Recebe o resultado
* Calcula o tempo total de execução

---

## 🟪 Cliente UDP

* Consulta o Servidor de Nomes pelo serviço `calc_udp`
* Envia datagramas diretamente ao servidor UDP
* Recebe resposta com o resultado
* Registra o tempo total

---

## 🔴 Cliente NotFound

* Solicita um serviço inexistente
* Recebe `NOT_FOUND`
* Testa a robustez do Servidor de Nomes

---

# 🔄 Fluxo de Funcionamento Completo

## **1️⃣ Inicialização dos servidores**

* Servidor de Nomes inicializa e aguarda registros
* Servidor TCP inicia e se registra automaticamente
* Servidor UDP inicia e se registra automaticamente

## **2️⃣ Execução dos clientes**

* Cliente TCP consulta o Servidor de Nomes → conecta → opera → recebe resultado
* Cliente UDP consulta → envia datagramas → recebe resultado
* Cliente NotFound consulta → recebe `NOT_FOUND`

## **3️⃣ Medição de tempo**

* Cada cliente calcula o tempo total entre envio e recebimento

## **4️⃣ Captura da execução no Wireshark**

* Gerar uma única captura contendo TODOS os fluxos:

  * Registros de serviços
  * Consultas dos clientes
  * Tráfego TCP
  * Tráfego UDP

---

# 📝 Como Executar o Projeto

⚠️ **A ordem de execução é obrigatória**:

### 1️⃣ Iniciar o Servidor de Nomes

```
python servidores/name_server.py
```

### 2️⃣ Iniciar o Servidor TCP

```
python servidores/service_tcp.py
```

### 3️⃣ Iniciar o Servidor UDP

```
python servidores/service_udp.py
```

### 4️⃣ Executar os clientes (em qualquer ordem)

```
python clientes/client_tcp.py
python clientes/client_udp.py
python clientes/client_notfound.py
```
---

# 📐 Diagramas Incluídos ✅

O projeto inclui:

* UML de sequência completo

---

# 🏁 Conclusão

Este projeto demonstra:

* Diferenças práticas entre TCP e UDP
* Funcionamento de um sistema distribuído real
* Importância de um Servidor de Nomes
  automático
* Uso adequado de sockets
* Comparação de desempenho entre protocolos

A arquitetura criada segue rigor acadêmico e pode ser utilizada como base para aplicações de redes mais avançadas.

---

**Autor:** *Rafael Moura*

**Ano:** 2025


