# 🌿 Clasificador de Hojas por Antracnosis

Este script automatiza la clasificación de imágenes de hojas en función del nivel de afectación por antracnosis, usando procesamiento en el espacio de color HSV.

---

## 🧠 Descripción

El sistema analiza imágenes contenidas en una carpeta de entrada, detecta zonas oscuras compatibles con síntomas de antracnosis y las clasifica automáticamente en tres categorías:

- ✅ `hSanas/`: hojas saludables
- ⚠️ `hCuarentena/`: hojas potencialmente afectadas
- ❌ `hEnfermas/`: hojas con alta probabilidad de infección

Las imágenes se mueven a su carpeta correspondiente según el análisis.

---

## 📁 Estructura de Carpetas

hojas/
├── imagen1.jpg
├── imagen2.png
└── ...

yaml
Copiar
Editar

Después de ejecutar el script:

hojas/
├── hSanas/
├── hCuarentena/
└── hEnfermas/

yaml
Copiar
Editar

---

## ⚙️ Requisitos

- Python 3.6+
- OpenCV
- NumPy

Instalación:

'''bash
pip install opencv-python numpy



🚀 Uso
Coloca tus imágenes en la carpeta hojas (puede contener .jpg, .png, .jpeg, .webp).

Edita la ruta en el script:

python
Copiar
Editar
carpeta_entrada = "/home/Dowloads/hojas"
Ejecuta el script:

bash
Copiar
Editar
python clasificador_hojas.py
Las imágenes se moverán automáticamente a su categoría correspondiente.

🎯 Lógica de Clasificación
Se convierte cada imagen a HSV.

Se aplica una máscara para detectar zonas oscuras compatibles con antracnosis.

Se calcula el porcentaje afectado:

Estado	Umbral % área afectada
SANA	≤ 0.2%
CUARENTENA	> 0.2% y ≤ 0.4%
ENFERMA	> 0.4%

✏️ Personalización
Puedes ajustar los límites HSV según tus condiciones de iluminación y color:

python
Copiar
Editar
limite_bajo = np.array([5, 50, 10])
limite_alto = np.array([25, 240, 100])
Y modificar los umbrales de clasificación:

python
Copiar
Editar
umbral_cuarentena = 0.2
umbral_enferma = 0.4
📋 Resultado de consola
El script imprime un resumen como este:

scss
Copiar
Editar
hoja01.jpg → SANA (0.03%)
hoja02.jpg → ENFERMA (1.20%)
hoja03.jpg → CUARENTENA (0.32%)
📌 Notas
El script mueve los archivos. Si deseas conservarlos, reemplaza shutil.move(...) por shutil.copy(...).

Asegúrate de que la carpeta de entrada exista y esté bien escrita (¡cuidado con /home/Dowloads!).

👨‍🔬 Autor
Desarrollado por [Tzurudo]
