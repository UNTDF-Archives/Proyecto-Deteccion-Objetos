"""
Script de entrenamiento para detección de objetos con MediaPipe Model Maker.

IMPORTANTE: Para ejecutar con GPU, usa el script wrapper:
    ./run_training.sh

El wrapper configura LD_LIBRARY_PATH correctamente antes de iniciar Python.
Si ejecutas directamente con 'python mediapipe_quan_simple.py', puede fallar con GPU.
"""

from mediapipe_model_maker import object_detector
from mediapipe_model_maker.python.vision.object_detector import model_spec as ms
import os
import shutil


# Obtener el directorio base del proyecto (donde está este script)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths relativos al directorio del proyecto
DATASET_DIR = os.path.join(BASE_DIR, "Hard Hat Sample.v2-augmented-416x416.voc")
CACHE_DIR = os.path.join(BASE_DIR, "Hard Hat Sample.v2-augmented-416x416.voc", "cache")
MODEL_PATH = os.path.join(BASE_DIR, "models", "mobilenet_v2_float")
MODEL_QUAN_PATH = os.path.join(BASE_DIR, "models", "mobilenet_v2_qat.tflite")

#============================================================================
# HIPERPARÁMETROS DE ENTRENAMIENTO
# ============================================================================

# EPOCHS: Número de veces que el modelo verá todo el dataset completo
# - Valores típicos: 20-100 para object detection
# - Más épocas = mejor aprendizaje, pero riesgo de overfitting
# - 30 épocas es un buen balance para datasets medianos
EPOCHS = 30

# LEARNING_RATE: Tasa de aprendizaje - controla qué tan grandes son los ajustes de pesos
# - Valores típicos: 0.001 - 0.3 para object detection
# - Muy alto (>0.5): el modelo no converge, loss oscila
# - Muy bajo (<0.001): entrenamiento muy lento
# - 0.15 es agresivo pero efectivo para QAT (Quantization Aware Training)
LEARNING_RATE = 0.15

# BATCH_SIZE: Número de imágenes procesadas simultáneamente antes de actualizar pesos
# - Valores típicos: 4-32 dependiendo de memoria GPU/CPU
# - Más alto: entrenamiento más rápido pero requiere más memoria
# - Más bajo: más estable pero más lento
# - 8 es ideal para GPUs con memoria limitada (4-8GB) o CPUs
BATCH_SIZE = 16

# DECAY_STEPS: Cada cuántos pasos (batches) se reduce el learning rate
# - Se usa con DECAY_RATE para implementar "learning rate decay"
# - 8 pasos significa que cada 8 batches se aplicará la reducción
# - Ayuda a que el modelo haga ajustes más finos conforme avanza el entrenamiento
DECAY_STEPS = 50

# DECAY_RATE: Factor de multiplicación para reducir el learning rate
# - Nuevo LR = LR actual × DECAY_RATE
# - 0.96 significa reducción del 4% cada DECAY_STEPS
# - Valores típicos: 0.9-0.99
# - Permite convergencia más suave: ajustes grandes al inicio, finos al final
DECAY_RATE = 0.96

def ensure_cache_structure(cache_dir):
    """Crea la estructura de cache que MediaPipe necesita."""
    if os.path.exists(cache_dir):
        shutil.rmtree(cache_dir)

    os.makedirs(os.path.join(cache_dir, "train"), exist_ok=True)
    os.makedirs(os.path.join(cache_dir, "valid"), exist_ok=True)


def main():
    train_dir = os.path.join(DATASET_DIR, "train")
    val_dir = os.path.join(DATASET_DIR, "valid")

    print("Creando estructura de cache...")
    ensure_cache_structure(CACHE_DIR)

    print("Cargando dataset...")
    train_data = object_detector.Dataset.from_pascal_voc_folder(
        data_dir=train_dir,
        cache_dir=os.path.join(CACHE_DIR, "train")
    )
    val_data = object_detector.Dataset.from_pascal_voc_folder(
        data_dir=val_dir,
        cache_dir=os.path.join(CACHE_DIR, "valid")
    )

    print(f"Train dataset cargado")
    print(f"Val dataset cargado")
    print(f"Clases: {train_data.label_names}")

    spec = ms.SupportedModels.MOBILENET_V2

    # Crear directorio para el modelo si no existe
    os.makedirs(MODEL_PATH, exist_ok=True)

    hparams = object_detector.HParams(
        export_dir=MODEL_PATH,
        epochs=EPOCHS
    )

    options = object_detector.ObjectDetectorOptions(
        supported_model=spec,
        hparams=hparams
    )
    options.model_options = object_detector.ModelOptions(l2_weight_decay=3e-05)

    print("\n=== PASO 1: Entrenando modelo FLOAT ===")
    model = object_detector.ObjectDetector.create(
        train_data=train_data,
        validation_data=val_data,
        options=options
    )

    print("\nEvaluando modelo float...")
    loss, metrics = model.evaluate(val_data)
    print("Float model - Loss: ", loss)
    print("Métricas:", metrics)

    # Si metrics es un diccionario o lista con estructura conocida
    if isinstance(metrics, dict):
        for key, value in metrics.items():
            print(f"  {key}: {value:.4f}" if isinstance(value, float) else f"  {key}: {value}")
    elif isinstance(metrics, list) and len(metrics) > 0:
        print(f"  mAP: {metrics[0]:.4f}" if isinstance(metrics[0], (int, float)) else f"  Métricas: {metrics}")

    # Exportar modelo float
    float_model_path = MODEL_PATH + "/model_float.tflite"
    model.export_model(float_model_path)
    print(f"Modelo float exportado: {float_model_path}")

    print("\n=== PASO 2: Quantization Aware Training ===")
    qat_hparams = object_detector.QATHParams(
        learning_rate=LEARNING_RATE,
        batch_size=BATCH_SIZE,
        epochs=EPOCHS,
        decay_steps=DECAY_STEPS,
        decay_rate=DECAY_RATE
    )

    print("Restaurando checkpoint float...")
    model.restore_float_ckpt()

    print("Iniciando QAT...")
    model.quantization_aware_training(train_data, val_data, qat_hparams=qat_hparams)

    print("\nEvaluando modelo cuantizado...")
    loss, metrics = model.evaluate(val_data)
    print("QAT model - Loss: ", loss)
    print("Métricas:", metrics)

    print(f"\nExportando modelo cuantizado: {MODEL_QUAN_PATH}")
    model.export_model(MODEL_QUAN_PATH)
    print("¡Entrenamiento completo!")
    print(f"\nResumen:")
    print(f"- Modelo float: {float_model_path}")
    print(f"- Modelo cuantizado: {MODEL_QUAN_PATH}")


if __name__ == "__main__":
    main()