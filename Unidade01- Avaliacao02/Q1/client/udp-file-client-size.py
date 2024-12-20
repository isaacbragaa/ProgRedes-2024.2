import socket

DIRETORIO_BASE = "files/"
SERVIDOR = '127.0.0.1'
PORTA = 12345
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

while True:
    # lê do usuário o nome do arquivo a pedir ao servidor
    nome_arquivo = input("Arquivo a pedir ao servidor: ")

    # envia ao servidor o nome do arquivo desejado pelo usuário
    print("Enviando pedido a", (SERVIDOR, PORTA), "para", nome_arquivo)
    sock.sendto(nome_arquivo.encode('utf-8'), (SERVIDOR, PORTA))

    try:
        # recebe o tamanho do arquivo
        dados_tamanho_arquivo, origem = sock.recvfrom(512)
        tamanho_arquivo = int(dados_tamanho_arquivo.decode('utf-8'))

        if tamanho_arquivo == 0:
            print("Erro: o arquivo está vazio ou não foi encontrado.")
            continue

        # grava o arquivo
        print("\nGravando arquivo")
        tamanho_recebido = 0
        with open(DIRETORIO_BASE + nome_arquivo, 'wb') as fd:
            while tamanho_recebido < tamanho_arquivo:
                dados, _ = sock.recvfrom(4096)
                if not dados:
                    break
                fd.write(dados)
                tamanho_recebido += len(dados)

        print("Arquivo recebido com sucesso!")
    except Exception as e:
        print(f"Erro: {e}")

sock.close()
