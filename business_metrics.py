"""
=========================================================
ZEUS AI - Business Metrics
Evaluación del modelo y métricas de negocio
=========================================================
"""

import math
import numpy as np
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error,
    r2_score
)

from config import *


class BusinessMetrics:

    def __init__(self):

        self.df = None

        self.summary = {}

        self.excursion_metrics = None

        self.monthly_metrics = None

        self.business_metrics = None

        self.daily_metrics = None


    def run(self):

        self.load_predictions()

        self.calculate_prediction_metrics()

        self.calculate_excursion_metrics()

        self.calculate_monthly_metrics()

        self.calculate_operational_metrics()

        self.calculate_daily_metrics()

        self.calculate_business_summary()

        self.save_results()

    # =====================================================
    # Métricas operativas
    # =====================================================

    def calculate_operational_metrics(self):

        print("\nCalculando métricas operativas...")

        # Autobuses necesarios
        self.df["buses_real"] = np.ceil(
            self.df["real"] / BUS_CAPACITY
        ).astype(int)

        self.df["buses_ai"] = np.ceil(
            self.df["prediction"] / BUS_CAPACITY
        ).astype(int)

        # Evitar negativos cuando la demanda es 0
        self.df.loc[self.df["real"] == 0, "buses_real"] = 0
        self.df.loc[self.df["prediction"] <= 0, "buses_ai"] = 0

        # Plazas disponibles
        self.df["capacity_real"] = (
            self.df["buses_real"] * BUS_CAPACITY
        )

        self.df["capacity_ai"] = (
            self.df["buses_ai"] * BUS_CAPACITY
        )

        # Ocupación
        self.df["occupancy_real"] = np.where(
            self.df["capacity_real"] > 0,
            self.df["real"] / self.df["capacity_real"] * 100,
            0
        )

        self.df["occupancy_ai"] = np.where(
            self.df["capacity_ai"] > 0,
            self.df["prediction"] / self.df["capacity_ai"] * 100,
            0
        )

        # Plazas vacías
        self.df["empty_real"] = (
            self.df["capacity_real"] - self.df["real"]
        )

        self.df["empty_ai"] = (
            self.df["capacity_ai"] - self.df["prediction"]
        )

        # Error de asignación
        self.df["assignment_error"] = (
            self.df["buses_ai"] -
            self.df["buses_real"]
        )

        print("OK")


    # =====================================================
    # Métricas diarias de planificación
    # =====================================================

    def calculate_daily_metrics(self):

        print("\nCalculando planificación diaria...")

        daily = (

            self.df

            .groupby("date", as_index=False)

            .agg({

                "real":"sum",

                "prediction":"sum",

                "buses_real":"sum",

                "buses_ai":"sum"

            })

        )

        # ------------------------------------
        # Diferencia
        # ------------------------------------

        daily["difference"] = (

            daily["buses_ai"]

            -

            daily["buses_real"]

        )

        # Error absoluto
        daily["abs_difference"] = daily["difference"].abs()

        # Coincidencia exacta
        daily["correct"] = (
            daily["abs_difference"] == 0
        )

        # Planificación correcta con margen de ±1 autobús
        daily["correct_1"] = (
            daily["abs_difference"] <= 1
        )

        # Planificación correcta con margen de ±2 autobuses
        daily["correct_2"] = (
            daily["abs_difference"] <= 2
        )        

        # ------------------------------------
        # Ocupación
        # ------------------------------------

        daily["occupancy_real"] = np.where(

            daily["buses_real"] > 0,

            daily["real"] /

            (daily["buses_real"] * BUS_CAPACITY)

            * 100,

            0

        )

        daily["occupancy_ai"] = np.where(

            daily["buses_ai"] > 0,

            daily["prediction"] /

            (daily["buses_ai"] * BUS_CAPACITY)

            * 100,

            0

        )

        # ------------------------------------
        # Exactitud
        # ------------------------------------

        #daily["correct"] = (

        #    daily["difference"] == 0

        #)

        self.daily_metrics = daily

        print("OK")


    def calculate_business_summary(self):

        print("\nGenerando resumen empresarial...")

        total_days = len(self.daily_metrics)

        exact_days = (

            self.daily_metrics["correct"]

            .sum()

        )

        correct1 = (
            self.daily_metrics["correct_1"].sum()
        )

        correct2 = (
            self.daily_metrics["correct_2"].sum()
        )        

        over = (

            self.daily_metrics["difference"] > 0

        ).sum()

        under = (

            self.daily_metrics["difference"] < 0

        ).sum()

        self.business_metrics = pd.DataFrame({

            "Indicador":[

                "Días evaluados",

                "Coincidencia exacta",

                "Precisión exacta (%)",

                "Precisión ±1 autobús (%)",

                "Precisión ±2 autobuses (%)",

                "Autobuses planificados",

                "Error medio (autobuses)",

                "Máximo error",

                "Sobreasignación",

                "Infraasignación",

                "Ocupación media (%)"

            ],

            "Valor":[
                total_days,

                exact_days,

                round(
                    exact_days / total_days * 100,
                    2
                ),

                round(
                    correct1 / total_days * 100,
                    2
                ),

                round(
                    correct2 / total_days * 100,
                    2
                ),

                int(
                    self.daily_metrics["buses_ai"].sum()
                ),

                round(
                    self.daily_metrics["abs_difference"].mean(),
                    2
                ),

                int(
                    self.daily_metrics["abs_difference"].max()
                ),

                over,

                under,

                round(
                    self.daily_metrics["occupancy_ai"].mean(),
                    2
                )

            ]

        })

        print("OK")

    # =====================================================
    # Guardar resultados
    # =====================================================

    def save_results(self):

        self.excursion_metrics.to_csv(

            OUTPUT / "excursion_metrics.csv",

            index=False,

            encoding="utf-8-sig"

        )

        self.monthly_metrics.to_csv(

            OUTPUT / "monthly_metrics.csv",

            index=False,

            encoding="utf-8-sig"

        )

        self.business_metrics.to_csv(

            OUTPUT / "business_metrics.csv",

            index=False,

            encoding="utf-8-sig"

        )

        self.daily_metrics.to_csv(

            OUTPUT / "daily_metrics.csv",

            index=False,

            encoding="utf-8-sig"

        )
        print("\nArchivos generados correctamente.")





    # =====================================================
    # Cargar predicciones
    # =====================================================

    def load_predictions(self):

        print("\nCargando predictions.csv...")

        self.df = pd.read_csv(

            OUTPUT / "predictions.csv",

            parse_dates=["date"]

        )

        print(f"Predicciones: {len(self.df):,}")

    # =====================================================
    # Métricas globales
    # =====================================================

    def calculate_prediction_metrics(self):

        print("\nCalculando métricas globales...")

        mae = mean_absolute_error(

            self.df["real"],

            self.df["prediction"]

        )

        rmse = np.sqrt(

            mean_squared_error(

                self.df["real"],

                self.df["prediction"]

            )

        )

        r2 = r2_score(

            self.df["real"],

            self.df["prediction"]

        )

        mape = (

            np.abs(

                (

                    self.df["real"]

                    -

                    self.df["prediction"]

                )

                /

                self.df["real"].replace(0, np.nan)

            )

        ).mean() * 100

        self.summary["MAE"] = mae

        self.summary["RMSE"] = rmse

        self.summary["MAPE"] = mape

        self.summary["R2"] = r2

        print("OK")

    # =====================================================
    # Métricas por excursión
    # =====================================================

    def calculate_excursion_metrics(self):

        print("\nCalculando métricas por excursión...")

        rows = []

        for evId, group in self.df.groupby("evId"):

            # Calcular MAPE ignorando los días con demanda 0
            valid = group[group["real"] > 0]

            if len(valid) > 0:

                mape = (
                    np.mean(
                        np.abs(
                            (
                                valid["real"] -
                                valid["prediction"]
                            ) /
                            valid["real"]
                        )
                    ) * 100
                )

            else:

                mape = np.nan


            rows.append({

                "evId": evId,

                "MAE":

                    mean_absolute_error(

                        group["real"],

                        group["prediction"]

                    ),

                "RMSE":

                    np.sqrt(

                        mean_squared_error(

                            group["real"],

                            group["prediction"]

                        )

                    ),

                "R2":
                    r2_score(
                        group["real"],
                        group["prediction"]
                    ),
                "MAPE": mape,
                "Predicciones":

                    len(group)

            })

        self.excursion_metrics = pd.DataFrame(rows)

        print("OK")

    # =====================================================
    # Métricas mensuales
    # =====================================================

    def calculate_monthly_metrics(self):

        print("\nCalculando métricas mensuales...")

        self.df["month_name"] = (

            self.df["date"]

            .dt.strftime("%Y-%m")

        )

        rows = []

        for month, group in self.df.groupby("month_name"):

            rows.append({

                "Mes": month,

                "MAE":

                    mean_absolute_error(

                        group["real"],

                        group["prediction"]

                    ),

                "RMSE":

                    np.sqrt(

                        mean_squared_error(

                            group["real"],

                            group["prediction"]

                        )

                    ),
                 "Dias": len(group)

            })

        self.monthly_metrics = pd.DataFrame(rows)

        print("OK")