#!/bin/bash
# Script para calcular el tamaño de los modelos generados

echo "=== Tamaños de Modelos ==="
echo ""

FLOAT_FILE="models/mobilenet_v2_float/model_float.tflite"
QUAN_FILE="models/mobilenet_v2_qat.tflite"

# Modelo float
if [ -f "$FLOAT_FILE" ]; then
    FLOAT_SIZE_H=$(ls -lh "$FLOAT_FILE" | awk '{print $5}')
    FLOAT_SIZE_BYTES=$(stat -c%s "$FLOAT_FILE" 2>/dev/null || wc -c < "$FLOAT_FILE")
    FLOAT_SIZE_MB=$(python3 -c "print(f'{int($FLOAT_SIZE_BYTES) / 1024 / 1024:.2f}')")
    echo "Modelo FLOAT:"
    echo "  - Tamaño: $FLOAT_SIZE_H ($FLOAT_SIZE_MB MB)"
    echo "  - Ruta: $FLOAT_FILE"
else
    echo "⚠️  Modelo FLOAT no encontrado en: $FLOAT_FILE"
fi

echo ""

# Modelo cuantizado
if [ -f "$QUAN_FILE" ]; then
    QUAN_SIZE_H=$(ls -lh "$QUAN_FILE" | awk '{print $5}')
    QUAN_SIZE_BYTES=$(stat -c%s "$QUAN_FILE" 2>/dev/null || wc -c < "$QUAN_FILE")
    QUAN_SIZE_MB=$(python3 -c "print(f'{int($QUAN_SIZE_BYTES) / 1024 / 1024:.2f}')")
    echo "Modelo CUANTIZADO:"
    echo "  - Tamaño: $QUAN_SIZE_H ($QUAN_SIZE_MB MB)"
    echo "  - Ruta: $QUAN_FILE"
else
    echo "⚠️  Modelo CUANTIZADO no encontrado en: $QUAN_FILE"
fi

echo ""

# Calcular factor de compresión si ambos existen
if [ -f "$FLOAT_FILE" ] && [ -f "$QUAN_FILE" ]; then
    FLOAT_SIZE_BYTES=$(stat -c%s "$FLOAT_FILE" 2>/dev/null || wc -c < "$FLOAT_FILE")
    QUAN_SIZE_BYTES=$(stat -c%s "$QUAN_FILE" 2>/dev/null || wc -c < "$QUAN_FILE")
    FACTOR=$(python3 -c "print(f'{int($FLOAT_SIZE_BYTES) / int($QUAN_SIZE_BYTES):.2f}')")
    echo "Factor de compresión: ${FACTOR}x"
    echo ""
    echo "Resumen:"
    echo "  Float: $(python3 -c "print(f'{int($FLOAT_SIZE_BYTES) / 1024 / 1024:.2f}')") MB"
    echo "  Cuantizado: $(python3 -c "print(f'{int($QUAN_SIZE_BYTES) / 1024 / 1024:.2f}')") MB"
    echo "  Reducción: $(python3 -c "print(f'{(1 - int($QUAN_SIZE_BYTES) / int($FLOAT_SIZE_BYTES)) * 100:.1f}')")%"
fi

