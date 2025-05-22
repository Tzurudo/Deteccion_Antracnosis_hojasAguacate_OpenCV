import cv2
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading

class AplicacionAntracnosis:
    def __init__(self, ventana_principal):
        self.ventana_principal = ventana_principal
        self.ventana_principal.title("Análisis de Antracnosis")
        
        # Variables
        self.url_camara = tk.StringVar(value="/video")
        self.analisis_activo = False
        self.capturador_video = None
        self.id_actualizacion = None
        
        # Configuración de rangos HSV
        self.hsv_minimo = np.array([5, 50, 10])
        self.hsv_maximo = np.array([20, 240, 100])
        
        # Crear interfaz
        self.crear_interfaz()
        
    def crear_interfaz(self):
        # Marco de control
        marco_control = ttk.LabelFrame(self.ventana_principal, text="Controles", padding=(10, 5))
        marco_control.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        # Entrada para URL de la cámara
        ttk.Label(marco_control, text="URL Cámara:").grid(row=0, column=0, sticky="w")
        entrada_url = ttk.Entry(marco_control, textvariable=self.url_camara, width=30)
        entrada_url.grid(row=0, column=1, padx=5, pady=2)
        
        # Botones
        self.boton_iniciar = ttk.Button(marco_control, text="Iniciar Análisis", command=self.iniciar_analisis)
        self.boton_iniciar.grid(row=1, column=0, pady=10)
        
        self.boton_detener = ttk.Button(marco_control, text="Detener Análisis", command=self.detener_analisis, state=tk.DISABLED)
        self.boton_detener.grid(row=1, column=1, pady=10)
        
        # Marco de diagnóstico
        marco_diagnostico = ttk.LabelFrame(self.ventana_principal, text="Diagnóstico", padding=(10, 5))
        marco_diagnostico.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        
        self.texto_diagnostico = tk.StringVar(value="Estado: No iniciado")
        ttk.Label(marco_diagnostico, textvariable=self.texto_diagnostico, font=('Arial', 16, 'bold')).pack(anchor="w")
        
        self.texto_area = tk.StringVar(value="Área afectada: 0.00%")
        ttk.Label(marco_diagnostico, font=('Arial', 16, 'bold'), textvariable=self.texto_area).pack(anchor="w")
        
        # Marco para las imágenes (ahora con dos columnas)
        marco_imagenes = ttk.Frame(self.ventana_principal)
        marco_imagenes.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky="nsew")
        
        # Configurar grid para las imágenes
        marco_imagenes.columnconfigure(0, weight=1)
        marco_imagenes.columnconfigure(1, weight=1)
        
        # Imagen original (columna izquierda)
        self.etiqueta_original = ttk.Label(marco_imagenes, text="Imagen Original")
        self.etiqueta_original.grid(row=0, column=0, pady=(0, 5))
        self.panel_original = ttk.Label(marco_imagenes)
        self.panel_original.grid(row=1, column=0, padx=5, pady=5)
        
        # Imagen procesada (columna derecha)
        self.etiqueta_procesada = ttk.Label(marco_imagenes, text="Áreas Detectadas")
        self.etiqueta_procesada.grid(row=0, column=1, pady=(0, 5))
        self.panel_procesada = ttk.Label(marco_imagenes)
        self.panel_procesada.grid(row=1, column=1, padx=5, pady=5)
        
        # Configurar grid principal
        self.ventana_principal.columnconfigure(0, weight=1)
        self.ventana_principal.columnconfigure(1, weight=3)
        self.ventana_principal.rowconfigure(0, weight=1)
        self.ventana_principal.rowconfigure(1, weight=1)
        
    def iniciar_analisis(self):
        if self.analisis_activo:
            return
            
        self.analisis_activo = True
        self.boton_iniciar.config(state=tk.DISABLED)
        self.boton_detener.config(state=tk.NORMAL)
        
        try:
            self.capturador_video = cv2.VideoCapture(self.url_camara.get())
            if not self.capturador_video.isOpened():
                raise Exception("No se pudo abrir la cámara")
                
            # Iniciar hilo para el procesamiento
            self.hilo_procesamiento = threading.Thread(target=self.procesar_fotograma, daemon=True)
            self.hilo_procesamiento.start()
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la cámara:\n{str(e)}")
            self.detener_analisis()
    
    def detener_analisis(self):
        self.analisis_activo = False
        self.boton_iniciar.config(state=tk.NORMAL)
        self.boton_detener.config(state=tk.DISABLED)
        
        if self.capturador_video is not None:
            self.capturador_video.release()
            self.capturador_video = None
        
        if self.id_actualizacion:
            self.ventana_principal.after_cancel(self.id_actualizacion)
            self.id_actualizacion = None
            
        self.texto_diagnostico.set("Estado: Detenido")
    
    def procesar_fotograma(self):
        while self.analisis_activo and self.capturador_video is not None:
            exito, fotograma = self.capturador_video.read()
            if not exito:
                self.texto_diagnostico.set("Error: No se puede capturar el fotograma")
                continue
                
            # Procesamiento de la imagen
            fotograma = cv2.resize(fotograma, (600, 800))
            imagen_hsv = cv2.cvtColor(fotograma, cv2.COLOR_BGR2HSV)
            mascara = cv2.inRange(imagen_hsv, self.hsv_minimo, self.hsv_maximo)
            resultado = cv2.bitwise_and(fotograma, fotograma, mask=mascara)
            
            # Cálculo del porcentaje
            pixeles_afectados = cv2.countNonZero(mascara)
            total_pixeles = fotograma.shape[0] * fotograma.shape[1]
            porcentaje_afectado = (pixeles_afectados / total_pixeles) * 100
            
            # Diagnóstico
            diagnostico = "\nSana"
            if porcentaje_afectado > 0.4:
                diagnostico = "\nAlta probabilidad de antracnosis"
            elif porcentaje_afectado > 0.1:
                diagnostico = "\nPosible antracnosis"
                
            # Actualizar interfaz
            self.actualizar_interfaz(fotograma, resultado, diagnostico, porcentaje_afectado)
            
            # Pequeña pausa para no saturar
            cv2.waitKey(30)
    
    def actualizar_interfaz(self, imagen_original, imagen_procesada, diagnostico, porcentaje):
        # Convertir imágenes para Tkinter
        imagen_original = cv2.cvtColor(imagen_original, cv2.COLOR_BGR2RGB)
        imagen_procesada = cv2.cvtColor(imagen_procesada, cv2.COLOR_BGR2RGB)
        
        imagen_original = Image.fromarray(imagen_original)
        imagen_procesada = Image.fromarray(imagen_procesada)
        
        imagen_original = ImageTk.PhotoImage(image=imagen_original)
        imagen_procesada = ImageTk.PhotoImage(image=imagen_procesada)
        
        # Actualizar los paneles
        self.panel_original.configure(image=imagen_original)
        self.panel_original.image = imagen_original
        
        self.panel_procesada.configure(image=imagen_procesada)
        self.panel_procesada.image = imagen_procesada
        
        # Actualizar textos
        self.texto_diagnostico.set(f"Diagnóstico: {diagnostico}")
        self.texto_area.set(f"Área afectada: {porcentaje:.2f}%")
        
        # Programar próxima actualización
        if self.analisis_activo:
            self.id_actualizacion = self.ventana_principal.after(10, lambda: None)

if __name__ == "__main__":
    ventana = tk.Tk()
    app = AplicacionAntracnosis(ventana)
    ventana.mainloop()