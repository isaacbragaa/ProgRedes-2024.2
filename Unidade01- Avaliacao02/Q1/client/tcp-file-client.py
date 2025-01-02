import socket
import os

DIRETORIO_BASE = os.path.join(os.path.dirname(__file__), "files/")
SERVIDOR = '127.0.0.1'
PORTA = 12345
TIMEOUT = 15  

# criar diretório
if not os.path.isdir(DIRETORIO_BASE):
    try:
        os.makedirs(DIRETORIO_BASE)
    except Exception as e:
        print(f"Erro ao criar diretório: {e}")
        exit(1)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(TIMEOUT)

while True:
    # lê do usuário o nome do arquivo a pedir ao servidor
    nome_arquivo = input("Arquivo a pedir ao servidor (ou 'sair' para encerrar): ").strip()

    if nome_arquivo.lower() == 'sair':
        print("Encerrando cliente...")
        break

    # envia ao servidor o nome do arquivo desejado pelo usuário
    print("Enviando pedido a", (SERVIDOR, PORTA), "para", nome_arquivo)
    sock.sendto(nome_arquivo.encode('utf-8'), (SERVIDOR, PORTA))

    try:
        # recebe o tamanho do arquivo ou mensagem de erro
        dados_tamanho_arquivo, origem = sock.recvfrom(512)
        mensagem = dados_tamanho_arquivo.decode('utf-8')

        if mensagem == 'ERROR':
            print("Erro recebido do servidor: Arquivo não encontrado ou problema interno.")
            continue

        # caso não seja erro, tenta converter para número
        try:
            tamanho_arquivo = int(mensagem)
        except ValueError:
            print("Erro: resposta inválida do servidor.")
            continue

        if tamanho_arquivo <= 0:
            print("Erro: o arquivo está vazio ou não foi encontrado.")
            continue

        # grava o arquivo
        print("\nGravando arquivo")
        tamanho_recebido = 0
        caminho_arquivo = os.path.join(DIRETORIO_BASE, nome_arquivo)

        with open(caminho_arquivo, 'wb') as fd:
            while tamanho_recebido < tamanho_arquivo:
                dados, _ = sock.recvfrom(4096)
                if not dados:
                    break
                fd.write(dados)
                tamanho_recebido += len(dados)

        print("Arquivo recebido com sucesso em", caminho_arquivo)
    except socket.timeout:
        print("Tempo limite atingido ao tentar se comunicar com o servidor.")
    except Exception as e:
        print(f"Erro: {e}")

sock.close()
