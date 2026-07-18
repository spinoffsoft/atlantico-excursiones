# ZEUS AI - Predicción de demanda para excursiones turísticas

## Descripción

Este repositorio contiene el código fuente desarrollado como parte del Trabajo Fin de Máster (TFM) titulado:

**Sistema de predicción de demanda mediante Inteligencia Artificial para la planificación operativa de excursiones turísticas.**

El objetivo del proyecto es desarrollar un sistema capaz de predecir la demanda diaria de excursiones utilizando técnicas de Machine Learning, proporcionando una herramienta de apoyo para la planificación operativa basada en datos históricos.

---

## Tecnologías utilizadas

- Python 3.11
- Pandas
- NumPy
- Scikit-Learn
- XGBoost
- LightGBM
- CatBoost
- Matplotlib
- Statsmodels
- MySQL

---

## Instalación

Clonar el repositorio:

```bash
git clone https://github.com/spinoffsoft/atlantico-excursiones.git
```

Instalar las dependencias:

```bash
pip install -r requirements.txt
```

---

## Estructura del proyecto

```
src/
│
├── extract_zeus.py           # Extracción de datos desde ZEUS
├── preprocess.py             # Preparación y limpieza de datos
├── train_models.py           # Entrenamiento de modelos
├── predict.py                # Generación de predicciones
├── forecasting_engine.py     # Motor de predicción
├── model_evaluation.py       # Evaluación de modelos
├── business_metrics.py       # Métricas de negocio
├── excursions.py             # Configuración de excursiones
├── plots_pro.py              # Generación de gráficos
├── config.py                 # Configuración del proyecto
└── main.py                   # Punto de entrada
```

---

## Flujo de ejecución

1. Extraer los datos desde ZEUS.
2. Preparar el conjunto de datos.
3. Entrenar los modelos.
4. Seleccionar el mejor modelo.
5. Generar las predicciones.
6. Evaluar los resultados.

---

## Datos

Los datos utilizados proceden del sistema de reservas **ZEUS**, propiedad de **Atlántico Excursiones**.

Por motivos de confidencialidad y protección de la información comercial de la empresa, el conjunto de datos original no puede hacerse público.

El repositorio contiene únicamente el código fuente desarrollado para el TFM.

---

## Modelo entrenado

El modelo puede generarse ejecutando:

```bash
python src/train_models.py
```

---

## Reproducibilidad

El proyecto puede reproducirse utilizando un conjunto de datos con la misma estructura que la descrita en la memoria del TFM.

---

## Versión

Versión correspondiente al Trabajo Fin de Máster.

Versión: **v1.0-TFM**

---

## Autor

Michael Cohen

Máster Universitario en Inteligencia Artificial

2026
