import cv2
import numpy as np
import os
import shutil

# - - - - - - - - - - - - - - - - - - - -
# Carpetas
carpeta_entrada = "/home/zurdexdathtml/Documents/hojas"
carpeta_sanas = os.path.join(carpeta_entrada, "hSanas")
carpeta_cuarentena = os.path.join(carpeta_entrada, "hCuarentena")
carpeta_enfermas = os.path.join(carpeta_entrada, "hEnfermas")

os.makedirs(carpeta_sanas, exist_ok=True)
os.makedirs(carpeta_cuarentena, exist_ok=True)
os.makedirs(carpeta_enfermas, exist_ok=True)

# - - - - - - - - - - - - - - - - - - - -
# Rango HSV para detectar manchas oscuras (antracnosis)
limite_bajo = np.array([5,50,10]) 
limite_alto = np.array([25, 240, 100]) 

# Umbrales para clasificación
umbral_cuarentena = 0.2  # >0.1% va a Cuarentena
umbral_enferma = 0.4    # >0.4% va a Enfermas

# - - - - - - - - - - - - - - - - - - - -
# Procesar todas las imágenes
for archivo in os.listdir(carpeta_entrada):
    if archivo.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
        ruta_img = os.path.join(carpeta_entrada, archivo)
        img = cv2.imread(ruta_img)
        if img is None:
            print(f"No se pudo cargar: {archivo}")
            continue

        # Redimensionar
        img = cv2.resize(img, (600, 800))

        # Convertir a HSV y crear máscara para zonas oscuras
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        mascara = cv2.inRange(hsv, limite_bajo, limite_alto)

        # Aplicar máscara y calcular porcentaje afectado
        pixeles_enfermos = cv2.countNonZero(mascara)
        pixeles_totales = img.shape[0] * img.shape[1]
        porcentaje_enfermo = (pixeles_enfermos / pixeles_totales) * 100

        # Clasificación
        if porcentaje_enfermo > umbral_enferma:
            destino = carpeta_enfermas
            estado = "ENFERMA"
        elif porcentaje_enfermo > umbral_cuarentena:
            destino = carpeta_cuarentena
            estado = "CUARENTENA"
        else:
            destino = carpeta_sanas
            estado = "SANA"

        # Resultado
        print(f"{archivo} → {estado} ({porcentaje_enfermo:.2f}%)")

        # Mover/copiar archivo
        shutil.move(ruta_img, os.path.join(destino, archivo))

