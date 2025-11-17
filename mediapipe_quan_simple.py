import os
import shutil
import sys

# Configurar LD_LIBRARY_PATH y crear enlaces simbólicos ANTES de importar TensorFlow
# Esto es necesario para que libnvrtc.so sea encontrado por TensorFlow
site_packages = [p for p in sys.path if 'site-packages' in p]
if site_packages:
    # Crear enlace simbólico para libnvrtc.so si no existe
    nvrtc_lib_dir = os.path.join(site_packages[0], 'nvidia', 'cuda_nvrtc', 'lib')
    nvrtc_so = os.path.join(nvrtc_lib_dir, 'libnvrtc.so.11.2')
    nvrtc_link = os.path.join(nvrtc_lib_dir, 'libnvrtc.so')
    if os.path.exists(nvrtc_so) and not os.path.exists(nvrtc_link):
        try:
            os.symlink('libnvrtc.so.11.2', nvrtc_link)
        except OSError:
            pass  # El enlace ya existe o no se pudo crear
    
    # Configurar LD_LIBRARY_PATH
    nvidia_lib_paths = [
        os.path.join(site_packages[0], 'nvidia', 'cuda_nvrtc', 'lib'),
        os.path.join(site_packages[0], 'nvidia', 'cudnn', 'lib'),
    ]
    existing_paths = os.environ.get('LD_LIBRARY_PATH', '').split(':')
    new_paths = [p for p in nvidia_lib_paths if os.path.exists(p) and p not in existing_paths]
    if new_paths:
        current_ld_path = os.environ.get('LD_LIBRARY_PATH', '')
        os.environ['LD_LIBRARY_PATH'] = ':'.join(new_paths + ([current_ld_path] if current_ld_path else []))

from mediapipe_model_maker import object_detector
from mediapipe_model_maker.python.vision.object_detector import model_spec as ms

# Configuración de TensorFlow para evitar problemas con cuDNN
# Si hay problemas con GPU (error de libnvrtc.so o cuDNN), descomenta la siguiente línea:
# os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # Esto fuerza el uso de CPU

try:
    import tensorflow as tf
    # Configurar TensorFlow para usar memoria GPU de forma dinámica
    gpus = tf.config.experimental.list_physical_devices('GPU')
    if gpus:
        try:
            for gpu in gpus:
                tf.config.experimental.set_memory_growth(gpu, True)
            print(f"GPU configurada: {len(gpus)} dispositivo(s) disponible(s)")
        except RuntimeError as e:
            print(f"Error al configurar GPU: {e}")
            print("Continuando con CPU...")
    else:
        print("No se detectó GPU, usando CPU")
except Exception as e:
    print(f"Advertencia al configurar TensorFlow: {e}")
    print("Continuando...")

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
EPOCHS = 4

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
BATCH_SIZE = 8

# DECAY_STEPS: Cada cuántos pasos (batches) se reduce el learning rate
# - Se usa con DECAY_RATE para implementar "learning rate decay"
# - 8 pasos significa que cada 8 batches se aplicará la reducción
# - Ayuda a que el modelo haga ajustes más finos conforme avanza el entrenamiento
DECAY_STEPS = 8

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