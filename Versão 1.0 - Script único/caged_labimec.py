# Pacotes necessários
# !pip install openpyxl
from ftplib import FTP
import os
from datetime import date
import pandas as pd
import numpy as np
import py7zr
import matplotlib.pyplot as plt
import seaborn as sns
from gooey import Gooey, GooeyParser

# DECLARAÇÃO DE CONSTANTES

# ---------------------Parte da extração dos dados---------------------
SERVER = "ftp.mtps.gov.br"
MESES = {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho",
         "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
MESES_INV = dict((v, k) for k, v in MESES.items())

# ---------------------Parte do tratamento dos dados referentes ao turismo---------------------
SUBCLASSES_TURISMO = pd.DataFrame(data={"Subclasse":
                                        (5510801, 5510802, 5510803,  # Hóteis e similares
                                         5590601, 5590602, 5590603, 5590699,  # Outros tipos de alojamento
                                         5611201, 5611202, 5611203,  # Restaurantes
                                         5612100,  # Serviços ambulantes de alimentação
                                         4923001, 4923002,  # Transporte rodoviário de táxi
                                         4929901, 4929903, 4929999,  # Transporte rodoviário coletivo
                                         4950700,  # Trens turísticos
                                         # Transporte rodoviário coletivo (trens)
                                         4922101, 4922102, 4922103,
                                         # Transporte rodoviário coletivo (fretamento) e n.e.a.
                                         4929902, 4929904,
                                         5011402, 5012202, 5022001, 5022002, 5091201, 5091202, 5099801, 5099899,
                                         # Transporte aquaviário
                                         5111100, 5112901, 5112999,  # Transporte aéreo
                                         7111000,  # Aluguel de transporte
                                         7911200, 7912100,  # Agências de viagem
                                         # Serviços de reserva e n.e.a.
                                         7990200,
                                         9001901, 9001902, 9001903, 9001904, 9001905, 9001999,  # Artês cênicas
                                         9102301,  # Atividades de museus
                                         9200301, 9200302, 9200399,
                                         # Atividade de exploração de jogos de azar e apostas
                                         # Atividades esportivas n.e.a.
                                         9319101, 9319199,
                                         9321200,  # Parques de diversão e parques temáticos
                                         9329801, 9329802, 9329803, 9329804,
                                         9329899)})  # Atividades de recreação e lazer n.e.a

ALOJAMENTO = (5510801, 5510802, 5510803,
              5590601, 5590602, 5590603, 5590699)

ALIMENTACAO = (5611201, 5611202, 5611203,
               5612100)

TRANSPORTE_TERRESTRE = (4923001, 4923002,
                        4929901, 4929903, 4929999,
                        4950700,
                        4922101, 4922102, 4922103,
                        4929902, 4929904)

TRANSPORTE_AQUAVIARIO = (5011402, 5012202, 5022001,
                         5022002, 5091201, 5091202, 5099801, 5099899)

TRANSPORTE_AEREO = (5111100, 5112901, 5112999)

ALUGUEL_TRANSPORTE = 7111000

AGENCIAS_VIAGEM = (7911200, 7912100, 7990200)

CULTURA = (9001901, 9001902, 9001903, 9001904, 9001905, 9001999,
           9102301)

LAZER = (9200301, 9200302, 9200399,
         9319101, 9319199,
         9321200,
         9329801, 9329802, 9329803, 9329804, 9329899)

# ---------------------Parte gráfica-----------------------------------

sns.set(style="white")
plt.rcParams["figure.dpi"] = 400
plt.rcParams["figure.figsize"] = [10, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["DejaVu Sans"]


# Funções

# ---------------------Parte da extração dos dados---------------------


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
    print(f"\nIniciando o download do arquivo {nome_arquivo}.\n")
    ftp = FTP(SERVER)
    ftp.login()
    ftp.cwd(diretorio_download)
    try:
        ftp.retrbinary("RETR " + nome_arquivo,
                       escrever_arquivo)
        print(f"\n\nARQUIVO TRANSFERIDO")
        ftp.close()
        arquivo_local.close()
    except Exception as e:
        print(f"\nERRO DURANTE A TRANSFERÊNCIA: {e}")

    print(f"\nIniciando extração e remoção do arquivo comprimido intermediário.")
    print(
        f"\nCaminho para salvar: {local_salvar}\\CAGEDMOV{periodo_escolhido}.txt")
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
    arquivo_local.write(dados)
    global progresso
    global n
    global tamanho
    progresso += len(dados)
    n += 1
    t = 100 * progresso / tamanho
    if n % 200 == 0:
        print(f"{t:.2f}%,")


# ---------------------Parte da transformação dos dados---------------------


def criar_df_categorias() -> pd.DataFrame:
    """

    :rtype df_categorias_turismo: pd.DataFrame
    """
    condicoes = [SUBCLASSES_TURISMO.isin(ALOJAMENTO),
                 SUBCLASSES_TURISMO.isin(ALIMENTACAO),
                 SUBCLASSES_TURISMO.isin(TRANSPORTE_TERRESTRE),
                 SUBCLASSES_TURISMO.isin(TRANSPORTE_AQUAVIARIO),
                 SUBCLASSES_TURISMO.isin(TRANSPORTE_AEREO),
                 SUBCLASSES_TURISMO == ALUGUEL_TRANSPORTE,
                 SUBCLASSES_TURISMO.isin(AGENCIAS_VIAGEM),
                 SUBCLASSES_TURISMO.isin(CULTURA),
                 SUBCLASSES_TURISMO.isin(LAZER)]
    valores = ["Alojamento",
               "Serviços de Alimentação",
               "Transporte Terrestre",
               "Transporte Aquaviário",
               "Transporte Aéreo",
               "Aluguel de Automóveis",
               "Agências e Operadoras",
               "Atividades Culturais",
               "Atividades Desportivas e Recreativas"]
    df_categorias_turismo = pd.DataFrame.copy(SUBCLASSES_TURISMO)
    df_categorias_turismo["Categoria"] = np.select(condicoes, valores)
    return df_categorias_turismo


def importar_caged(nome_arquivo: str, df_categorias_turismo: pd.DataFrame, turismo: bool) -> pd.DataFrame:
    """

    :rtype df_caged: pd.DataFrame
    :type nome_arquivo: str
    :type df_categorias_turismo: pd.DataFrame
    :type turismo: bool
    """
    dados_caged = pd.DataFrame()
    if turismo:
        print(
            f"\nImportando os dados da CAGED e criando o pd.DataFrame apenas com os dados referentes"
            f" ao turismo em João Pessoa")
        try:
            dados_caged_turismo_jp = pd.read_table(
                nome_arquivo, decimal=",", sep=";")
            dados_caged_turismo_jp = dados_caged_turismo_jp[dados_caged_turismo_jp["município"] == 250750]
            dados_caged_turismo_jp = df_categorias_turismo.merge(dados_caged_turismo_jp, how="left",
                                                                 left_on="Subclasse",
                                                                 right_on="subclasse").reset_index()
            dados_caged = dados_caged_turismo_jp
        except Exception as e:
            print(f"Erro durante a importação do arquivo {nome_arquivo}: {e}")
    else:
        print(f"\nImportando os dados da CAGED e criando o pd.DataFrame com os dados")
        try:
            dados_caged = pd.read_table(nome_arquivo, decimal=",", sep=";")
        except Exception as e:
            print(f"Erro durante a importação do arquivo {nome_arquivo}: {e}")

    return dados_caged


def recodificar_dummies(dados_caged: pd.DataFrame, turismo: bool) -> pd.DataFrame:
    """

    :rtype df_recodificado: pd.DataFrame
    :type dados_caged: pd.DataFrame
    :type turismo: bool
    """
    print(f"\nRecodificando as variáveis dummies de escolaridade, raça/cor e sexo")
    df_recodificado = pd.DataFrame.copy(dados_caged)

    df_recodificado["graudeinstrução"] = np.where(df_recodificado["graudeinstrução"].values == 99, "Não identificado",
                                                  np.where(df_recodificado["graudeinstrução"].isin(range(1, 5)),
                                                           "Ensino fundamental incompleto",
                                                           np.where(
                                                               df_recodificado["graudeinstrução"].isin(
                                                                   range(5, 7)),
                                                               "Ensino médio incompleto",
                                                               np.where(df_recodificado["graudeinstrução"].values <= 8,
                                                                        "Ensino médio completo",
                                                                        "Ensino superior completo"))))
    df_recodificado["raçacor"] = np.where(df_recodificado["raçacor"].isin([6, 9]), "Não informado/identificado",
                                          np.where(df_recodificado["raçacor"].isin([2, 3]), "Preto ou parda",
                                                   "Outros"))
    df_recodificado["sexo"] = np.where(df_recodificado["sexo"].values == 9, "Não identificado",
                                       np.where(df_recodificado["sexo"].values == 1, "Homem",
                                                "Mulher"))
    df_recodificado["tipomovimentação"] = np.where(df_recodificado["saldomovimentação"].values == 1, "Admissão",
                                                   "Desligamento")
    if turismo:
        df_recodificado = df_recodificado.astype({"Categoria": "category", "graudeinstrução": "category",
                                                  "raçacor": "category", "sexo": "category",
                                                  "tipomovimentação": "category"})
    else:
        df_recodificado = df_recodificado.astype({"município": "category", "graudeinstrução": "category",
                                                  "raçacor": "category", "sexo": "category",
                                                  "tipomovimentação": "category"})
    return df_recodificado


def agregar_resultados(df_recodificado: pd.DataFrame, turismo: bool) -> pd.DataFrame:
    """

    :rtype df_agregado: pd.DataFrame
    :type df_recodificado: pd.DataFrame
    :type turismo: bool
    """
    if turismo:
        print(f"\nAgrupando os dados por categoria do turismo, tipo de movimentação, escolaridade, raça/cor e sexo")
        dados_agrupados = (
            df_recodificado
            .groupby(["Categoria", "tipomovimentação", "graudeinstrução", "raçacor", "sexo"], dropna=False)
            .agg(**{
                "Salário médio (R$)": ("salário", "mean"),
                "Saldo de movimentações": ("saldomovimentação", "sum"),
                "Idade média": ("idade", "mean")
            })
            .reset_index()
        )
    else:
        print(f"\nAgrupando os dados por município, tipo de movimentação, escolaridade, raça/cor e sexo")
        dados_agrupados = (
            df_recodificado
            .groupby(["município", "tipomovimentação", "graudeinstrução", "raçacor", "sexo"], dropna=False)
            .agg(**{
                "Salário médio (R$)": ("salário", "mean"),
                "Saldo de movimentações": ("saldomovimentação", "sum"),
                "Idade média": ("idade", "mean")
            })
            .reset_index()
        )
    return dados_agrupados


def lidar_na(df_agregado: pd.DataFrame, turismo: bool) -> pd.DataFrame:
    """

    :rtype df_agregado_final: pd.DataFrame
    :type df_agregado: pd.DataFrame
    :type turismo: bool
    """
    print(f"\nLidando com os dados ausentes")
    df_agregado_final = pd.DataFrame.copy(df_agregado)

    df_agregado_final["Salário médio (R$)"] = np.where(df_agregado_final["Salário médio (R$)"].isna(), float("NaN"),
                                                       df_agregado_final["Salário médio (R$)"])
    df_agregado_final["Saldo de movimentações"] = np.where(df_agregado_final["Saldo de movimentações"].isna(),
                                                           float("NaN"),
                                                           df_agregado_final["Saldo de movimentações"])
    df_agregado_final["Idade média"] = np.where(df_agregado_final["Idade média"].isna(), float("NaN"),
                                                df_agregado_final["Idade média"])
    df_agregado_final["graudeinstrução"] = np.where(df_agregado_final["graudeinstrução"].isna(), "Dado ausente",
                                                    df_agregado_final["graudeinstrução"])
    df_agregado_final["raçacor"] = np.where(df_agregado_final["raçacor"].isna(), "Dado ausente",
                                            df_agregado_final["raçacor"])
    df_agregado_final["sexo"] = np.where(
        df_agregado_final["sexo"].isna(), "Dado ausente", df_agregado_final["sexo"])

    df_agregado_final["Data"] = periodo_escolhido

    if turismo:
        df_agregado_final.rename(columns={"graudeinstrução": "Escolaridade", "tipomovimentação": "Movimentação",
                                          "raçacor": "Raça/Cor",
                                          "sexo": "Sexo", "salario_faltante": "Salário ausente",
                                          "movimentaçao_faltante": "Movimentação faltante"}, inplace=True)
    else:
        df_agregado_final.rename(columns={"município": "Cód. Município", "tipomovimentação": "Movimentação",
                                          "graudeinstrução": "Escolaridade", "raçacor": "Raça/Cor",
                                          "sexo": "Sexo"}, inplace=True)
    return df_agregado_final


# ---------------------Parte da plotagem dos gráficos---------------------


def plotar_resultados(dados: pd.DataFrame, local: str) -> None:
    """

    :type dados: pd.DataFrame
    :type local: str
    """
    for m in ("Admissão", "Desligamento"):
        if not os.path.isdir(local + "/" + periodo_escolhido + " - " + m):
            os.mkdir(local + "/" + periodo_escolhido + " - " + m)
        print(f"\nGráficos de: {m}")
        temp = dados.query("`Movimentação` == @m").reset_index()
        temp["Saldo de movimentações"] = abs(temp["Saldo de movimentações"])
        print("\n(1/14) Salário médio por categoria")
        try:
            t = temp.groupby("Categoria").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                 "Saldo de movimentações": (
                                                     "Saldo de movimentações", "sum")}).reset_index()
            g1 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette="viridis", kind='bar',
                             aspect=1.4)
            ax = g1.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            plt.xlabel("Salário médio (R$)", size=14)
            plt.xlim((0, 2300))
            plt.tick_params(axis="both", which="major", labelsize=14)
            g1.set(ylabel=None)
            sns.despine()

            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_categoria" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (1/14): {e}")

        print("\n(2/14) Salário médio por escolaridade")
        try:
            t = temp.groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                    "Saldo de movimentações": (
                                                        "Saldo de movimentações", "sum")}).reset_index()

            g2 = sns.catplot(data=t, x="Salário médio (R$)", y="Escolaridade", palette="viridis", kind='bar',
                             aspect=1.4)
            ax = g2.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g2.set(ylabel=None)
            sns.despine()

            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_escolaridade" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (2/14): {e}")

        print("\n(3/14) Salário médio por sexo")
        try:
            t = temp.groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                            "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()

            g3 = sns.catplot(data=t, x="Salário médio (R$)", y="Sexo",
                             palette="viridis", kind='bar', aspect=1.4)
            ax = g3.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g3.set(ylabel=None)
            sns.despine()
            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_sexo" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (3/14): {e}")

        print("\n(4/14) Salário médio por raça/cor")
        try:
            t = (
                temp.groupby("Raça/Cor")
                .agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                        "Saldo de movimentações": ("Saldo de movimentações", "sum")})
                .reset_index()
            )
            g4 = sns.catplot(data=t, x="Salário médio (R$)", y="Raça/Cor", palette="viridis", kind='bar',
                             aspect=1.4)
            ax = g4.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g4.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (4/14): {e}")

        print("\n(5/14) Salário médio por categoria, escolaridade e sexo")
        try:
            t = temp.groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g5 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette="viridis",
                                 col="Sexo", row="Escolaridade", kind="bar", errorbar=None, aspect=1.4,
                                 margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g5.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g5.set(ylabel=None)
                sns.despine()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_categoria_escolaridade_sexo" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (5/14): {e}")

        print("\n(6/14) Salário médio por categoria, escolaridade e raça/cor")
        try:
            t = temp.groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g6 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette="viridis",
                                 col="Escolaridade", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4,
                                 margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g6.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g6.set(ylabel=None)
                sns.despine()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_categoria_escolaridade_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (6/14): {e}")

        print("\n(7/14) Salário médio por categoria, sexo e raça/cor")
        try:
            t = temp.groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g7 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette="viridis",
                                 col="Sexo", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4, margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g7.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g7.set(ylabel=None)
                sns.despine()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/salario_medio_por_categoria_sexo_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (7/14): {e}")

        print("\n(8/14) Saldo de movimentações por categoria")
        try:
            t = temp.groupby("Categoria").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                 "Saldo de movimentações": (
                                                     "Saldo de movimentações", "sum")}).reset_index()
            g8 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette="viridis", kind='bar',
                             aspect=1.4)
            ax = g8.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            plt.xlabel("Saldo de movimentações", size=12)
            plt.tick_params(axis="both", which="major", labelsize=12)
            g8.set(ylabel=None)
            sns.despine()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_categoria" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (8/14): {e}")

        print("\n(9/14) Saldo de movimentações por escolaridade")
        try:
            t = temp.groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                    "Saldo de movimentações": (
                                                        "Saldo de movimentações", "sum")}).reset_index()
            g9 = sns.catplot(data=t, x="Saldo de movimentações", y="Escolaridade", palette="viridis", kind='bar',
                             aspect=1.4)
            ax = g9.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g9.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.margins(x=0.2)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_escolaridade" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (9/14): {e}")

        print("\n(10/14) Saldo de movimentações por sexo")
        try:
            t = temp.groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                            "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            g10 = sns.catplot(data=t, x="Saldo de movimentações", y="Sexo", palette="viridis", kind='bar',
                              aspect=1.4)
            ax = g10.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g10.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.margins(x=0.2)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_sexo" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (10/14): {e}")

        print("\n(11/14) Saldo de movimentações por raça/cor")
        try:
            t = temp.groupby("Raça/Cor").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                "Saldo de movimentações": (
                                                    "Saldo de movimentações", "sum")}).reset_index()
            g11 = sns.catplot(data=t, x="Saldo de movimentações", y="Raça/Cor", palette="viridis", kind='bar',
                              aspect=1.4)
            ax = g11.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g11.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Saldo de movimentações", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (11/14): {e}")

        print("\n(12/14) Saldo de movimentações por categoria, escolaridade e sexo")
        try:
            t = temp.groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g12 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette="viridis",
                                  col="Sexo", row="Escolaridade", kind="bar", errorbar=None, aspect=1.4,
                                  margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g12.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g12.set(ylabel=None)
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_categoria_escolaridade_sexo" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (12/14): {e}")

        print("\n(13/14) Saldo de movimentações por categoria, escolaridade e raça/cor")
        try:
            t = temp.groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g13 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette="viridis",
                                  col="Escolaridade", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4,
                                  margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g13.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g13.set(ylabel=None)
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_categoria_escolaridade_raca" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (13/14): {e}")

        print("\n(14/14) Saldo de movimentações por categoria, sexo e raça/cor")
        try:
            t = temp.groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g14 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette="viridis",
                                  col="Sexo", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4, margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g14.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g14.set(ylabel=None)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m + "/saldo_movimentacoes_por_categoria_sexo_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (14/14): {e}")
        print(
            f"\n\nFIGURAS EXPORTADAS COM SUCESSO PARA A PASTA {local}/{periodo_escolhido} - {m}")


# LOOP PRINCIPAL DO PROGRAMA


@Gooey(dump_build_config=False, richtext_controls=True, clear_before_run=True,
       program_name="Utilitário para extração, leitura e tratamento de"
                    " microdados do NOVO CAGED sobre turismo - LABIMEC",
       language="portuguese", default_size=(1024, 800), image_dir="figs", language_dir="lang",
       show_restart_button=False,
       timing_options={
           "show_time_remaining": True,
           "hide_time_remaining_on_complete": True},
       menu=[{
           "name": "Informações",
           "items": [{
               "type": "AboutDialog",
               "menuTitle": "Sobre",
               "name": "Utilitário para extração, leitura e tratamento de"
                       " microdados do NOVO CAGED sobre turismo - LABIMEC",
               "description": "Um programa simples que serve para baixar, extrair"
                              " e analisar os microdados do NOVO CAGED (2020 em diante)"
                              " utilizando conexões FTP e o módulo Gooey para desenvolver a GUI.",
               "version": "1.0",
               "copyright": "2022",
               "website": "https://www.ufpb.br/labimec\nhttps://github.com/PedroMilreuCunha",
               "developer": "Pedro Milreu Cunha - Doutorando e Mestre em Economia"
                            " Aplicada pelo PPGE/UFPB e \nBacharel em Ciências Econômicas pela UFV"
                            "",
               "license": "Gratuito para uso pessoal."
           }, {
               "type": "MessageDialog",
               "menuTitle": "Contato",
               "caption": "Feedback",
               "message": "Para quaisquer dúvidas, sugestões, críticas"
                          " ou elogios entrar em contato com o desenvolvedor através do e-mail pcunha.2107@gmail.com."
           }]
       }])
def loop_programa():  # Função principal para obter e extrair os argumentos das entradas dos usuários
    # Descrição geral do programa
    desc = "Programa utilizado para baixar, extrair e analisar" \
           " (em relação ao turismo) os microdados do NOVO CAGED" \
           "\ndisponíveis no servidor FTP do Ministério do Trabalho."
    parser = GooeyParser(description=desc)

    # Configuração da parte de transferência e extração dos dados do NOVO CAGED
    extracao = parser.add_argument_group(
        "Download e extração dos dados",
        description="Utilize esses campos para escolher o arquivo desejado"
                    " do servidor FTP e a pasta onde deseja salvá-lo.",
        gooey_options={"show_border": True}
    )

    # Mensagens de ajuda
    msg_arquivos = "Os microdados do NOVO CAGED disponíveis até a data atual" \
                   " podem ser vistos e escolhidos utilizando a caixa de seleção."
    msg_salvar = "Utilize esse campo para selecionar a pasta de gravação" \
                 " do arquivo final com os microdados extraídos em .txt."

    # Obtenção dos arquivos disponíveis do servidor FTP
    arquivos_disponiveis = obter_diretorios_caged()
    visualizacao_arquivos_disponiveis = []
    for i in arquivos_disponiveis:
        mes = i[-2:]
        ano = i[0:4]
        visualizacao_arquivos_disponiveis.append(MESES[mes] + "-" + ano)

    # Criação dos campos para entrada — parte da extração dos dados
    extracao.add_argument(
        "Escolher", help=msg_arquivos, widget="FilterableDropdown", choices=visualizacao_arquivos_disponiveis,
        gooey_options={
            "placeholder": "Comece a escrever o nome do mês que deseja (Janeiro, por exemplo)."}
    )
    extracao.add_argument(
        "Salvar", help=msg_salvar, widget="DirChooser", action="store", type=str,
        gooey_options={
            "placeholder": "Escolha um diretório para salvar o arquivo final em .xlsx."}
    )

    # ---------------------Configuração da parte de transformção dos microdados do NOVO CAGED---------------------
    transformacao = parser.add_argument_group(
        "Transformação dos dados",
        description="Utilize essa seção para marcar se deseja realizar uma limpeza e agregação dos dados e, também,"
                    "se deve ser feita uma análise especificamente para o setor de turismo de João Pessoa.",
        gooey_options={"show_border": True}
    )
    # Mensagens de ajuda
    msg_transformar = "Marque essa opção caso deseje que os dados sejam" \
                      " trabalhados, organizados e agregados por escolaridade," \
                      "município, raça/cor e sexo."
    msg_turismo_jp = "Marque essa opção caso deseje que os dados trabalhados" \
                     " façam referência apenas às categoria do turismo e ao município de João Pessoa."

    # Criação do campo para entrada — parte do tratamento dos dados
    transformacao.add_argument(
        "--Transformar", help=msg_transformar, widget="BlockCheckbox", action="store_true"
    )
    # Criação do campo para entrada — parte do tratamento em relação ao turismo e João Pessoa
    transformacao.add_argument(
        "--Turismo", help=msg_turismo_jp, widget="BlockCheckbox", action="store_true"
    )

    # ---------------------Configuração da parte de visualização de sínteses dos resultados---------------------
    plotagem = parser.add_argument_group(
        "Visualização dos dados",
        description="\t\t\t\tIMPORTANTE: DISPONÍVEL APENAS PARA OS DADOS DO TURISMO DE JOÃO PESSOA\n\n"
                    "Utilize essa seção para escolher se os gráficos-síntese dos resultados devem ser elaborados"
                    " e exportados.",
        gooey_options={"show_border": True}
    )

    # Mensagem de ajuda
    msg_plotar = "Marque essa opção caso deseje que gráficos sintetizando os resultados (turismo) sejam criados."
    msg_exportar = "Selecione a pasta onde deseja salvar as visualizações gráficas dos resultados."

    # Criação do campo para entrada — parte da criação dos gráficos
    plotagem.add_argument(
        "--Plotar", help=msg_plotar, widget="BlockCheckbox", action="store_true"
    )
    plotagem.add_argument(
        "--Exportar", help=msg_exportar, widget="DirChooser", action="store", type=str,
        gooey_options={
            "placeholder": "Escolha o diretório para salvar os gráficos."}
    )

    # ---------------------Configuração da parte de exclusão do arquivo intermediário em .txt---------------------
    exclusao = parser.add_argument_group(
        "Exclusão do arquivo intermediário em .txt.",
        description="Utilize essa seção para escolher se o arquivo intermediário"
                    " em .txt dos microdados deve ser excluído.",
        gooey_options={"show_border": True}
    )

    # Mensagens de ajuda
    msg_excluir = "Marque essa opção caso deseje que o arquivo intermediário em .txt seja removido."

    # Criação do campo para entrada — parte para excluir o arquivo intermediário em .txt
    exclusao.add_argument(
        "--Excluir", help=msg_excluir, widget="BlockCheckbox", action="store_true"
    )

    # Retorno dos argumentos obtidos
    args = parser.parse_args()
    return args


# Código para execução do programa

args = loop_programa()
print("Esquentando as caldeiras...")

# ---------------------Parte da extração de dados---------------------

# Definição do arquivo escolhido pelo usuário e obtenção dos nomes para transferência
mes, ano = args.Escolher.split("-")
periodo_escolhido = ano + MESES_INV[mes]
diretorio_download, nome_arquivo_ftp = criar_caminhos(periodo_escolhido)

# Checar se o arquivo .txt já não existe no diretório informado
local_salvar = args.Salvar
if os.path.isfile(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt"):
    print(
        f"\nARQUIVO CAGEDMOV{periodo_escolhido}.txt JÁ EXISTENTE. PULANDO A ETAPA DE DOWNLOAD.")
else:
    # Abertura do arquivo local
    arquivo_local = open(local_salvar + "/CAGEDMOV" +
                         periodo_escolhido + ".7z", "wb")

    # Conexão com o servidor FTP para determinar o tamanho do arquivo
    ftp = FTP(SERVER)
    ftp.login()
    ftp.cwd(diretorio_download)
    tamanho = ftp.size(nome_arquivo_ftp)
    ftp.close()

    # Variáveis para a barra de progresso da transferência
    progresso = 0
    n = 0

    # Download do arquivo
    print("\n\nEXTRAÇÃO DOS DADOS")
    baixar_arquivo(periodo_escolhido, diretorio_download,
                   nome_arquivo_ftp, local_salvar)

# ---------------------Parte do tratamento dos dados---------------------

# Checando e realizando a limpeza dos dados, deixando referente apenas ao Turismo se necessário
if args.Transformar:
    turismo = args.Turismo
    print("\n\nTRATAMENTO DOS DADOS")
    criar_df_categorias()
    dados_caged = importar_caged(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt", criar_df_categorias(),
                                 turismo)
    df_recodificado = recodificar_dummies(dados_caged, turismo)
    df_agregado = agregar_resultados(df_recodificado, turismo)
    df_agregado_final = lidar_na(df_agregado, turismo)
    print(f"\nExportando os dados trabalhados")
    if turismo:
        try:
            print(
                f"\nCaminho para salvar: {local_salvar}\\Dados trabalhados - NOVO CAGED"
                f" - Turismo - JP - {periodo_escolhido}.xlsx")
            df_agregado_final.to_excel(
                local_salvar + "/Dados trabalhados - NOVO CAGED - Turismo - JP - " +
                periodo_escolhido + ".xlsx",
                index=False)
            print("ARQUIVO FINAL .xlsx EXPORTADO COM SUCESSO.")
        except Exception as e:
            print(f"\nErro durante a exportação do arquivo: {e}")
    else:
        try:
            print(
                f"\nCaminho para salvar: {local_salvar}\\Dados trabalhados - NOVO CAGED - {periodo_escolhido}.xlsx")
            df_agregado_final.to_excel(
                local_salvar + "/Dados trabalhados - NOVO CAGED - " + periodo_escolhido + ".xlsx",
                index=False)
            print("ARQUIVO FINAL .xlsx EXPORTADO COM SUCESSO.")
        except Exception as e:
            print(f"\nErro durante a exportação do arquivo: {e}")

    # ---------------------Parte da plotagem dos gráficos---------------------

    local_exportar = args.Exportar
    if args.Plotar and args.Turismo:
        print("\n\nCRIANDO E SALVANDO AS SÍNTESES GRÁFICAS DAS INFORMAÇÕES")
        plotar_resultados(df_agregado_final, local_exportar)

# ---------------------Parte da exclusão do arquivo intermediário em .txt---------------------

if args.Excluir:
    print("\n\nEXCLUINDO ARQUIVO INTERMEDIÁRIO EM .txt")
    try:
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt")
        print(
            f"\nArquivo {local_salvar}/CAGEDMOV{periodo_escolhido}.txt excluído com sucesso.")
    except Exception as e:
        print(f"\nFalha na exclusão do arquivo. Erro: {e}")

if __name__ == "__main__":
    loop_programa()
