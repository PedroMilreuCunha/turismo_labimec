# Pacotes necessários
import os
import time
from datetime import date
from ftplib import FTP


import py7zr
from tqdm import tqdm

# DECLARAÇÃO DE CONSTANTES
SERVER = "ftp.mtps.gov.br"
MESES = {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho",
         "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
MESES_INV = dict((v, k) for k, v in MESES.items())


# Funções
def obter_diretorios_caged() -> list:
    """

    :rtype  arquivos_disponiveis: list
    """
    ftp = FTP(SERVER)
    ftp.login()
    ano_corrente = date.today().year
    arquivos_disponiveis = []
    for ano in range(2020, ano_corrente + 1):
        ftp.cwd("/pdet/microdados/NOVO CAGED/" + str(ano))
        for arq in ftp.nlst():
            arquivos_disponiveis.append(arq)
            ftp.cwd("../")
    ftp.close()
    return arquivos_disponiveis


def criar_caminhos(opcao_escolhida: str) -> tuple:
    """

    :rtype c: str
    :type opcao_escolhida: str
    """
    diretorio = "pdet/microdados/NOVO CAGED/" + \
                opcao_escolhida[0:4] + "/" + opcao_escolhida
    nome_arquivo = "CAGEDMOV" + opcao_escolhida + ".7z"

    c = (diretorio, nome_arquivo)
    print(f"\nDiretório e nome do arquivo selecionado: \t{c}")
    return c


def baixar_arquivo(periodo_escolhido: str, diretorio_download: str, nome_arquivo: str, local_salvar: str) -> None:
    """

    :rtype: None
    :type periodo_escolhido: str
    :type diretorio_download: str
    :type nome_arquivo: str
    :type local_salvar: str
    """
    # Abertura do arquivo local
    arquivo_local = open(local_salvar + "/CAGEDMOV" +
                         periodo_escolhido + ".7z", "wb")
    # Conexão com o servidor FTP
    ftp = FTP(SERVER)
    ftp.login()
    ftp.cwd(diretorio_download)
    atual = [0, ]
    total = ftp.size(nome_arquivo)

    # Função de download modificada para gerar uma barra de progresso - baseado em https://www.cnblogs.com/frost-hit/p/6669227.html
    print(f"\nBaixando o arquivo {nome_arquivo}.\n")
    t0 = time.time()
    pbar = tqdm(total=total)

    def bar(dados: float) -> None:
        """

        :type dados: float
        """
        arquivo_local.write(dados)
        pbar.update(len(dados))

    try:
        ftp.retrbinary("RETR " + nome_arquivo,
                       bar, 1024)
        pbar.close()
        ftp.close()
        arquivo_local.close()
        print(f"\nARQUIVO TRANSFERIDO EM {round(time.time() - t0, 2)} SEGUNDOS.")
    except Exception as e:
        print(f"\nERRO DURANTE A TRANSFERÊNCIA: {e}. O arquivo corrompido será excluído.")
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".7z")
    print(f"\nIniciando extração e remoção do arquivo comprimido intermediário.")
    print(f"\nCaminho para salvar: {local_salvar}\\CAGEDMOV{periodo_escolhido}.txt")
    try:
        py7zr.SevenZipFile(local_salvar + "/CAGEDMOV" +
                           periodo_escolhido + ".7z", "r").extractall(local_salvar)
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".7z")
        print(f"\nARQUIVO FINAL .txt EXTRAÍDO COM SUCESSO.")
    except Exception as e:
        print(
            f"\nERRO DURANTE A EXTRAÇÃO DO ARQUIVO: {e}\nA versão em .7z foi mantida.")

