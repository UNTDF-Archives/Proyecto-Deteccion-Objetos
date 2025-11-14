try:
    from mediapipe_model_maker import object_detector
    from mediapipe_model_maker.python.vision.object_detector import model_spec as ms
    import os
    import random
    import shutil
    print("✅ Todos los módulos se importaron correctamente.")
except ImportError as e:
    print("❌ Error de importación:", e)
except Exception as e:
    print("⚠️ Otro error:", e)

