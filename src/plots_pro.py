"""
=========================================================
ZEUS AI
Professional Charts
Versión para el TFM
=========================================================
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np

from config import *
from excursions import EXCURSION_NAMES
# =====================================================
# PALETA CORPORATIVA
# =====================================================

PRIMARY = "#0B4F6C"

SECONDARY = "#F4A259"

SUCCESS = "#4CAF50"

WARNING = "#F4A259"

ERROR = "#D1495B"

GRID = "#EAEAEA"

BACKGROUND = "white"

def apply_theme():

    plt.rcParams.update({

        "figure.figsize": (13,7),

        "figure.dpi": 300,

        "axes.facecolor": BACKGROUND,

        "figure.facecolor": BACKGROUND,

        "axes.grid": True,

        "grid.color": GRID,

        "grid.alpha": 0.45,

        "axes.spines.top": False,

        "axes.spines.right": False,

        "axes.titleweight": "bold",

        "axes.titlesize": 17,

        "axes.labelsize": 12,

        "font.size": 11,

        "legend.frameon": False,

        "lines.linewidth": 2.5

    })

class ProfessionalPlots:

    def __init__(self):

        apply_theme()

        self.predictions = None

        self.excursions = None

        self.monthly = None

        self.daily = None

        self.business = None
        

    def load_data(self):

        print("Cargando datos...")

        self.predictions = pd.read_csv(

            OUTPUT / "predictions.csv",

            parse_dates=["date"]

        )

        self.excursions = pd.read_csv(

            OUTPUT / "excursion_metrics.csv"

        )

        self.monthly = pd.read_csv(

            OUTPUT / "monthly_metrics.csv"

        )

        self.daily = pd.read_csv(

            OUTPUT / "daily_metrics.csv",

            parse_dates=["date"]

        )

        self.business = pd.read_csv(

            OUTPUT / "business_metrics.csv"

        )

        self.excursions["Excursión"] = (

            self.excursions["evId"]

            .map(EXCURSION_NAMES)

        )

        print("Datos cargados.")

    # =====================================================
    # Figura 12
    # Demanda real vs Predicción
    # =====================================================

    def figure12_prediction(self):

        fig, ax = plt.subplots(figsize=(14,7))

        # -------------------------------
        # Demanda real
        # -------------------------------

        ax.plot(

            self.daily["date"],

            self.daily["real"],

            color=PRIMARY,

            linewidth=3,

            label="Demanda real"

        )

        # -------------------------------
        # Predicción IA
        # -------------------------------

        ax.plot(

            self.daily["date"],

            self.daily["prediction"],

            color=SECONDARY,

            linewidth=2.5,

            linestyle="--",

            label="Predicción ZEUS AI"

        )

        # -------------------------------
        # Zona de diferencia
        # -------------------------------

        ax.fill_between(

            self.daily["date"],

            self.daily["real"],

            self.daily["prediction"],

            color=SECONDARY,

            alpha=0.15

        )

        # -------------------------------
        # Formato
        # -------------------------------

        ax.set_title( "Comparación entre la demanda real y la demanda predicha",pad=20)

        ax.set_xlabel("Fecha")

        ax.set_ylabel("Número de pasajeros")

        ax.legend(loc="upper right")

        ax.grid(True, alpha=0.30)

        plt.tight_layout()

        import matplotlib.dates as mdates

        ax.xaxis.set_major_locator(

            mdates.MonthLocator(interval=2)

        )

        ax.xaxis.set_major_formatter(

            mdates.DateFormatter("%b %Y")

        )

        plt.xticks(rotation=45)   

        plt.savefig(

            FIGURES / "fig12_prediction_pro.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()


    # =====================================================
    # Figura 13
    # Evolución mensual del MAE
    # =====================================================

    def figure13_monthly(self):
        data = self.monthly.copy()

        if "Dias" in data.columns:
            data = data[data["Dias"] >= 20]
        fig, ax = plt.subplots(figsize=(12,6))

        bars = ax.bar(

            data["Mes"],

            data["MAE"],

            color=PRIMARY,

            edgecolor="black",

            linewidth=0.5

        )

        for bar in bars:

            h = bar.get_height()

            ax.text(

                bar.get_x() + bar.get_width()/2,

                h + 0.08,

                f"{h:.2f}",

                ha="center",

                fontsize=10

            )

        ax.set_title( "Evolución mensual del error absoluto medio (MAE)",pad=20)

        ax.set_ylabel("MAE")

        plt.xticks(rotation=45)

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig13_monthly_mae_pro.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # =====================================================
    # Figura 14
    # Ranking por excursión
    # =====================================================

    def figure14_excursions(self):

        data = self.excursions.sort_values("MAE")

        fig, ax = plt.subplots(figsize=(12,7))

        bars = ax.barh(

            data["Excursión"],

            data["MAE"],

            color=PRIMARY

        )

        for bar in bars:

            w = bar.get_width()

            ax.text(

                w + 0.05,

                bar.get_y() + bar.get_height()/2,

                f"{w:.2f}",

                va="center",

                fontsize=10

            )

        ax.set_title(

            "Error medio obtenido para cada excursión",

            pad=20

        )

        ax.set_xlabel("MAE")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig14_excursions_pro.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()

    # =====================================================
    # Figura 15
    # Planificación diaria de autobuses
    # =====================================================

    def figure15_buses(self):

        fig, ax = plt.subplots(figsize=(14,7))

        # Autobuses reales
        ax.plot(
            self.daily["date"],
            self.daily["buses_real"],
            color=PRIMARY,
            linewidth=3,
            label="Autobuses necesarios"
        )

        # Autobuses IA
        ax.plot(
            self.daily["date"],
            self.daily["buses_ai"],
            color=SECONDARY,
            linewidth=2.5,
            linestyle="--",
            label="Planificación ZEUS AI"
        )

        # Diferencia entre ambas curvas
        ax.fill_between(
            self.daily["date"],
            self.daily["buses_real"],
            self.daily["buses_ai"],
            alpha=0.18,
            color=SECONDARY
        )

        # ==========================================
        # Estadísticas operativas
        # ==========================================

        precision0 = (
            self.daily["correct"].mean() * 100
        )

        precision1 = (
            self.daily["correct_1"].mean() * 100
        )

        precision2 = (
            self.daily["correct_2"].mean() * 100
        )

        error = (
            self.daily["abs_difference"].mean()
        )

        texto = (
            "RESUMEN OPERATIVO\n\n"
            f"Días evaluados: {len(self.daily)}\n"
            f"Error medio: {error:.2f} autobuses\n"
            f"Precisión ±1 autobús: {precision1:.1f}%\n"
            f"Precisión ±2 autobuses: {precision2:.1f}%"
        )

        ax.text(
            0.02,
            0.98,
            texto,
            transform=ax.transAxes,
            fontsize=10,
            verticalalignment="top",
            bbox=dict(
                boxstyle="round,pad=0.8",
                facecolor="white",
                edgecolor="#CCCCCC"
            )
        )

        # Fechas
        import matplotlib.dates as mdates

        ax.xaxis.set_major_locator(
            mdates.MonthLocator(interval=2)
        )

        ax.xaxis.set_major_formatter(
            mdates.DateFormatter("%b %Y")
        )

        plt.xticks(rotation=45)

        ax.set_ylabel("Número de autobuses")
        ax.set_xlabel("Fecha")

        ax.set_title(
            "Comparación entre la planificación real y la estimada por ZEUS AI",
            pad=20
        )

        ax.legend()

        plt.tight_layout()

        plt.savefig(
            FIGURES / "fig15_buses_pro.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()


    # =====================================================
    # Figura 16
    # Distribución del error
    # =====================================================

    def figure16_error(self):

        freq = (

            self.daily["difference"]

            .value_counts()

            .sort_index()

        )

        fig, ax = plt.subplots(figsize=(10,6))

        bars = ax.bar(

            freq.index.astype(str),

            freq.values,

            color=WARNING

        )

        for bar in bars:

            h = bar.get_height()

            ax.text(

                bar.get_x() + bar.get_width()/2,

                h + 1,

                str(int(h)),

                ha="center",

                fontsize=10

            )

        ax.set_title(

            "Distribución del error de planificación",

            pad=20

        )

        ax.set_xlabel("Error (autobuses)")

        ax.set_ylabel("Número de días")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig16_error_distribution_pro.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()



    # =====================================================
    # Figura 17
    # Dashboard ejecutivo
    # =====================================================

    def figure17_dashboard(self):

        fig = plt.figure(figsize=(14,8))
        fig.patch.set_facecolor("white")

        # Recuperar métricas
        precision = self.daily["correct"].mean() * 100

        mae = (
            abs(
                self.predictions["real"] -
                self.predictions["prediction"]
            ).mean()
        )

        rmse = np.sqrt(
            (
                (
                    self.predictions["real"] -
                    self.predictions["prediction"]
                )**2
            ).mean()
        )

        ocupacion = self.daily["occupancy_ai"].mean()

        autobuses = self.daily["buses_ai"].sum()

        datos = [

            ("Precisión\nplanificación",
            f"{precision:.1f} %",
            SUCCESS),

            ("MAE",
            f"{mae:.2f}",
            PRIMARY),

            ("RMSE",
            f"{rmse:.2f}",
            WARNING),

            ("Ocupación\nmedia",
            f"{ocupacion:.1f} %",
            SECONDARY),

            ("Autobuses\nplanificados",
            f"{int(autobuses)}",
            PRIMARY)

        ]

        columnas = len(datos)

        for i, (titulo, valor, color) in enumerate(datos):

            ax = fig.add_subplot(1, columnas, i+1)

            ax.set_xticks([])
            ax.set_yticks([])

            for spine in ax.spines.values():
                spine.set_visible(False)

            ax.set_facecolor("#F8F8F8")

            ax.text(
                0.5,
                0.72,
                titulo,
                ha="center",
                fontsize=13,
                weight="bold"
            )

            ax.text(
                0.5,
                0.38,
                valor,
                ha="center",
                fontsize=24,
                weight="bold",
                color=color
            )

        plt.suptitle(
            "Indicadores principales del sistema ZEUS AI",
            fontsize=18,
            weight="bold"
        )

        plt.figtext(
            0.01,
            0.01,
            "Fuente: Elaboración propia.",
            fontsize=9,
            color="gray"
        )

        plt.tight_layout()

        plt.savefig(
            FIGURES / "fig17_dashboard_pro.png",
            dpi=300,
            bbox_inches="tight"
        )

        plt.close()


    # =====================================================
    # Figura 18
    # Ranking de precisión
    # =====================================================

    def figure18_ranking(self):

        data = self.excursions.copy()

        data["Score"] = (
            1 /
            (1 + data["MAE"])
        ) * 100

        data = data.sort_values(
            "Score",
            ascending=False
        )

        fig, ax = plt.subplots(figsize=(12,7))

        bars = ax.barh(

            data["Excursión"],

            data["Score"],

            color=SUCCESS

        )

        for bar in bars:

            w = bar.get_width()

            ax.text(

                w + 0.5,

                bar.get_y() + bar.get_height()/2,

                f"{w:.1f}%",

                va="center",

                fontsize=10

            )

        ax.invert_yaxis()

        ax.set_xlabel("Índice de precisión")

        ax.set_title(

            "Ranking de precisión predictiva por excursión",

            pad=20

        )

        plt.figtext(

            0.01,

            -0.02,

            "Fuente: Elaboración propia.",

            fontsize=9,

            color="gray"

        )

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig18_ranking_pro.png",

            dpi=300,

            bbox_inches="tight"

        )

        plt.close()



    # =====================================================
    # Ejecutar
    # =====================================================
    def run(self):

        self.load_data()

        self.figure12_prediction()

        self.figure13_monthly()

        self.figure14_excursions()

        self.figure15_buses()

        self.figure16_error()

        self.figure17_dashboard()

        self.figure18_ranking()

        print("\nTodas las figuras PRO generadas correctamente.")