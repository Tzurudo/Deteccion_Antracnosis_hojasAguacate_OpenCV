🚀 Ejecución
Clona o descarga el proyecto.

Ejecuta el script:

bash
Copiar
Editar
python app_antracnosis.py
Introduce la URL de la cámara IP o ruta de video (por ejemplo, 0 para webcam local),pero puede
ser de la Aplicación de IP web Cam disponible en android.

Haz clic en "Iniciar Análisis".

📷 Ejemplo de uso
Imagen original: se muestra la captura en tiempo real.

Áreas detectadas: zonas dentro del rango de colores indicativos de la enfermedad.

Diagnóstico dinámico y porcentaje de afectación.

🎯 Algoritmo
Conversión BGR ➡ HSV

Filtro cv2.inRange para colores entre [5, 50, 10] y [20, 240, 100]

Cálculo de porcentaje de píxeles afectados

Clasificación del estado:

> 0.4% → Alta probabilidad

> 0.1% → Posible

<= 0.1% → Sano



```bash
pip install opencv-python pillow numpy
