"""
=========================================================
ZEUS AI - Forecasting Engine
Motor de predicción de demanda
Atlantic Dolphin Travel S.L.
=========================================================
"""

import joblib
import pandas as pd
import numpy as np

from config import *


class ZeusForecastEngine:

    def __init__(self):

        self.model = None

        self.forecasting = None

        self.real = None

        self.predictions = None


    # =====================================================
    # Cargar modelo
    # =====================================================

    def load_model(self):

        print("\n======================================")
        print("Cargando modelo Random Forest...")
        print("======================================")

        self.model = joblib.load(MODEL)

        # Obtener automáticamente las variables del modelo
        self.features = list(self.model.feature_names_in_)

        print("Modelo cargado correctamente.")

        print("\nVariables del modelo:")

        for f in self.features:
            print(" -", f)


    # =====================================================
    # Dataset forecasting
    # =====================================================

    def load_forecasting_dataset(self):

        print("\nCargando dataset forecasting...")

        self.forecasting = pd.read_csv(
            DATASET,
            parse_dates=["date"]
        )

        print(f"Registros: {len(self.forecasting):,}")


    # =====================================================
    # Dataset real
    # =====================================================

    def load_real_dataset(self):

        print("\nCargando histórico real...")

        self.real = pd.read_csv(
            "ticket_details.csv",
            parse_dates=["dateFrom"],
            low_memory=False
        )

        print(f"Reservas: {len(self.real):,}")


    # =====================================================
    # Preparar demanda real
    # =====================================================

    def prepare_real_demand(self):

        print("\nCalculando demanda real...")

        self.real["demand"] = (

            self.real["adultsNum"]

            +

            self.real["childNum"]

        )

        self.real = (

            self.real

            .groupby(

                ["dateFrom","evId"],

                as_index=False

            )["demand"]

            .sum()

        )

        self.real.rename(

            columns={

                "dateFrom":"date",

                "demand":"real"

            },

            inplace=True

        )

        print("Demanda preparada.")


    # =====================================================
    # Predicción
    # =====================================================

    def predict_period(self):

        print("\nGenerando predicciones...")

        period = self.forecasting[

            (self.forecasting["date"]>=START_DATE)

            &

            (self.forecasting["date"]<=END_DATE)

        ].copy()

        X = period[self.features]

        period["prediction"] = self.model.predict(X)

        self.predictions = period

        print(

            f"Predicciones generadas: {len(period):,}"

        )


    # =====================================================
    # Comparar con demanda real
    # =====================================================

    def merge_predictions(self):

        print("\nUniendo demanda real...")

        self.predictions = self.predictions.merge(

            self.real,

            on=["date","evId"],

            how="left"

        )

        self.predictions["real"] = (

            self.predictions["real"]

            .fillna(0)

        )

        self.predictions["abs_error"] = (

            self.predictions["prediction"]

            -

            self.predictions["real"]

        ).abs()

        print("Comparación realizada.")


    # =====================================================
    # Guardar CSV
    # =====================================================

    def save_predictions(self):

        file = OUTPUT / "predictions.csv"

        self.predictions.to_csv(

            file,

            index=False,

            encoding="utf-8-sig"

        )

        print(f"\nArchivo generado:\n{file}")


    # =====================================================
    # Ejecutar
    # =====================================================

    def run(self):

        self.load_model()

        self.load_forecasting_dataset()

        self.load_real_dataset()

        self.prepare_real_demand()

        self.predict_period()

        self.merge_predictions()

        self.save_predictions()