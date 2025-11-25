# 📊 Resumen de Resultados - Entrenamientos Completados

## ✅ Entrenamientos Ejecutados

Se ejecutaron **DOS entrenamientos** con diferentes configuraciones para comparar resultados:

### Configuración 1: Baseline (4 épocas)
- **Fecha:** 2025-11-24
- **Parámetros:** EPOCHS=4, BATCH_SIZE=8, DECAY_STEPS=8
- **Duración:** ~4 minutos
- **Log:** `Docs/output_config1_baseline.log`

### Configuración 2: Optimizada (30 épocas)
- **Fecha:** 2025-11-24  
- **Parámetros:** EPOCHS=30, BATCH_SIZE=16, DECAY_STEPS=50
- **Duración:** ~7 minutos
- **Log:** `Docs/output_config2_optimizada.log`

---

## 🎯 Resultados Principales

### Tabla Comparativa Resumida

| Métrica | Config 1 (4 épocas) | Config 2 (30 épocas) |
|---------|---------------------|----------------------|
| **Float - Loss** | 0.7808 | 0.5930 |
| **Float - mAP** | 13.97% | **26.43%** ⬆️ |
| **Float - AP50** | 27.54% | **57.84%** ⬆️ |
| **Cuantizado - Loss** | 1.5600 | 0.6976 |
| **Cuantizado - mAP** | **0%** ❌ | **19.03%** ✅ |
| **Cuantizado - AP50** | 0% | **47.15%** ✅ |
| **Tamaño Float** | 10.41 MB | 10.41 MB |
| **Tamaño Cuantizado** | 3.15 MB | 3.15 MB |
| **Factor Compresión** | 3.30x | 3.30x |

---

## 📈 Hallazgos Clave

### 1. Efecto del Número de Épocas

- **Modelo Float:**
  - 4 épocas: mAP = 13.97% (funcional pero limitado)
  - 30 épocas: mAP = 26.43% (**mejora del 89%**)

- **Modelo Cuantizado:**
  - 4 épocas: mAP = 0% (**totalmente inutilizable**)
  - 30 épocas: mAP = 19.03% (**funcional y útil**)

**Conclusión:** El QAT requiere suficientes épocas para adaptarse. Con solo 4 épocas, el modelo no aprendió a manejar la cuantización.

### 2. Efectividad de la Cuantización

**Con 30 épocas (configuración óptima):**
- **Compresión:** 3.30x (de 10.41 MB a 3.15 MB)
- **Reducción de tamaño:** 69.7%
- **Pérdida de precisión:** 28% relativa (del 26.43% al 19.03%)
- **Trade-off:** Aceptable para deployment móvil

### 3. Comparación entre Configuraciones

| Aspecto | Config 1 | Config 2 | Ganador |
|---------|----------|----------|---------|
| **Tiempo entrenamiento** | Más rápido (~4 min) | Más lento (~7 min) | Config 1 |
| **Precisión Float** | 13.97% | 26.43% | **Config 2** ✅ |
| **Precisión Cuantizado** | 0% (inutilizable) | 19.03% (funcional) | **Config 2** ✅ |
| **Compresión** | 3.30x | 3.30x | Igual |
| **Utilidad práctica** | Baja (cuantizado no funciona) | Alta (ambos funcionales) | **Config 2** ✅ |

**Conclusión:** La configuración 2 (30 épocas) es claramente superior. El tiempo adicional invertido vale completamente la pena porque:
- El modelo float es casi el doble de preciso
- El modelo cuantizado pasa de inutilizable a funcional
- El modelo cuantizado es adecuado para deployment móvil (3.15 MB, 19% mAP)

---

## 📁 Archivos Generados

1. **Logs de entrenamiento:**
   - `Docs/output_config1_baseline.log` - Log completo config 1
   - `Docs/output_config2_optimizada.log` - Log completo config 2

2. **Resultados detallados:**
   - `Docs/resultados_config1_baseline.md` - Análisis detallado config 1
   - `Docs/resultados_config2_optimizada.md` - Análisis detallado config 2

3. **Comparación:**
   - `Docs/TABLA_COMPARATIVA.md` - Tabla comparativa completa

4. **Modelos generados:**
   - `models/mobilenet_v2_float/model_float.tflite` - Modelo float (10.41 MB)
   - `models/mobilenet_v2_qat.tflite` - Modelo cuantizado (3.15 MB)

---

## 🎓 Próximos Pasos

Con estos resultados, podemos:
1. ✅ Completar el **Ejercicio 1** - Tabla comparativa con todos los datos
2. ✅ Responder el **Ejercicio 2** - Analizar las métricas detalladas del modelo optimizado
3. ✅ Redactar el informe final (máx. 5 páginas, en plural)

---

## 💡 Recomendación Final

**Usar la Configuración 2 (30 épocas) para el informe** porque:
- Tiene datos completos y funcionales para ambos modelos
- El modelo cuantizado funciona correctamente
- Las métricas son más representativas del desempeño real
- Permite un análisis más completo para el Ejercicio 2

Los datos de la Configuración 1 pueden usarse para mostrar el impacto de entrenar más épocas en la comparación.

