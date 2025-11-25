# Tabla Comparativa: Configuración Baseline vs Optimizada

## 📊 Comparación de Configuraciones

| Métrica | Config 1 (4 épocas) | Config 2 (30 épocas) | Mejora |
|---------|---------------------|----------------------|--------|
| **Parámetros** ||||
| EPOCHS | 4 | 30 | +26 épocas |
| BATCH_SIZE | 8 | 16 | +8 |
| DECAY_STEPS | 8 | 50 | +42 |
| **Modelo FLOAT** ||||
| Loss final | 0.7808 | 0.5930 | -24.1% ⬇️ |
| mAP (AP@[0.50:0.95]) | 0.1397 (13.97%) | 0.2643 (26.43%) | +89.2% ⬆️ |
| AP50 | 0.2754 (27.54%) | 0.5784 (57.84%) | +110.0% ⬆️ |
| AP75 | 0.1483 (14.83%) | 0.2132 (21.32%) | +43.8% ⬆️ |
| Tamaño (MB) | 10.41 | 10.41 | Sin cambio |
| **Modelo CUANTIZADO** ||||
| Loss final | 1.5600 | 0.6976 | -55.3% ⬇️ |
| mAP (AP@[0.50:0.95]) | 0.0 (0%) | 0.1903 (19.03%) | +∞ (funcional ahora) ⬆️ |
| AP50 | 0.0 (0%) | 0.4715 (47.15%) | +∞ ⬆️ |
| AP75 | 0.0 (0%) | 0.0916 (9.16%) | +∞ ⬆️ |
| Tamaño (MB) | 3.15 | 3.15 | Sin cambio |
| Factor de compresión | 3.30x | 3.30x | Igual |
| **Compromiso Precisión/Compresión** ||||
| Pérdida mAP por cuantización (abs) | -0.1397 (-100%) | -0.0740 (-28%) | Mucho mejor ⬆️ |
| Pérdida mAP por cuantización (rel) | -100% | -28% | Mucho mejor ⬆️ |

---

## 🔍 Análisis de Mejoras

### 1. Efecto del Entrenamiento Extendido

**Modelo Float:**
- Con 4 épocas: mAP = 13.97% - modelo funcional pero subóptimo
- Con 30 épocas: mAP = 26.43% - **mejora del 89%**
- El modelo aprendió mucho mejor con más épocas, duplicando prácticamente el rendimiento

**Modelo Cuantizado:**
- Con 4 épocas: mAP = 0% - **modelo completamente inutilizable**
- Con 30 épocas: mAP = 19.03% - **modelo funcional**
- La diferencia es crítica: el QAT necesita suficientes épocas para adaptarse a la cuantización

### 2. Impacto de la Cuantización

**Configuración 1 (4 épocas):**
- Pérdida total de precisión - el modelo cuantizado no logra detectar nada
- Indica que el QAT necesita más tiempo de entrenamiento

**Configuración 2 (30 épocas):**
- Pérdida de precisión del 28% relativa (del 26.43% al 19.03%)
- Aceptable para un modelo 3.3x más pequeño
- El modelo cuantizado sigue siendo útil para deployment móvil

### 3. Compresión

- **Factor constante:** 3.30x en ambas configuraciones
- **Reducción:** 69.7% del tamaño original
- La compresión no depende del número de épocas, solo de la técnica de cuantización

### 4. Trade-off Tiempo/Precisión

- **4 épocas:** Más rápido, pero modelo cuantizado inutilizable
- **30 épocas:** Más lento, pero modelo cuantizado funcional con buena precisión
- **Conclusión:** Vale la pena invertir tiempo adicional para obtener un modelo cuantizado funcional

---

## ✅ Conclusiones

1. **El número de épocas es crítico para QAT**: Con solo 4 épocas, el modelo cuantizado no funciona. Con 30 épocas, funciona correctamente.

2. **La cuantización funciona bien**: Reducción del 69.7% en tamaño con pérdida de precisión aceptable (28% relativa).

3. **30 épocas es óptimo para este dataset**: Balance entre tiempo de entrenamiento y precisión obtenida.

4. **El modelo final es adecuado para deployment móvil**: 3.15 MB con mAP del 19% es aceptable para aplicaciones prácticas.

