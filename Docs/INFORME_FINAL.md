# Sistema de Detección de Cascos de Seguridad con IA
## Informe de Entrenamiento y Análisis de Métricas

**Materia:** Sistemas Inteligentes 2025  
**Universidad:** Universidad Nacional de Tierra del Fuego, Antártida e Islas del Atlántico Sur (UNTDF)  

**Lucas Araya** - **Constanza Benedetti**


---

## 1. Ejercicio 1: Entrenamiento y Comparación de Modelos

Ejecutamos el script `mediapipe_quan_simple.py` con el dataset **"Hard Hat Sample.v2"**, realizando dos entrenamientos comparativos para analizar el impacto de diferentes configuraciones de hiperparámetros.

### 1.1 Configuraciones Evaluadas

**Configuración 1 (Baseline):** EPOCHS=4, BATCH_SIZE=8, DECAY_STEPS=8, tiempo ~4 min  
**Configuración 2 (Optimizada):** EPOCHS=30, BATCH_SIZE=16, DECAY_STEPS=50, tiempo ~7 min

El aumento de épocas (4→30) y batch_size (8→16) permite aprovechar mejor la GPU y dar tiempo suficiente al QAT para adaptarse a la cuantización.

### 1.2 Comparación entre Configuraciones

| Métrica | 4 épocas | 30 épocas | Mejora |
|---------|---------------------|----------------------|--------|
| **Modelo FLOAT** ||||
| Loss final | 0.7808 | 0.5930 | -24.1% |
| mAP [0.50:0.95] | 13.97% | 26.43% | +89.2% |
| AP-0.50 | 27.54% | 57.84% | +110.0% |
| **Modelo CUANTIZADO** ||||
| Loss final | 1.5600 | 0.6976 | -55.3% |
| mAP [0.50:0.95] | 0% (inutilizable) | 19.03% | Funcional |
| AP-0.50 | 0% | 47.15% | Funcional |

**Análisis:** La configuración 2 muestra mejoras resultados. El modelo float casi duplica su mAP (13.97%→26.43%), mientras que el cuantizado pasa de inutilizable (0%) a funcional (19.03%). Esto confirma que el QAT requiere entrenamiento extenso para adaptarse a la reducción de precisión numérica.

### 1.3 Tabla Comparativa: Float vs Cuantizado (Configuración Optimizada)

| Métrica | Modelo Float | Modelo Cuantizado (QAT) | Diferencia |
|---------|--------------|-------------------------|------------|
| **Tamaño en disco** | 10.41 MB | 3.15 MB | -7.26 MB |
| **Factor de compresión** | - | **3.30x** | - |
| **Reducción de tamaño** | - | **69.7%** | - |
| **Loss final** | 0.5930 | 0.6976 | +0.1046 |
| **mAP [0.50:0.95]** | 26.43% | 19.03% | -7.4% |
| **AP-0.50** | 57.84% | 47.15% | -10.7% |
| **AP-0.75** | 21.32% | 9.16% | -12.2% |
| **Tiempo entrenamiento** | ~7 minutos | (incluido) | - |

### 1.4 Análisis de Resultados

**Compresión:** La cuantización reduce el modelo de 10.41 MB a 3.15 MB (factor 3.30x, reducción 69.7%), crítico para deployment móvil. El factor es consistente en ambas configuraciones, confirmando que depende solo de la técnica de cuantización.

**Pérdida de precisión:** El modelo cuantizado presenta una reducción del 28% en mAP relativa (26.43%→19.03%), aceptable considerando la reducción de tamaño. El aumento del loss (+17.6%) es consistente. Es importante destacar que con solo 4 épocas el modelo cuantizado no aprendió nada útil (mAP=0%), subrayando la importancia de un entrenamiento adecuado para QAT.

**Impacto de parámetros:** El aumento de épocas (4→30) fue crítico: mejoró el float en 89.2% y transformó el cuantizado de inutilizable a funcional. El batch_size mayor (8→16) aprovecha mejor la GPU, manteniendo el tiempo razonable (~7 min). Los decay_steps se ajustaron a 50 para que el learning rate decay ocurra cada ~4 épocas.

---

## 2. Ejercicio 2: Análisis de Métricas de Desempeño

Para el análisis detallado, utilizamos las métricas del **modelo float optimizado** (30 épocas), que presenta el mejor desempeño y permite un análisis más completo del comportamiento del modelo.

### Métricas de referencia (Modelo Float):

- **AP-[0.50:0.95]:** 0.264
- **AP-0.50:** 0.578
- **AP-0.75:** 0.213
- **AP small:** 0.232
- **AP medium:** 0.282
- **AP large:** 0.734
- **AR maxDets=1:** 0.153
- **AR maxDets=10:** 0.486
- **AR maxDets=100:** 0.488
- **AR small:** 0.300
- **AR medium:** 0.495
- **AR large:** 0.750

### 2.1 ¿Qué indica el valor de AP-[0.50:0.95] sobre el desempeño general del modelo?

El valor de **AP-[0.50:0.95] = 0.264 (26.43%)** indica un desempeño moderado pero funcional. Esta métrica promedia la precisión en múltiples umbrales de IoU (0.50 a 0.95), proporcionando una medida más estricta que AP-0.50. Significa que el modelo detecta correctamente aproximadamente uno de cada cuatro objetos, considerando clasificación y localización. Aunque no es excepcional, es suficiente para aplicaciones prácticas de seguridad laboral con supervisión humana.

### 2.2 ¿Qué diferencia observás entre AP-0.50 y AP-0.75? ¿Qué implica sobre la precisión de las cajas?

Observamos una diferencia significativa: **AP-0.50 = 57.84%** vs **AP-0.75 = 21.32%** (caída del 63% relativa). Esto indica problemas importantes con la precisión de localización. El umbral IoU 0.50 es permisivo (50% superposición), mientras que 0.75 es estricto (75% superposición). La gran diferencia sugiere que muchas cajas tienen localización aproximada pero no precisa, común en modelos optimizados para velocidad como MobileNetV2. Puede mejorarse con NMS más estricto o post-procesamiento de cajas.

### 2.3 Según las métricas AP por tamaño (small, medium, large), ¿en qué escala funciona mejor el modelo?

El modelo funciona notablemente mejor con objetos **large (APl = 73.4%)**, seguido por medium (28.2%) y small (23.2%). La diferencia es muy significativa (casi 3 veces mejor que medium). Esto tiene sentido porque: (1) objetos grandes ocupan más píxeles, proporcionando más información, (2) el modelo aprende características más distintivas en escalas mayores, y (3) MobileNetV2 tiene mejor resolución para objetos que ocupan áreas significativas (416x416). Para cascos de seguridad (tamaño medio-grande), este comportamiento es adecuado.

### 2.4 ¿Qué limitaciones del modelo se evidencian cuando analizás el AP-small?

El **AP-small = 23.2%** revela limitaciones importantes: (1) dificultades detectando objetos pequeños, posiblemente por la resolución de entrada (416x416) que no captura suficientes detalles, (2) características insuficientes para distinguir pequeños objetos en contextos complejos, y (3) MobileNetV2 prioriza eficiencia sobre detección de detalles finos. En seguridad laboral, esto limita la detección de cascos en trabajadores a distancia. Mejoras: aumentar resolución de entrada o multi-scale training.

### 2.5 ¿Cómo cambia el recall cuando se aumenta maxDets (1 → 10 → 100)? ¿Qué interpretás de esa variación?

El recall aumenta significativamente: **AR maxDets=1 = 15.3%**, **AR maxDets=10 = 48.6%**, **AR maxDets=100 = 48.8%**. La variación muestra que: (1) con 1 detección por imagen se capturan muy pocos objetos, (2) aumentar a 10 permite encontrar casi el máximo posible, y (3) permitir 100 no mejora sustancialmente, sugiriendo que el modelo genera relativamente pocas detecciones. Esto indica un comportamiento conservador: pocas detecciones pero con precisión razonable. La mejora de 1 a 10 sugiere que múltiples objetos por imagen son comunes, esperable en escenas de construcción.

### 2.6 Analizando AP y AR juntos, ¿el modelo parece tener más problemas de falsos positivos o falsos negativos?

Comparando **AP-[0.50:0.95] = 26.43%** y **AR maxDets=100 = 48.8%**, el recall es casi el doble que la precisión. Esto indica **más problemas con falsos positivos**. El modelo encuentra aproximadamente la mitad de los objetos (AR alto), pero solo una cuarta parte son correctas con umbral estricto (AP bajo). Esto sugiere que genera muchas detecciones con localización imprecisa. Mejoras: ajustar umbral de confianza o NMS más estricto.

### 2.7 ¿La diferencia entre AR-small, AR-medium y AR-large es consistente con lo observado en AP?

Sí, es consistente: **AR-small = 30.0%**, **AR-medium = 49.5%**, **AR-large = 75.0%**. Al igual que en AP, los objetos large tienen mejor desempeño. Esta consistencia confirma que la escala es un factor determinante. Sin embargo, las diferencias relativas en AR son menores que en AP (AR-large es 2.5x mejor que AR-small, mientras AP-large es 3.2x mejor), sugiriendo que el modelo puede encontrar objetos pequeños con cierta frecuencia, pero tiene más dificultades para localizarlos precisamente.

### 2.8 ¿El modelo parece generar muchas detecciones irrelevantes? ¿Qué evidencia del reporte te lleva a esa conclusión?

El modelo **no genera excesivas detecciones irrelevantes**. Evidencia: (1) el recall con maxDets=100 (48.8%) no es mucho mayor que con maxDets=10 (48.6%), indicando pocas detecciones totales, (2) el gap entre AP-0.50 (57.84%) y AP-[0.50:0.95] (26.43%) sugiere que el problema principal es localización imprecisa más que detecciones erróneas, y (3) comportamiento conservador (AP y AR moderados). Si generara muchas detecciones irrelevantes, esperaríamos recall muy alto pero precisión muy baja, lo cual no observamos. El problema principal es precisión de localización, no falsos positivos masivos.

### 2.9 ¿Qué tipo de error identificás como más crítico en este modelo: mala localización, falta de detecciones o exceso de detecciones?

El error más crítico es **mala localización**. Evidencia: (1) gran diferencia entre AP-0.50 (57.84%) y AP-0.75 (21.32%) muestra cajas con superposición parcial pero imprecisa, (2) recall razonable (48.8%), no falla masivamente en encontrar objetos, (3) no hay exceso de detecciones (recall se satura con 10), y (4) el modelo genera cajas cerca de objetos correctos pero no suficientemente precisas para umbrales de IoU altos. Aunque encuentra objetos, las cajas imprecisas pueden no ser útiles para aplicaciones que requieren localización exacta. Mejoras: refinamiento de cajas, anchors mejor calibrados, o aumento de resolución de entrada.

### 2.10 A partir del análisis general, ¿qué mejoras concretas propondrías para optimizar el modelo?

Proponemos las siguientes mejoras:

1. **Mejorar precisión de localización:** Refinamiento de cajas, NMS más estricto, y aumentar resolución de entrada a 640x640.

2. **Aumentar resolución para objetos pequeños:** Multi-scale training o mayor resolución de entrada para mejorar AP-small (23.2%).

3. **Ajustar umbrales de confianza:** Optimizar umbral de confianza y NMS para balancear precisión y recall.

4. **Data augmentation específica:** Más ejemplos de objetos pequeños y diversas condiciones de iluminación y ángulos.

5. **Fine-tuning post-cuantización:** Fine-tuning adicional del modelo cuantizado con learning rate bajo para recuperar precisión.

6. **Ensemble de modelos:** Combinar predicciones del modelo float y cuantizado cuando la latencia lo permita.

---

## Conclusiones

El entrenamiento demostró que la cuantización logra una compresión exitosa (3.30x, reducción del 69.7%) con una pérdida de precisión aceptable (28% relativa). El modelo cuantizado final (3.15 MB, mAP 19.03%) es adecuado para deployment móvil. El análisis de métricas reveló que el principal desafío es la precisión de localización de cajas delimitadoras, especialmente para objetos pequeños, mientras que el modelo muestra un comportamiento conservador con relativamente pocos falsos positivos. Las mejoras propuestas se enfocan en refinar la localización y mejorar el desempeño en escalas pequeñas.
