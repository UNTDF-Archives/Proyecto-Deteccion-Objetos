#!/bin/bash
# Script wrapper para ejecutar el entrenamiento con GPU correctamente configurado

# Activar entorno virtual
source .venv/bin/activate

# Encontrar la ruta de site-packages
SITE_PACKAGES=$(python -c "import site; print(site.getsitepackages()[0])")

# Configurar LD_LIBRARY_PATH con las rutas de las librerías NVIDIA
export LD_LIBRARY_PATH="${SITE_PACKAGES}/nvidia/cuda_nvrtc/lib:${SITE_PACKAGES}/nvidia/cudnn/lib:${LD_LIBRARY_PATH}"

# Crear enlace simbólico si no existe
NVRTC_LIB_DIR="${SITE_PACKAGES}/nvidia/cuda_nvrtc/lib"
if [ -f "${NVRTC_LIB_DIR}/libnvrtc.so.11.2" ] && [ ! -f "${NVRTC_LIB_DIR}/libnvrtc.so" ]; then
    ln -s libnvrtc.so.11.2 "${NVRTC_LIB_DIR}/libnvrtc.so"
fi

# Ejecutar el script de entrenamiento
python mediapipe_quan_simple.py

