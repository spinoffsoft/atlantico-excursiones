# 🧠 Sistema de Predicción de Demanda - ZEUS

Este proyecto implementa un sistema de predicción de demanda para excursiones turísticas en Tenerife, integrado con el sistema ZEUS de Atlántico Excursiones.

El objetivo principal es anticipar la demanda diaria de cada excursión para optimizar la planificación de recursos, especialmente la asignación de autobuses.

---

## 🚀 Funcionalidades

* 📊 Predicción de demanda diaria por excursión
* 🤖 Uso de modelos de Machine Learning (Random Forest, XGBoost, etc.)
* 📅 Incorporación de variables temporales (día de la semana, mes)
* 📈 Uso de variables históricas (lags y medias móviles)
* 🔗 Integración con sistema ZEUS (PHP + Python)

---

## 📂 Estructura del proyecto

```text
src/
├── extract_zeus.py      # Extracción de datos desde MySQL
├── preprocess.py        # Limpieza y generación de variables
├── train_models.py      # Entrenamiento y evaluación de modelos
├── predict.py           # Predicción diaria
```

---

## 🔄 Pipeline del sistema

1. **Extracción de datos**

   * Se obtienen las reservas desde la base de datos ZEUS

2. **Preprocesamiento**

   * Limpieza de datos
   * Generación de variables temporales
   * Creación de lags y medias móviles

3. **Entrenamiento**

   * Evaluación de múltiples modelos
   * Selección del mejor modelo (Random Forest)

4. **Predicción**

   * Estimación de demanda para el día siguiente
   * Integración con el sistema ZEUS

---

## 🤖 Modelo utilizado

El modelo seleccionado ha sido **Random Forest**, debido a:

* Mejor rendimiento en MAE
* Mayor robustez frente a ruido
* Mejor generalización en datos reales

---

## 📊 Resultados

* MAE ≈ 5.7 personas
* R² ≈ 0.76
* Error en picos ≈ 16 personas

Estos resultados se consideran adecuados para su uso en un entorno real de negocio.

---

## ⚙️ Tecnologías utilizadas

* Python
* Pandas / NumPy
* Scikit-learn
* XGBoost / LightGBM / CatBoost
* MySQL
* PHP (integración con ZEUS)

---

## ▶️ Uso

1. Entrenar modelo:

```bash
python train_models.py
```

2. Generar predicción:

```bash
python predict.py
```

---

## 📌 Notas

* Los datos históricos y modelos entrenados no se incluyen en el repositorio por motivos de privacidad y tamaño.
* El sistema está diseñado para su integración en producción con ZEUS.

---

## 👨‍💻 Autor

Proyecto desarrollado como Trabajo Fin de Máster (TFM) en Ingeniería de Software / Inteligencia Artificial.

---

## 📈 Futuras mejoras

* Predicción por intervalos horarios
* Incorporación de variables externas (clima, eventos)
* Optimización automática de recursos (buses)
* Dashboard de visualización en tiempo real

---
