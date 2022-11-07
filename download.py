# Pacotes necessários
from ftplib import FTP
from datetime import date
import os

import py7zr
import time

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

def baixar_arquivo(periodo_escolhido: str, diretorio_download: str , nome_arquivo: str, local_salvar: str,
                   progresso: float, n: float, tamanho: float) -> None:
    """

    :rtype: None
    :type periodo_escolhido: str
    :type diretorio_download: str
    :type nome_arquivo: str
    :type local_salvar: str
    :type progresso: float
    :type n: float
    :type tamanho: float
    """
    # Abertura do arquivo local
    arquivo_local = open(local_salvar + "/CAGEDMOV" +
                         periodo_escolhido + ".7z", "wb")
    # Conexão com o servidor FTP
    ftp = FTP(SERVER)
    ftp.login()
    ftp.cwd(diretorio_download)
    print(f"\nBaixando o arquivo {nome_arquivo}.\n")
    t0 = time.time()
    try:
        ftp.retrbinary("RETR " + nome_arquivo,
                       arquivo_local.write)
        print(f"\nARQUIVO TRANSFERIDO EM {round(time.time() - t0, 2)} SEGUNDOS.")
        ftp.close()
        arquivo_local.close()
    except Exception as e:
        print(f"\nERRO DURANTE A TRANSFERÊNCIA: {e}")
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

def escrever_arquivo(dados):
    """
    Função de escrita em arquivo local alterada para mostrar o progresso da transferência dos arquivos via FTP
    """
    global arquivo_local
    global progresso
    global n
    global tamanho
    arquivo_local.write(dados)
    progresso += len(dados)
    n += 1
    t = 100 * progresso / tamanho
    if n % 200 == 0:
        print(f"{t:.2f}%,")