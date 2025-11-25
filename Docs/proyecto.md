### SISTEMAS INTELIGENTES 2025
**Universidad Nacional de Tierra del Fuego, Antártida e Islas del Atlántico Sur (UNTDF)**
**IDEI - Instituto de Desarrollo Económico e Innovación**

### Proyecto: Sistema de Detección de Cascos de Seguridad con IA

#### Introducción

**El Problema: Seguridad Laboral en Construcción**
Los accidentes laborales por falta de equipo de protección personal (EPP) representan un problema crítico en la industria de la construcción. Según estadísticas internacionales, los traumatismos craneoencefálicos son una de las principales causas de lesiones graves y muertes en obras. El uso obligatorio de cascos de seguridad puede prevenir hasta el 85% de estas lesiones.

**Desafíos actuales:**
* La supervisión manual es costosa y no escalable.
* Es difícil monitorear zonas extensas simultáneamente.
* Los sistemas tradicionales requieren infraestructura de red.
* Las soluciones basadas en la nube tienen problemas de latencia y privacidad.

**Solución propuesta:**
Un sistema de detección automatizada basado en IA que puede ejecutarse directamente en dispositivos móviles, permitiendo:
* Monitoreo en tiempo real sin conexión a internet.
* Bajo costo (usa hardware existente).
* Privacidad de datos (procesamiento local).
* Alertas inmediatas ante infracciones.

---

#### Detección de Objetos: Dos Tareas en Una
La detección de objetos es una tarea fundamental en visión por computadora que consiste en identificar y localizar múltiples objetos dentro de una imagen. A diferencia de la clasificación simple, un detector debe resolver dos problemas simultáneamente:

1.  **¿Qué objetos están presentes?** (clasificación - tarea discreta).
2.  **¿Dónde están ubicados?** (regresión - tarea continua).

La localización es efectivamente un problema de regresión donde el modelo debe predecir 4 valores continuos por cada objeto. En el formato PASCAL VOC (usado en este proyecto), estos valores son:
* $(x_{min}, y_{min})$: coordenadas de la esquina superior izquierda.
* $(x_{max}, y_{max})$: coordenadas de la esquina inferior derecha.

El modelo aprende a "ajustar" estos valores numéricos para minimizar el error entre las cajas predichas y las cajas reales (ground truth), típicamente usando funciones de pérdida como Smooth L1 Loss o IoU Loss.

Esta tarea tiene aplicaciones críticas en múltiples dominios:
* **Seguridad laboral:** Detección de EPP (cascos, chalecos, arneses) en obras.
* **Vehículos autónomos:** Identificación de peatones, señales y otros vehículos.
* **Vigilancia inteligente:** Monitoreo de actividades y objetos de interés.
* **Retail:** Conteo de productos y análisis de inventario.

En este proyecto nos enfocamos específicamente en la detección de cascos de seguridad usando el dataset "Hard Hat Detection", que contiene imágenes reales de trabajadores en ambientes de construcción con y sin cascos.

---

#### El Desafío del Deployment en Celulares
Para que este sistema sea práctico en obra, debe ejecutarse en smartphones comunes (no servidores ni equipos especializados). Esto presenta desafíos técnicos significativos:

**Limitaciones de hardware móvil:**
* **CPU limitada:** procesadores ARM con menos FLOPS que GPUs de escritorio.
* **Batería:** el procesamiento intensivo drena la batería rápidamente.
* **Memoria RAM:** típicamente 4-8 GB (vs 16-64 GB en laptops).
* **Almacenamiento:** apps móviles deben ser <100 MB idealmente.

**Requisitos para deployment móvil:**
* Inferencia en <100ms para video en tiempo real (10+ FPS).
* Consumo energético bajo para operación continua.
* Modelo pequeño (<10 MB) para descarga rápida.
* Compatible con TensorFlow Lite (runtime móvil).

#### ¿Qué es la Cuantización?
La cuantización es una técnica de compresión de modelos que reduce la precisión numérica de los pesos y activaciones de una red neuronal. En lugar de usar números de punto flotante de 32 bits (float32), se utilizan enteros de 8 bits (int8).

**Ventajas de la cuantización:**
* **Tamaño reducido:** Modelos hasta 4x más pequeños.
* **Inferencia más rápida:** Operaciones enteras son más eficientes.
* **Menor consumo energético:** Crucial para dispositivos móviles.
* Compatible con hardware especializado: TPUs, NPUs optimizados para int8.

**Desventaja:**
* **Pérdida de precisión:** La reducción numérica puede afectar el rendimiento.

**Quantization-Aware Training (QAT)**
El código proporcionado implementa QAT, una técnica avanzada donde:
1.  El modelo se entrena simulando la cuantización durante el proceso.
2.  Los pesos aprenden a ser "robustos" ante la pérdida de precisión.
3.  El resultado es un modelo cuantizado con mínima degradación de precisión.

Alternativa: Post-Training Quantization (PTQ) cuantiza después del entrenamiento, pero suele perder más precisión.

#### ¿Por qué MobileNetV2?
El proyecto usa MobileNetV2 como arquitectura base porque fue diseñada específicamente para dispositivos móviles.

**Características clave:**
* **Inverted Residuals:** estructura eficiente que reduce operaciones.
* **Linear Bottlenecks:** preserva información con menos parámetros.
* **Depthwise Separable Convolutions:** reduce cómputo hasta 9x.
* **Trade-off configurable:** balance entre precisión y velocidad.

MobileNetV2 es ideal para este proyecto porque logra buen rendimiento (~70-80% mAP) con solo 3.5M parámetros, vs modelos más grandes como ResNet50 (25M parámetros) o EfficientDet (varios tamaños).

#### Dataset: Hard Hat Detection
* **Contenido:** Imágenes de trabajadores en obras de construcción.
* **Formato:** PASCAL VOC (XML annotations).
* **Clases:** `['background', 'head', 'helmet', 'person']`.
* Dataset aumentado para mejorar generalización.

---

### Ejercicios

**Objetivo:** Comprender el pipeline de entrenamiento con cuantización.
Entregar un informe (máx 5 pág.) con la resolución de los siguientes ejercicios:

**Ejercicio 1.** Ejecutar `mediapipe_quan_simple.py` con el dataset proporcionado y registrar el tiempo total de entrenamiento y confeccionar en una tabla resumen comparando los modelos (original float y el cuantizado):
* Comparar tamaño en disco (MB): modelo float vs cuantizado.
* Calcular el factor de compresión: $tamaño\_float / tamaño\_cuantizado$.
* Registrar el loss final de validación.
* Tiempo de entrenamiento, Loss y mAP finales reportados.

**Ejercicio 2.** En base a los resultados obtenidos y a partir del reporte de métricas (AP, AR, IoU y escalas), responder a las siguientes preguntas para analizar el desempeño de un modelo de detección de objetos:

* **2.1.** ¿Qué indica el valor de AP@[0.50:0.95] sobre el desempeño general del modelo?
* **2.2.** ¿Qué diferencia observás entre AP@0.50 y AP@0.75? ¿Qué implica sobre la precisión de las cajas?
* **2.3.** Según las métricas AP por tamaño (small, medium, large), ¿en qué escala funciona mejor el modelo?
* **2.4.** ¿Qué limitaciones del modelo se evidencian cuando analizás el AP-small?
* **2.5.** ¿Cómo cambia el recall cuando se aumenta maxDets $(1 \rightarrow 10 \rightarrow 100)$? ¿Qué interpretás de esa variación?
* **2.6.** Analizando AP y AR juntos, ¿el modelo parece tener más problemas de falsos positivos o falsos negativos?
* **2.7.** ¿La diferencia entre AR-small, AR-medium y AR-large es consistente con lo observado en AP? Explicá brevemente.
* **2.8.** ¿El modelo parece generar muchas detecciones irrelevantes? ¿Qué evidencia del reporte te lleva a esa conclusión?
* **2.9.** ¿Qué tipo de error identificás como más crítico en este modelo: mala localización, falta de detecciones o exceso de detecciones?
* **2.10.** A partir del análisis general, ¿qué mejoras concretas propondrías para optimizar el modelo?

---

### Referencias
* Padilla, R., Netto, S. L., & da Silva, E. A. (2020). "A Survey on Performance Metrics for Object-Detection Algorithms." International Conference on Systems, Signals and Image Processing (IWSSIP).