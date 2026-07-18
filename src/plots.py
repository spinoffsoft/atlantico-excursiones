"""
=========================================================
ZEUS AI
Generación automática de figuras del TFM
=========================================================
"""

import matplotlib.pyplot as plt
import pandas as pd

from config import *

plt.rcParams["figure.figsize"] = (12,6)
plt.rcParams["font.size"] = 11


class ZeusPlots:

    def __init__(self):

        self.predictions = None
        self.excursions = None
        self.monthly = None
        self.daily = None
        self.business = None


    # =====================================================
    # Cargar datos
    # =====================================================

    def load_data(self):

        print("\nCargando datos...")

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

        print("OK")

    # =====================================================
    # Figura 12
    # =====================================================

    def figure_prediction(self):

        plt.figure()

        plt.plot(
            self.daily["date"],
            self.daily["real"],
            label="Demanda real"
        )

        plt.plot(
            self.daily["date"],
            self.daily["prediction"],
            label="Predicción IA"
        )

        plt.title("Figura 12. Demanda real frente a demanda predicha")

        plt.xlabel("Fecha")

        plt.ylabel("Pasajeros")

        plt.legend()

        plt.tight_layout()

        plt.savefig(
            FIGURES / "fig12_prediction.png",
            dpi=300
        )

        plt.close()

    # =====================================================
    # Figura 13
    # =====================================================

    def figure_monthly(self):

        plt.figure()

        plt.bar(

            self.monthly["Mes"],

            self.monthly["MAE"]

        )

        plt.xticks(rotation=45)

        plt.ylabel("MAE")

        plt.title("Figura 13. Error medio mensual")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig13_monthly_mae.png",

            dpi=300

        )

        plt.close()

    # =====================================================
    # Figura 14
    # =====================================================

    def figure_excursions(self):

        data = self.excursions.sort_values("MAE")

        plt.figure()

        plt.barh(

            data["evId"].astype(str),

            data["MAE"]

        )

        plt.xlabel("MAE")

        plt.ylabel("Excursión")

        plt.title("Figura 14. Error medio por excursión")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig14_excursions.png",

            dpi=300

        )

        plt.close()

    # =====================================================
    # Figura 15
    # =====================================================

    def figure_buses(self):

        plt.figure()

        plt.plot(

            self.daily["date"],

            self.daily["buses_real"],

            label="Necesarios"

        )

        plt.plot(

            self.daily["date"],

            self.daily["buses_ai"],

            label="ZEUS AI"

        )

        plt.legend()

        plt.ylabel("Autobuses")

        plt.title("Figura 15. Planificación diaria de autobuses")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig15_buses.png",

            dpi=300

        )

        plt.close()

    # =====================================================
    # Figura 16
    # =====================================================

    def figure_error(self):

        plt.figure()

        plt.hist(

            self.daily["difference"],

            bins=15

        )

        plt.xlabel("Error (autobuses)")

        plt.ylabel("Número de días")

        plt.title("Figura 16. Distribución del error de planificación")

        plt.tight_layout()

        plt.savefig(

            FIGURES / "fig16_error_distribution.png",

            dpi=300

        )

        plt.close()


    # =====================================================
    # Ejecutar
    # =====================================================

    def run(self):

        self.load_data()

        self.figure_prediction()

        self.figure_monthly()

        self.figure_excursions()

        self.figure_buses()

        self.figure_error()

        print("\nTodas las figuras generadas.")