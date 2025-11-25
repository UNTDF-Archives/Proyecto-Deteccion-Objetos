# Resultados - Configuración 2: Optimizada (30 épocas)

**Fecha:** 2025-11-24
**Parámetros:**
- EPOCHS: 30
- BATCH_SIZE: 16
- LEARNING_RATE: 0.15
- DECAY_STEPS: 50
- DECAY_RATE: 0.96

---

## ⏱️ Tiempo de Entrenamiento

- **Inicio:** [Registrado en log]
- **Fin:** [Registrado en log]
- **Duración total:** [A calcular desde timestamps]

---

## 📊 Resultados Modelo FLOAT

- **Loss final de validación:** [0.5930466055870056, 0.33203357458114624, 0.004120912868529558, 0.5380792617797852]
- **Loss principal:** 0.5930
- **mAP (AP@[0.50:0.95]):** 0.2643 (26.43%)
- **AP50:** 0.5784 (57.84%)
- **AP75:** 0.2132 (21.32%)
- **Tamaño archivo:** 10.41 MB
- **Ruta:** `models/mobilenet_v2_float/model_float.tflite`

---

## 📊 Resultados Modelo CUANTIZADO (QAT)

- **Loss final de validación:** [0.6976369619369507, 0.40550175309181213, 0.005842702463269234, 0.6976369619369507]
- **Loss principal:** 0.6976
- **mAP (AP@[0.50:0.95]):** 0.1903 (19.03%)
- **AP50:** 0.4715 (47.15%)
- **AP75:** 0.0916 (9.16%)
- **Tamaño archivo:** 3.15 MB
- **Ruta:** `models/mobilenet_v2_qat.tflite`

---

## 📈 Comparación

### Factor de Compresión
- **Tamaño float:** 10.41 MB
- **Tamaño cuantizado:** 3.15 MB
- **Factor de compresión:** 3.30x
- **Reducción:** 69.7%

### Pérdida de Precisión
- **Diferencia de Loss:** +0.1046 (cuantizado - float) - Aumento moderado
- **Diferencia de mAP:** -0.0740 (cuantizado - float) - Pérdida del 28% relativa

---

## 📋 Métricas Detalladas Modelo FLOAT

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.264
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.578
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.213
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.232
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.282
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.734
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.153
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.486
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.488
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.300
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.495
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.750

Métricas dict: {
  'AP': 0.26435295, 
  'AP50': 0.57841367, 
  'AP75': 0.21322618, 
  'APs': 0.23201396, 
  'APm': 0.28200442, 
  'APl': 0.7336634, 
  'ARmax1': 0.1525926, 
  'ARmax10': 0.4862963, 
  'ARmax100': 0.48814815, 
  'ARs': 0.3, 
  'ARm': 0.4948148, 
  'ARl': 0.75
}
```

---

## 📋 Métricas Detalladas Modelo CUANTIZADO

```
Average Precision  (AP) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.190
Average Precision  (AP) @[ IoU=0.50      | area=   all | maxDets=100 ] = 0.472
Average Precision  (AP) @[ IoU=0.75      | area=   all | maxDets=100 ] = 0.092
Average Precision  (AP) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.159
Average Precision  (AP) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.197
Average Precision  (AP) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.583
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=  1 ] = 0.083
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets= 10 ] = 0.232
Average Recall     (AR) @[ IoU=0.50:0.95 | area=   all | maxDets=100 ] = 0.236
Average Recall     (AR) @[ IoU=0.50:0.95 | area= small | maxDets=100 ] = 0.156
Average Recall     (AR) @[ IoU=0.50:0.95 | area=medium | maxDets=100 ] = 0.245
Average Recall     (AR) @[ IoU=0.50:0.95 | area= large | maxDets=100 ] = 0.633

Métricas dict: {
  'AP': 0.19037212, 
  'AP50': 0.47153893, 
  'AP75': 0.091584936, 
  'APs': 0.15940595, 
  'APm': 0.19669133, 
  'APl': 0.5831683, 
  'ARmax1': 0.08259259, 
  'ARmax10': 0.23222223, 
  'ARmax100': 0.23592593, 
  'ARs': 0.15555556, 
  'ARm': 0.24518518, 
  'ARl': 0.6333333
}
```

---

## 📝 Observaciones

- ✅ El modelo float con 30 épocas logra un mAP del 26.43%, casi el doble que con 4 épocas (13.97%).
- ✅ El modelo cuantizado con 30 épocas de QAT ahora funciona correctamente (mAP=19.03%), comparado con 0% con solo 4 épocas.
- ✅ La compresión sigue siendo excelente (3.3x), reduciendo el tamaño en un 69.7%.
- ✅ La pérdida de precisión por cuantización es aceptable: del 26.43% al 19.03% (reducción del 28% relativa).
- ✅ El modelo funciona mejor con objetos grandes (APl=0.734 float, 0.583 cuantizado) que con objetos pequeños.
- ✅ La mejora de 4 a 30 épocas es muy significativa tanto para float como para cuantizado.
