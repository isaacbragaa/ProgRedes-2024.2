import socket
import os

DIRETORIO_BASE = os.path.join(os.path.dirname(__file__), "files/")
INTERFACE = '127.0.0.1'
PORTA = 12345
TIMEOUT = 15  

# verificar se o arquivo existe
def arquivo_existe(caminho):
    try:
        with open(caminho, 'rb'):
            return True
    except FileNotFoundError:
        return False

# obtem o tamanho do arquivo
def tamanho_arquivo(caminho):
    tamanho = 0
    try:
        with open(caminho, 'rb') as f:
            while f.read(1):
                tamanho += 1
    except FileNotFoundError:
        tamanho = -1
    return tamanho

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((INTERFACE, PORTA))
sock.settimeout(TIMEOUT)

print("Escutando em ...", (INTERFACE, PORTA))

while True:
    try:
        # recebe o nome do arquivo
        dados, origem = sock.recvfrom(512)
        nome_arquivo = dados.decode('utf-8').strip()
        caminho_arquivo = os.path.join(DIRETORIO_BASE, nome_arquivo)

        try:
            # verifica se o arquivo existe
            if not arquivo_existe(caminho_arquivo):
                raise FileNotFoundError("Arquivo não encontrado.")

            print(f"Recebido pedido para {nome_arquivo}. Caminho completo: {caminho_arquivo}")

            # pega o tamanho do arquivo
            tamanho = tamanho_arquivo(caminho_arquivo)
            if tamanho < 0:
                raise FileNotFoundError("Erro ao calcular o tamanho do arquivo.")

            sock.sendto(str(tamanho).encode('utf-8'), origem)  # Envia o tamanho do arquivo

            # lê o conteúdo do arquivo e envia em partes
            with open(caminho_arquivo, 'rb') as fd:
                print("Enviando arquivo", nome_arquivo)
                while True:
                    dados_arquivo = fd.read(4096)
                    if not dados_arquivo:
                        break
                    sock.sendto(dados_arquivo, origem)

        except Exception as e:
            print(f"Erro: {e}")
            sock.sendto(b'ERROR', origem)
    except socket.timeout:
        print("Tempo limite atingido para comunicação. Recomeçando...")
    except Exception as e:
        print(f"Erro inesperado: {e}")