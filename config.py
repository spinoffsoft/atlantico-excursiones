from pathlib import Path

# ======================================
# Directorios
# ======================================

BASE_DIR = Path(__file__).parent

DATASET = BASE_DIR / "dataset_forecasting.csv"

MODEL = BASE_DIR / "best_model.pkl"

OUTPUT = BASE_DIR / "output"

FIGURES = OUTPUT / "figures"

LOGS = BASE_DIR / "logs"

# Crear carpetas automáticamente
OUTPUT.mkdir(exist_ok=True)
FIGURES.mkdir(exist_ok=True)
LOGS.mkdir(exist_ok=True)

# ======================================
# Variables del modelo
# ======================================

TARGET = "demand"

# ======================================
# Horizonte de evaluación
# ======================================

START_DATE = "2025-01-01"

END_DATE = "2026-06-01"

# ======================================
# Configuración autobuses
# ======================================

BUS_CAPACITY = 20