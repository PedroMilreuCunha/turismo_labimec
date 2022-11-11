# Pacotes necessários
# !pip install openpyxl
import numpy as np
import pandas as pd

from colored import stylize, fg, attr

# DECLARAÇÃO DE CONSTANTES
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


# Funções


def criar_df_categorias() -> pd.DataFrame:
    """
    A função é utilizada para gerar o pd.DataFrame com as categorias do turismo
    a partir das constantes definidas no início do código. Ela retorna um
    pd.DataFrame chamado df_categorias_turismo.

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
    Função utilizada para importar o arquivo em .txt com as informações do NOVO
    CAGED que foi baixado pelo programa. Utiliza quatro parâmetros: nome_arquivo,
    uma string com o caminho para o arquivo; df_categorias_turismo, o pd.DataFrame
    criado pela função criar_df_categorias e turismo, uma variável booleana
    utilizada para definir se a filtragem relacionada ao turismo em João Pessoa
    deve ser realizada.

    Retorna um pd.DataFrame com os dados do arquivo .txt e, caso turismo==True,
    realiza as devidas filtragens nele antes de retorná-lo.

    ** Essa função provavelmente será alterada no futuro **
    :rtype df_caged: pd.DataFrame
    :param nome_arquivo: str
    :param df_categorias_turismo: pd.DataFrame
    :param turismo: bool
    """
    dados_caged = pd.DataFrame()
    if turismo:
        print(
            f"\nImportando os dados da CAGED e criando o pd.DataFrame apenas com os dados referentes"
            f" ao turismo em João Pessoa")
        try:
            dados_caged_turismo_jp = pd.read_csv(nome_arquivo, decimal=",", sep=";")
            dados_caged_turismo_jp = dados_caged_turismo_jp[dados_caged_turismo_jp["município"] == 250750]
            dados_caged_turismo_jp = df_categorias_turismo.merge(dados_caged_turismo_jp, how="left",
                                                                 left_on="Subclasse",
                                                                 right_on="subclasse").reset_index()
            dados_caged = dados_caged_turismo_jp
        except Exception as e:
            print(stylize("ERRO DURANTE A IMPORTAÇÃO DO ARQUIVO " + nome_arquivo + ": " + str(e),
                          fg("red") + attr("bold")))
    else:
        print(f"\nImportando os dados da CAGED e criando o pd.DataFrame com os dados")
        try:
            dados_caged = pd.read_csv(nome_arquivo, decimal=",", sep=";")
        except Exception as e:
            print(stylize("ERRO DURANTE A IMPORTAÇÃO DO ARQUIVO " + nome_arquivo + ": " + str(e),
                          fg("red") + attr("bold")))
    return dados_caged


def recodificar_dummies(dados_caged: pd.DataFrame, turismo: bool) -> pd.DataFrame:
    """
    Função utilizada para recodificar as variáveis dummies presentes nos dados.
    Têm dois parâmetros: dados_caged, o pd.DataFrame com as informações do NOVO
    CAGED e turismo, variável booleana indicando se o usuário optou apenas
    pelas informações relacionadas ao turismo em João Pessoa.

    Retorna um pd.DataFrame semelhante ao dados_caged, porém com as variáveis
    devidamente recodificadas.
    :rtype df_recodificado: pd.DataFrame
    :param dados_caged: pd.DataFrame
    :param turismo: bool
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
    Utilizada para agregar as informações a partir do pd.DataFrame df_recodificado
    e da variável booleana turismo, que serve para inferir o tipo correto de
    agregação a ser feita.

    Retorna um pd.DataFrame com os resultados agregados segundo o ditado
    pela escolha do usuário.
    :rtype df_agregado: pd.DataFrame
    :param df_recodificado: pd.DataFrame
    :param turismo: bool
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


def lidar_na(df_agregado: pd.DataFrame, periodo_escolhido: str, turismo: bool) -> pd.DataFrame:
    """
    Função utilizada para lidar com as informações ausentes nos dados. Recebe um
    pd.DataFrame com os dados agregados (pd.DataFrame df_agregado), o período
    escolhido pelo usuário (string periodo_escolhido) e a variável booleana
    turismo, que serve para decidir os nomes corretos das colunas do
    pd.DataFrame resultante.

    Retorna um pd.DataFrame com os dados ausentes tratados de acordo com o
    tipo da variável original.
    :rtype df_agregado_final: pd.DataFrame
    :param df_agregado: pd.DataFrame
    :param periodo_escolhido: str
    :param turismo: bool
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
