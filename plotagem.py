# Pacotes necessários
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Parâmetros gráficos
sns.set(style="white")
plt.rcParams["figure.dpi"] = 400
plt.rcParams["figure.figsize"] = [10, 8]
plt.rcParams["figure.autolayout"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["DejaVu Sans"]


# Funções
def plotar_resultados(dados: pd.DataFrame, periodo_escolhido: str, local: str) -> None:
    """


    :type dados: pd.DataFrame
    :type periodo_escolhido: str
    :type local: str
    """
    m = ['Admissão', 'Desligamento', 'Admissões e desligamentos']
    d1 = dados.query("`Movimentação` == 'Admissão'").reset_index()
    d2 = dados.query("`Movimentação` == 'Desligamento'").reset_index()
    d2["Saldo de movimentações"] = abs(d2["Saldo de movimentações"])
    temp = [d1, d2, dados]
    paletas = ["Accent", "Set2", "Pastel2"]
    for i in range(3):
        if not os.path.isdir(local + "/" + periodo_escolhido + " - " + m[i]):
            os.mkdir(local + "/" + periodo_escolhido + " - " + m[i])
        print(f"\nGráficos de: {m[i]}")
        print("\n(1/14) Salário médio por categoria")
        try:
            t = temp[i].groupby("Categoria").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                    "Saldo de movimentações": (
                                                        "Saldo de movimentações", "sum")}).reset_index()
            g1 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i], kind='bar',
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

            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (1/14): {e}")

        print("\n(2/14) Salário médio por escolaridade")
        try:
            t = temp[i].groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                       "Saldo de movimentações": (
                                                           "Saldo de movimentações", "sum")}).reset_index()

            g2 = sns.catplot(data=t, x="Salário médio (R$)", y="Escolaridade", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g2.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g2.set(ylabel=None)
            sns.despine()

            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_escolaridade" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (2/14): {e}")

        print("\n(3/14) Salário médio por sexo")
        try:
            t = temp[i].groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                               "Saldo de movimentações": (
                                               "Saldo de movimentações", "sum")}).reset_index()

            g3 = sns.catplot(data=t, x="Salário médio (R$)", y="Sexo",
                             palette=paletas[i], kind='bar', aspect=1.4)
            ax = g3.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g3.set(ylabel=None)
            sns.despine()
            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_sexo" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (3/14): {e}")

        print("\n(4/14) Salário médio por raça/cor")
        try:
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
                ax.bar_label(c, labels=labels, label_type='edge')
            g4.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Salário médio (R$)", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (4/14): {e}")

        print("\n(5/14) Salário médio por categoria, escolaridade e sexo")
        try:
            t = temp[i].groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g5 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
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
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_escolaridade_sexo" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (5/14): {e}")

        print("\n(6/14) Salário médio por categoria, escolaridade e raça/cor")
        try:
            t = temp[i].groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g6 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
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
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_escolaridade_raca" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (6/14): {e}")

        print("\n(7/14) Salário médio por categoria, sexo e raça/cor")
        try:
            t = temp[i].groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g7 = sns.catplot(data=t, x="Salário médio (R$)", y="Categoria", palette=paletas[i],
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
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/salario_medio_por_categoria_sexo_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (7/14): {e}")

        print("\n(8/14) Saldo de movimentações por categoria")
        try:
            t = temp[i].groupby("Categoria").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                    "Saldo de movimentações": (
                                                        "Saldo de movimentações", "sum")}).reset_index()
            g8 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g8.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            plt.xlabel("Saldo de movimentações", size=12)
            plt.tick_params(axis="both", which="major", labelsize=12)
            g8.set(ylabel=None)
            sns.despine()
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_categoria" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (8/14): {e}")

        print("\n(9/14) Saldo de movimentações por escolaridade")
        try:
            t = temp[i].groupby("Escolaridade").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                       "Saldo de movimentações": (
                                                           "Saldo de movimentações", "sum")}).reset_index()
            g9 = sns.catplot(data=t, x="Saldo de movimentações", y="Escolaridade", palette=paletas[i], kind='bar',
                             aspect=1.4)
            ax = g9.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g9.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.margins(x=0.2)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_escolaridade" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (9/14): {e}")

        print("\n(10/14) Saldo de movimentações por sexo")
        try:
            t = temp[i].groupby("Sexo").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                               "Saldo de movimentações": (
                                               "Saldo de movimentações", "sum")}).reset_index()
            g10 = sns.catplot(data=t, x="Saldo de movimentações", y="Sexo", palette=paletas[i], kind='bar',
                              aspect=1.4)
            ax = g10.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g10.set(ylabel=None)
            sns.despine()
            plt.xlabel("Saldo de movimentações", size=14)
            plt.margins(x=0.2)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_sexo" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (10/14): {e}")

        print("\n(11/14) Saldo de movimentações por raça/cor")
        try:
            t = temp[i].groupby("Raça/Cor").agg(**{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                                                   "Saldo de movimentações": (
                                                       "Saldo de movimentações", "sum")}).reset_index()
            g11 = sns.catplot(data=t, x="Saldo de movimentações", y="Raça/Cor", palette=paletas[i], kind='bar',
                              aspect=1.4)
            ax = g11.facet_axis(0, 0)
            for c in ax.containers:
                labels = [f"{(v.get_width()):.0f}" for v in c]
                ax.bar_label(c, labels=labels, label_type='edge')
            g11.set(ylabel=None)
            sns.despine()
            plt.margins(x=0.2)
            plt.xlabel("Saldo de movimentações", size=14)
            plt.savefig(local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_raca" +
                        ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (11/14): {e}")

        print("\n(12/14) Saldo de movimentações por categoria, escolaridade e sexo")
        try:
            t = temp[i].groupby(["Categoria", "Escolaridade", "Sexo"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g12 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
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
                local + "/" + periodo_escolhido + " - " + m[
                    i] + "/saldo_movimentacoes_por_categoria_escolaridade_sexo" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (12/14): {e}")

        print("\n(13/14) Saldo de movimentações por categoria, escolaridade e raça/cor")
        try:
            t = temp[i].groupby(["Categoria", "Escolaridade", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g13 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
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
                local + "/" + periodo_escolhido + " - " + m[
                    i] + "/saldo_movimentacoes_por_categoria_escolaridade_raca" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (13/14): {e}")

        print("\n(14/14) Saldo de movimentações por categoria, sexo e raça/cor")
        try:
            t = temp[i].groupby(["Categoria", "Sexo", "Raça/Cor"]).agg(
                **{"Salário médio (R$)": ("Salário médio (R$)", "mean"),
                   "Saldo de movimentações": ("Saldo de movimentações", "sum")}).reset_index()
            with sns.plotting_context(font_scale=2.25):
                g14 = sns.catplot(data=t, x="Saldo de movimentações", y="Categoria", palette=paletas[i],
                                  col="Sexo", row="Raça/Cor", kind="bar", errorbar=None, aspect=1.4, margin_titles=True,
                                  sharex=False, sharey=True, facet_kws={"despine": True})
                for ax in g14.axes.ravel():
                    # add annotations
                    for c in ax.containers:
                        labels = [f"{(v.get_width()):.0f}" for v in c]
                        ax.bar_label(c, labels=labels, label_type="edge")
                    ax.margins(x=0.1, y=0.01)
                g14.set(ylabel=None)
            plt.savefig(
                local + "/" + periodo_escolhido + " - " + m[i] + "/saldo_movimentacoes_por_categoria_sexo_raca" +
                ".svg", pad_inches=0.05, bbox_inches="tight")
            plt.close()
            print("Exportado com sucesso.")
        except Exception as e:
            print(f"Erro durante a exportação da figura (14/14): {e}")
        print(
            f"\nFIGURAS EXPORTADAS COM SUCESSO PARA A PASTA {local}/{periodo_escolhido} - {m[i]}")
