# Pacotes necessários
import os
from datetime import date
from ftplib import FTP

import py7zr
from tqdm.rich import tqdm
from colored import stylize, fg, attr
import warnings
warnings.filterwarnings("ignore")

# DECLARAÇÃO DE CONSTANTES
SERVER = "ftp.mtps.gov.br"
MESES = {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho",
         "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
MESES_INV = dict((v, k) for k, v in MESES.items())

# Funções


def obter_diretorios_caged() -> list:
    """
    Função utilizada para mostrar os arquivos disponíveis no servidor FTP
    do Ministério do Trabalho do NOVO CAGED.

    Retorna uma lista de strings com os nomes dos arquivos disponíveis.

    :rtype arquivos_disponiveis: list
    """
    ftp = FTP(SERVER)
    ftp.login()
    ano_corrente = date.today().year
    arquivos_disponiveis = []
    for ano in range(2020, ano_corrente+1):
        ftp.cwd("/pdet/microdados/NOVO CAGED/" + str(ano))
        for arq in ftp.nlst():
            arquivos_disponiveis.append(arq)
            ftp.cwd("../")
    ftp.close()
    return arquivos_disponiveis


def criar_caminhos(opcao_escolhida: str) -> tuple:
    """
    Função utilizada para criar os caminhos para o arquivo escolhido pelo
    usuário e o diretório que o contém. Utiliza como parâmetro a opção
    escolhida pelo usuário, representada pela opcao_escolhida.

    Retorna uma tupla contendo o caminho para o arquivo e o diretório em que
    ele se encontra.

    :rtype c: tuple
    :param opcao_escolhida: str
    """
    diretorio = "pdet/microdados/NOVO CAGED/" + \
                opcao_escolhida[0:4] + "/" + opcao_escolhida
    nome_arquivo = "CAGEDMOV" + opcao_escolhida + ".7z"

    c = (diretorio, nome_arquivo)
    print(f"Diretório e nome do arquivo selecionado: \t{c}\n")
    return c


def baixar_arquivo(periodo_escolhido: str, diretorio_download: str, nome_arquivo: str, local_salvar: str) -> None:
    """
    Função utilizada para baixar o arquivo escolhido pelo usuário. Utiliza como
    parâmetros strings representando o período escolhido (periodo_escolhido),
    o diretório de download (diretorio_download), o nome do arquivo (nome_arquivo)
    e o caminho do local para salvar o arquivo transferido (local_salvar).

    A função não retorna nada, agindo apenas como intermediária para
    transferir o arquivo.

    :rtype: None
    :param periodo_escolhido: str
    :param diretorio_download: str
    :param nome_arquivo: str
    :param local_salvar: str
    """
    # Abertura do arquivo local
    arquivo_local = open(local_salvar + "/CAGEDMOV" +
                         periodo_escolhido + ".7z", "wb")
    # Conexão com o servidor FTP
    ftp = FTP(SERVER)
    ftp.login()
    ftp.cwd(diretorio_download)
    total = ftp.size(nome_arquivo)

    print(stylize("Baixando o arquivo " + nome_arquivo, attr("bold")))
    pbar = tqdm(total=total, desc="",
                dynamic_ncols=True, position=0,
                unit='B', unit_scale=True, unit_divisor=1000)  # Criação da barra

    def bar(dados: bytes) -> None:
        """
        Função utilizada para mostrar uma barra de progresso em tempo real
        durante a transferência via FTP. O parâmetro dados representa o fluxo
        de dados durante o download.
        Utilizando a variável global n controlamos a frequência com que o
        progresso é mostrado no terminal, evitando que ele fique visualmente
        poluído. Em particular, só há atualização a cada 70 execuções da
        função (n % 70 == 0).

        :param dados: bytes
        """
        arquivo_local.write(dados)
        global n
        n += 1
        pbar.update(len(dados))
        if n % 70 == 0:
            print(stylize(pbar, fg("light_blue")), flush=True)

    try:
        ftp.retrbinary("RETR " + nome_arquivo,
                       bar, 81920)
        pbar.close()
        ftp.close()
        arquivo_local.close()
    except Exception as e:
        print(stylize("ERRO DURANTE A TRANSFERÊNCIA: " + str(e) + ". O arquivo corrompido será excluído.",
                      fg("red") + attr("bold")))
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".7z")
    print(f"\nIniciando extração e remoção do arquivo comprimido intermediário.")
    print(f"\nCaminho para salvar: {local_salvar}\\CAGEDMOV{periodo_escolhido}.txt\n")
    try:
        py7zr.SevenZipFile(local_salvar + "/CAGEDMOV" +
                           periodo_escolhido + ".7z", "r").extractall(local_salvar)
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".7z")
        print(stylize("Arquivo final .txt extraído com sucesso.", fg("green") + attr("bold")))
    except Exception as e:
        print(
            stylize("ERRO DURANTE A EXTRAÇÃO DO ARQUIVO: " + str(e) + ". A versão em .7z foi mantida.",
                    fg("red") + attr("bold")))


n = 0  # Variável contadora
