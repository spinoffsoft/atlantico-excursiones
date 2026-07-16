"""
=========================================================
ZEUS AI - Model Evaluation
Evaluación científica del modelo
=========================================================
"""

import joblib
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from config import *


class ModelEvaluation:

    def __init__(self):

        self.model = None

        self.dataset = None

        self.X_train = None
        self.X_test = None

        self.y_train = None
        self.y_test = None

        self.predictions = None

        self.metrics = {}

    # =====================================================
    # Cargar modelo
    # =====================================================

    def load_model(self):

        print("\nCargando modelo...")

        self.model = joblib.load(MODEL)

        print("Modelo cargado correctamente.")

    # =====================================================
    # Dataset
    # =====================================================

    def load_dataset(self):

        print("\nCargando dataset...")

        self.dataset = pd.read_csv(
            DATASET,
            parse_dates=["date"]
        )

        print(f"Registros: {len(self.dataset):,}")

    # =====================================================
    # Preparar dataset
    # =====================================================

    def prepare_dataset(self):

        X = self.dataset.drop(
            columns=[
                "demand",
                "date",
                "series"
            ]
        )

        y = self.dataset["demand"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            shuffle=False
        )

        print("Dataset preparado.")

    # =====================================================
    # Evaluación
    # =====================================================

    def evaluate(self):

        print("\nEvaluando modelo...")

        self.predictions = self.model.predict(
            self.X_test
        )

        mae = mean_absolute_error(
            self.y_test,
            self.predictions
        )

        rmse = np.sqrt(
            mean_squared_error(
                self.y_test,
                self.predictions
            )
        )

        r2 = r2_score(
            self.y_test,
            self.predictions
        )

        mape = (
            np.abs(
                (
                    self.y_test -
                    self.predictions
                )
                /
                self.y_test.replace(0, np.nan)
            )
        ).mean() * 100

        self.metrics = {

            "MAE": mae,

            "RMSE": rmse,

            "MAPE": mape,

            "R2": r2

        }

        print("Evaluación terminada.")

    # =====================================================
    # Guardar resultados
    # =====================================================

    def save_results(self):

        df = pd.DataFrame(
            [self.metrics]
        )

        file = OUTPUT / "model_metrics.csv"

        df.to_csv(
            file,
            index=False,
            encoding="utf-8-sig"
        )

        print(f"\nArchivo generado:\n{file}")

        print("\n===============")

        print("MODEL METRICS")

        print("===============")

        for k, v in self.metrics.items():

            print(f"{k}: {v:.4f}")

    # =====================================================
    # Ejecutar
    # =====================================================

    def run(self):

        self.load_model()

        self.load_dataset()

        self.prepare_dataset()

        self.evaluate()

        self.save_results()