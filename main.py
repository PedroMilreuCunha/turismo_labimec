# Pacotes necessários
import os

from gooey import Gooey, GooeyParser
from colored import stylize, fg, attr, set_tty_aware

from download import obter_diretorios_caged, criar_caminhos, baixar_arquivo
from tratamento import criar_df_categorias, importar_caged, recodificar_dummies, agregar_resultados, lidar_na
from plotagem import plotar_resultados

set_tty_aware(False)

# DECLARAÇÃO DE CONSTANTES
SERVER = "ftp.mtps.gov.br"
MESES = {"01": "Janeiro", "02": "Fevereiro", "03": "Março", "04": "Abril", "05": "Maio", "06": "Junho",
         "07": "Julho", "08": "Agosto", "09": "Setembro", "10": "Outubro", "11": "Novembro", "12": "Dezembro"}
MESES_INV = dict((v, k) for k, v in MESES.items())


@Gooey(dump_build_config=False, clear_before_run=True,
       program_name="Utilitário para extração, leitura, tratamento e visualização de"
                    " microdados do NOVO CAGED sobre turismo - LABIMEC",
       language="portuguese", default_size=(1000, 600), image_dir="figs", language_dir="lang",
       show_restart_button=False, richtext_controls=True,
       timing_options={
           'show_time_remaining': True,
           'hide_time_remaining_on_complete': True
       },
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
               "version": "2.0",
               "copyright": "2022",
               "website": " https://www.ufpb.br/labimec",
               "developer": "Pedro Milreu Cunha - Doutorando e Mestre em Economia"
                            " Aplicada pelo PPGE/UFPB e \nBacharel em Ciências Econômicas pela UFV"
                            "\n https://github.com/PedroMilreuCunha",
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
        gooey_options={"show_border": True, "margin": 25}
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
        m = i[-2:]
        a = i[0:4]
        visualizacao_arquivos_disponiveis.append(MESES[m] + "-" + a)

    # Criação dos campos para entrada — parte da extração dos dados
    extracao.add_argument(
        "Escolher", help=msg_arquivos, widget="FilterableDropdown", choices=visualizacao_arquivos_disponiveis,
        gooey_options={
            "placeholder": "Comece a escrever o nome do mês que deseja para ver sugestões (Janeiro, por exemplo)."}
    )
    extracao.add_argument(
        "Salvar", help=msg_salvar, widget="DirChooser", action="store", type=str,
        gooey_options={
            "placeholder": "Escolha um diretório para salvar o arquivo final em .xlsx."}
    )

    # Configuração da parte de transformção dos microdados do NOVO CAGED
    transformacao = parser.add_argument_group(
        "Transformação dos dados",
        description="Utilize essa seção para marcar se deseja realizar uma limpeza e agregação dos dados e, também,"
                    "se deve ser feita uma análise especificamente para o setor de turismo de João Pessoa.",
        gooey_options={"show_border": True, "margin": 25}
    )
    # Mensagens de ajuda
    msg_transformar = "Marque essa opção caso deseje que os dados sejam" \
                      " trabalhados, organizados e agregados por escolaridade," \
                      "município, raça/cor e sexo."
    msg_turismo_jp = "Marque essa opção caso deseje que os dados trabalhados" \
                     " façam referência apenas às categorias do turismo e ao município de João Pessoa."

    # Criação do campo para entrada — parte do tratamento dos dados
    transformacao.add_argument(
        "--Transformar", help=msg_transformar, widget="BlockCheckbox", action="store_true"
    )
    # Criação do campo para entrada — parte do tratamento em relação ao turismo e João Pessoa
    transformacao.add_argument(
        "--Turismo", help=msg_turismo_jp, widget="BlockCheckbox", action="store_true"
    )

    # Configuração da parte de visualização de sínteses dos resultados
    plotagem = parser.add_argument_group(
        "Visualização dos dados",
        description="IMPORTANTE:\n\n"
                    "> DISPONÍVEL APENAS PARA OS DADOS DO TURISMO DE JOÃO PESSOA\n\n"
                    "> SE OPTAR POR GERAR OS GRÁFICOS, NÃO DEIXE DE ESCOLHER UM DIRETÓRIO PARA SALVÁ-LOS\n\n"
                    "Utilize essa seção para escolher se os gráficos-síntese dos resultados devem ser elaborados"
                    " e exportados.",
        gooey_options={"show_border": True, "margin": 25}
    )

    plotagem_radio = plotagem.add_mutually_exclusive_group(gooey_options={"title": "Criação de gráficos em .svg"})

    # Mensagem de ajuda
    msg_exportar = "Selecione a pasta onde deseja salvar as visualizações gráficas dos resultados."

    plotagem_radio.add_argument(
        "--Exportar", help=msg_exportar, widget="DirChooser", type=str,
        gooey_options={
            "placeholder": "Escolha o diretório para salvar os gráficos."}
    )

    # Configuração da parte de exclusão do arquivo intermediário em .txt
    exclusao = parser.add_argument_group(
        "Exclusão do arquivo intermediário em .txt.",
        description="Utilize essa seção para escolher se o arquivo intermediário"
                    " em .txt dos microdados deve ser excluído.",
        gooey_options={"show_border": True, "margin": 25}
    )

    # Mensagens de ajuda
    msg_excluir = "Marque essa opção caso deseje que o arquivo intermediário em .txt seja removido."

    # Criação do campo para entrada — parte para excluir o arquivo intermediário em .txt
    exclusao.add_argument(
        "--Excluir", help=msg_excluir, widget="BlockCheckbox", action="store_true"
    )

    # Retorno dos argumentos obtidos
    a = parser.parse_args()
    return a


# Código para execução do programa

args = loop_programa()
print(stylize("Para utilizar o programa novamente basta clicar no botão"
      " 'voltar' ao final da execução.\n", fg("red") + attr("bold")))
# Parte da extração de dados

# Definição do arquivo escolhido pelo usuário e obtenção dos nomes para transferência
mes, ano = args.Escolher.split("-")
periodo_escolhido = ano + MESES_INV[mes]
diretorio_download, nome_arquivo_ftp = criar_caminhos(periodo_escolhido)

# Checar se o arquivo txt já não existe no diretório informado
local_salvar = args.Salvar
if os.path.isfile(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt"):
    print(stylize("ARQUIVO CAGEDMOV" + periodo_escolhido + ".txt JÁ EXISTENTE. PULANDO A ETAPA DE DOWNLOAD.",
          fg("green")))
else:
    # Download do arquivo
    print(stylize("DOWNLOAD DOS DADOS", fg("magenta") + attr("bold")))
    baixar_arquivo(periodo_escolhido, diretorio_download,
                   nome_arquivo_ftp, local_salvar)

# Parte do tratamento dos dados

# Checando e realizando a limpeza dos dados, deixando referente apenas ao Turismo se necessário
if args.Transformar:
    turismo = args.Turismo
    print()
    print(stylize("TRATAMENTO DOS DADOS", fg("magenta") + attr("bold")))
    criar_df_categorias()
    dados_caged = importar_caged(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt", criar_df_categorias(),
                                 turismo)
    df_recodificado = recodificar_dummies(dados_caged, turismo)
    df_agregado = agregar_resultados(df_recodificado, turismo)
    df_agregado_final = lidar_na(df_agregado, periodo_escolhido, turismo)
    print(f"\nExportando os dados trabalhados")
    if turismo:
        try:
            print(
                f"\nCaminho para salvar: {local_salvar}\\Dados trabalhados - NOVO CAGED"
                f" - Turismo - JP - {periodo_escolhido}.xlsx\n")
            df_agregado_final.to_excel(
                local_salvar + "/Dados trabalhados - NOVO CAGED - Turismo - JP - " +
                periodo_escolhido + ".xlsx",
                index=False)
            print(stylize("Arquivo final .xlsx exportado com sucesso.", fg("green") + attr("bold")))
        except Exception as e:
            print(stylize("ERRO DURANTE A EXPORTAÇÃO DO ARQUIVO: " + str(e), fg("red") + attr("bold")))
    else:
        try:
            print(
                f"\nCaminho para salvar: {local_salvar}\\Dados trabalhados - NOVO CAGED - {periodo_escolhido}.xlsx\n")
            df_agregado_final.to_excel(
                local_salvar + "/Dados trabalhados - NOVO CAGED - " + periodo_escolhido + ".xlsx",
                index=False)
            print(stylize("Arquivo final .xlsx exportado com sucesso.", fg("green") + attr("bold")))
        except Exception as e:
            print(stylize("ERRO DURANTE A EXPORTAÇÃO DO ARQUIVO: " + str(e), fg("red") + attr("bold")))

    # Parte da plotagem dos gráficos

    local_exportar = args.Exportar
    if args.Exportar and args.Turismo:
        print()
        print(stylize("CRIANDO E SALVANDO AS SÍNTESES GRÁFICAS DAS INFORMAÇÕES", fg("magenta") + attr("bold")))
        plotar_resultados(df_agregado_final, periodo_escolhido, local_exportar)

# Parte da exclusão do arquivo intermediário em .txt

if args.Excluir:
    print()
    print(stylize("EXCLUINDO ARQUIVO INTERMEDIÁRIO EM .txt\n", fg("magenta") + attr("bold")))
    try:
        os.remove(local_salvar + "/CAGEDMOV" + periodo_escolhido + ".txt")
        print(stylize("Arquivo " + local_salvar + "\\CAGEDMOV" + periodo_escolhido + ".txt excluído com sucesso.",
              fg("green") + attr("bold")))
    except Exception as e:
        print(stylize("FALHA NA EXCLUSÃO DO ARQUIVO. Erro: " + str(e), fg("red") + attr("bold")))

if __name__ == "__main__":
    loop_programa()
