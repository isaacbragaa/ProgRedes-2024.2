import socket
import os

DIRETORIO_BASE = "files/"
INTERFACE = '127.0.0.1'
PORTA = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((INTERFACE, PORTA))

print("Escutando em ...", (INTERFACE, PORTA))
while True:
    # recebe o nome do arquivo
    dados, origem = sock.recvfrom(512)
    nome_arquivo = dados.decode('utf-8')
    caminho_arquivo = DIRETORIO_BASE + nome_arquivo

    try:
        # verifica se o arquivo existe
        if not os.path.exists(caminho_arquivo):
            raise FileNotFoundError("Arquivo não encontrado.")

        print("Recebi pedido para o arquivo", nome_arquivo)

        # abre o arquivo e pega o tamanho
        tamanho_arquivo = os.path.getsize(caminho_arquivo)
        sock.sendto(str(tamanho_arquivo).encode('utf-8'), origem)  # envia o tamanho do arquivo

        # lê o conteúdo do arquivo 
        with open(caminho_arquivo, 'rb') as fd:
            print("Enviando arquivo", nome_arquivo)
            while True:
                dados_arquivo = fd.read(4096)
                if not dados_arquivo:
                    break
                sock.sendto(dados_arquivo, origem)
    except Exception as e:
        # tratamento de erro
        print(f"Erro: {e}")
        sock.sendto(b'ERROR', origem)

sock.close()