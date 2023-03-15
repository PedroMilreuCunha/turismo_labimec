# Pacotes necessários
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

from colored import stylize, fg, attr
from tqdm.rich import tqdm
import warnings
warnings.filterwarnings("ignore")

# Parâmetros gráficos
sns.set(style="white", font_scale = 1.4)
plt.rcParams["figure.dpi"] = 600
plt.rcParams["figure.figsize"] = [15, 12]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.serif"] = ["Tahoma"]


# Funções


def plotar_resultados(dados: pd.DataFrame, periodo_escolhido: str, local: str) -> None:
    """
    Função utilizada para gerar as sínteses gráficas do resultado. Utiliza três
    parâmetros para isso: dados, um pd.DataFrame com as informações a serem
    plotadas; periodo_escolhido, uma string utilizada para nomear os arquivos
    e local, outra string que representa o caminho para o local onde as
    figuras serão salvas.

    A função não retorna nada, sendo só um 'wrapper' conveniente para automatizar
    o processo de geração das figuras.

    :param dados: pd.DataFrame
    :param periodo_escolhido: str
    :param local: str
    """
    m = ['Admissões', 'Desligamentos', 'Admissões e desligamentos']
    d1 = dados.query("`Movimentação` == 'Admissão'").reset_index()
    d2 = dados.query("`Movimentação` == 'Desligamento'").reset_index()
    d2["Saldo de movimentações"] = abs(d2["Saldo de movimentações"])
    temp = [d1, d2, dados]
    paletas = ["Accent", "Set2", "Pastel2"]

    for i in range(3):
        print()
        print(stylize("Gráficos de: " + m[i], attr("bold")))
        pbar = tqdm(total=14, desc="", unit="gráficos",
                    dynamic_ncols=True, position=0)
        try:
            if not os.path.isdir(local + "/" + periodo_escolhido + " - " + m[i]):
                os.mkdir(local + "/" + periodo_escolhido + " - " + m[i])
                t = temp[i].groupby("Categoria").agg(
                    **{
                        "Salário médio (R$)": ("Salário médio (R$)", "mean"),
                        "Saldo de movimentações": ("Saldo de movimentações", "sum")
                    }
                ).reset_index()

                g1 = sns.catplot(
                    data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i], kind='bar', aspect=1.4
                )
                ax = g1.facet_axis(0, 0)
                for c in ax.containers:
                    labels = [f"{(v.get_width()):.0f}" for v in c]
                    ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
                plt.xlabel('Salário médio (R$)',
                           fontsize = 14)
                plt.xlim(0, max(t['Salário médio (R$)']) + 300)
                plt.tick_params(axis="both", which="major", labelsize=14)
                plt.minorticks_off()
                g1.set(ylabel=None)
                sns.despine()

            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por escolaridade
            t = temp[i].groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                       "Saldo de movimentações": (
                                                           "Saldo de movimentações", "sum")}).reset_index()
            g2 = sns.catplot(data=t, x="Salário médio (R$)", y="Escolaridade", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g2.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g2.set(ylabel=None)
            sns.despine()
            plt.xlabel("Salário médio (R$)", size=14)
            plt.xlim(0, max(t['Salário médio (R$)']) + 300)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_escolaridade" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por sexo
            t = temp[i].groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                               "Saldo de movimentações": (
                                                   "Saldo de movimentações", "sum")}).reset_index()
            g3 = sns.catplot(data=t, x="Salário médio (R$)", y="Sexo",
                             palette=paletas[i], kind='bar', aspect=1.4)
            ax = g3.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g3.set(ylabel=None)
            sns.despine()
            plt.xlabel("Salário médio (R$)", size=14)
            plt.xlim(0, max(t['Salário médio (R$)']) + 300)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_sexo" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por raça/cor
            t = (
                temp[i].groupby("Raça/Cor")
                .agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                        "Saldo de movimentações": ("Saldo de movimentações", "sum")})
                .reset_index()
            )
            g4 = sns.catplot(data=t, x="Salário médio (R$)", y="Raça/Cor", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g4.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g4.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Salário médio (R$)", size=14)
            plt.xlim(0, max(t['Salário médio (R$)']) + 300)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_raca" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por categoria, escolaridade e sexo
            t = temp[i].groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g5 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
                                 col="Sexo", row="Escolaridade", kind="bar", errorbar=None, aspect=1.4,
                                 margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g5.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g5.set(ylabel=None)
                sns.despine()
            plt.minorticks_off()
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_escolaridade_sexo" +
                ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por categoria, escolaridade e raça/cor
            t = temp[i].groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g6 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
                                 row="Escolaridade", col="Raça/Cor", kind="bar", errorbar=None, aspect=1.4,
                                 margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g6.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g6.set(ylabel=None)
                sns.despine()
            plt.minorticks_off()
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_escolaridade_raca" +
                ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Salário médio por categoria, sexo e raça/cor
            t = temp[i].groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g7 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
                                 col="Sexo", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4, margin_titles=True,
                                 sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g7.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g7.set(ylabel=None)
                sns.despine()
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_sexo_raca" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por categoria
            t = temp[i].groupby("Categoria").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                    "Saldo de movimentações": (
                                                        "Saldo de movimentações", "sum")}).reset_index()
            g8 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g8.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            plt.xlabel("Saldo de movimentações", size=14)
            plt.xlim(min(t['Saldo de movimentações']) - 20, max(t['Saldo de movimentações']) + 20)
            plt.tick_params(axis="both", which="major", labelsize=12)
            g8.set(ylabel=None)
            sns.despine()
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_categoria" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por escolaridade
            t = temp[i].groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                       "Saldo de movimentações": (
                                                           "Saldo de movimentações", "sum")}).reset_index()
            g9 = sns.catplot(data=t, x="Saldo de movimentações", y="Escolaridade", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g9.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g9.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.xlim(min(t['Saldo de movimentações']) - 20, max(t['Saldo de movimentações']) + 20)
            plt.margins(x=0.2)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_escolaridade" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por sexo
            t = temp[i].groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                               "Saldo de movimentações": (
                                                   "Saldo de movimentações", "sum")}).reset_index()
            g10 = sns.catplot(data=t, x="Saldo de movimentações", y="Sexo", palette=paletas[i], kind='bar',
                              aspect=1.4)
            ax = g10.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g10.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.xlim(min(t['Saldo de movimentações']) - 20, max(t['Saldo de movimentações']) + 20)
            plt.margins(x=0.2)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_sexo" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por raça/cor
            t = temp[i].groupby("Raça/Cor").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                   "Saldo de movimentações": (
                                                       "Saldo de movimentações", "sum")}).reset_index()
            g11 = sns.catplot(data=t, x="Saldo de movimentações", y="Raça/Cor", palette=paletas[i], kind='bar',
                              aspect=1.4)
            ax = g11.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge', padding=0.075)
            g11.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Saldo de movimentações", size=14)
            plt.xlim(min(t['Saldo de movimentações']) - 20, max(t['Saldo de movimentações']) + 20)
            plt.minorticks_off()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_raca" +
                        ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por categoria, escolaridade e sexo
            t = temp[i].groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g12 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
                                  col="Sexo", row="Escolaridade", kind="bar", errorbar=None, aspect=1.4,
                                  margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g12.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g12.set(ylabel=None)
            plt.minorticks_off()
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[
                    i] + "/saldo_movimentacoes_por_categoria_escolaridade_sexo" +
                ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por categoria, escolaridade e raça/cor
            t = temp[i].groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g13 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
                                  row="Escolaridade", col="Raça/Cor", kind="bar", errorbar=None, aspect=1.4,
                                  margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g13.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g13.set(ylabel=None)
            plt.minorticks_off()
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[
                    i] + "/saldo_movimentacoes_por_categoria_escolaridade_raca" +
                ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)

            # Saldo de movimentações por categoria, sexo e raça/cor
            t = temp[i].groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g14 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
                                  col="Sexo", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4, margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g14.axes.ravel():
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g14.set(ylabel=None)
            plt.minorticks_off()
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_categoria_sexo_raca" +
                ".svg", pad_inches=0.15, bbox_inches="tight")
            plt.close()
            pbar.update(1)
            print(stylize(pbar, fg("light_blue")), flush=True)
        except Exception as e:
            print(stylize("ERRO DURANTE A CRIAÇÃO/EXPORTAÇÃO DAS FIGURAS: " + str(e), fg("red") + attr("bold")))
        pbar.close()
        print()
        print(stylize("FIGURAS EXPORTADAS COM SUCESSO PARA A PASTA " + local + "\\" + periodo_escolhido + " - " + m[i],
                      fg("green") + attr("bold")))
