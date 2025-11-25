# Resultados - Configuración 1: Baseline (4 épocas)

**Fecha:** 2025-11-24
**Parámetros:**
- EPOCHS: 4
- BATCH_SIZE: 8
- LEARNING_RATE: 0.15
- DECAY_STEPS: 8
- DECAY_RATE: 0.96

---

## ⏱️ Tiempo de Entrenamiento

- **Inicio:** [Registrado en log]
- **Fin:** [Registrado en log]
- **Duración total:** [A calcular desde timestamps]

---

## 📊 Resultados Modelo FLOAT

- **Loss final de validación:** [0.7808439135551453, 0.5234692692756653, 0.004036908037960529, 0.7253146171569824]
- **Loss principal:** 0.7808
- **mAP (AP@[0.50:0.95]):** 0.1397 (13.97%)
- **AP50:** 0.2754 (27.54%)
- **AP75:** 0.1483 (14.83%)
- **Tamaño archivo:** 10.41 MB
- **Ruta:** `models/mobilenet_v2_float/model_float.tflite`

---

## 📊 Resultados Modelo CUANTIZADO (QAT)

- **Loss final de validación:** [1.5600216388702393, 1.0956612825393677, 0.009287207387387753, 1.5600216388702393]
- **Loss principal:** 1.5600
- **mAP (AP@[0.50:0.95]):** 0.0 (0%)
- **AP50:** 0.0
- **AP75:** 0.0
- **Tamaño archivo:** 3.15 MB
- **Ruta:** `models/mobilenet_v2_qat.tflite`

**Nota:** El modelo cuantizado con solo 4 épocas de QAT no logró buenos resultados. Esto indica que necesita más épocas de entrenamiento.

---

## 📈 Comparación

### Factor de Compresión
- **Tamaño float:** 10.41 MB
- **Tamaño cuantizado:** 3.15 MB
- **Factor de compresión:** 3.30x
- **Reducción:** 69.7%

### Pérdida de Precisión
- **Diferencia de Loss:** +0.7792 (cuantizado - float) - Aumento significativo
- **Diferencia de mAP:** -0.1397 (cuantizado - float) - Pérdida completa de precisión

---

## 📋 Métricas Detalladas Modelo FLOAT

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.140
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.275
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.148
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.059
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.144
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.702
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.079
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.284
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.327
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.122
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.349
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.750

Métricas dict: {
  'AP': 0.13974904, 
  'AP50': 0.27541965, 
  'AP75': 0.14828952, 
  'APs': 0.059397936, 
  'APm': 0.14368756, 
  'APl': 0.701603, 
  'ARmax1': 0.078888886, 
  'ARmax10': 0.2837037, 
  'ARmax100': 0.32740742, 
  'ARs': 0.12222222, 
  'ARm': 0.34925926, 
  'ARl': 0.75
}
```

---

## 📋 Métricas Detalladas Modelo CUANTIZADO

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.000
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.000
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.000

Métricas dict: {
  'AP': 0.0, 
  'AP50': 0.0, 
  'AP75': 0.0, 
  'APs': 0.0, 
  'APm': 0.0, 
  'APl': 0.0, 
  'ARmax1': 0.0, 
  'ARmax10': 0.0, 
  'ARmax100': 0.0, 
  'ARs': 0.0, 
  'ARm': 0.0, 
  'ARl': 0.0
}
```

---

## 📝 Observaciones

- El modelo float con 4 épocas logra un mAP modesto del 13.97% pero funcional.
- El modelo cuantizado con solo 4 épocas de QAT no logra detectar nada (mAP=0%), indicando que necesita más entrenamiento.
- La compresión funciona bien (3.3x), pero se pierde toda la precisión con tan pocas épocas.
- El modelo float funciona mejor con objetos grandes (APl=0.702) que con objetos pequeños (APs=0.059).
