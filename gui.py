import os
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from src.pipeline import PipelineAnonimizacion  # Reutilizamos tu pipeline exacto[cite: 4]

class AnonimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PrivaDocs — Anonimizador de PDFs con IA")
        self.root.geometry("620x520")
        self.root.resizable(False, False)

        self.archivos_pdf = []
        self.carpeta_destino = ""
        self.pipeline = None

        self._crear_componentes()

    def _crear_componentes(self):
        # Título
        lbl_titulo = tk.Label(self.root, text="PrivaDocs Desktop", font=("Helvetica", 16, "bold"))
        lbl_titulo.pack(pady=10)

        # Frame Archivos
        frame_archivos = tk.LabelFrame(self.root, text=" 1. Selección de Archivos PDF ", padx=10, pady=10)
        frame_archivos.pack(fill="x", padx=15, pady=5)

        btn_seleccionar_archivos = tk.Button(frame_archivos, text="Seleccionar PDFs...", command=self._seleccionar_archivos)
        btn_seleccionar_archivos.pack(anchor="w")

        self.lbl_conteo_archivos = tk.Label(frame_archivos, text="No se han seleccionado archivos.", fg="gray")
        self.lbl_conteo_archivos.pack(anchor="w", pady=5)

        # Frame Destino
        frame_destino = tk.LabelFrame(self.root, text=" 2. Carpeta de Destino ", padx=10, pady=10)
        frame_destino.pack(fill="x", padx=15, pady=5)

        btn_seleccionar_destino = tk.Button(frame_destino, text="Elegir Carpeta de Salida...", command=self._seleccionar_destino)
        btn_seleccionar_destino.pack(anchor="w")

        self.lbl_destino = tk.Label(frame_destino, text="No se ha seleccionado carpeta de destino.", fg="gray")
        self.lbl_destino.pack(anchor="w", pady=5)

        # Botón de Procesamiento
        self.btn_procesar = tk.Button(
            self.root, 
            text="🚀 Anonimizar Documentos", 
            font=("Helvetica", 11, "bold"),
            bg="#12A776", 
            fg="white", 
            padx=10, 
            pady=5,
            command=self._iniciar_procesamiento_hilo
        )
        self.btn_procesar.pack(pady=15)

        # Bar de Progreso y Consola de Estado
        self.progreso = ttk.Progressbar(self.root, orient="horizontal", mode="determinate", length=570)
        self.progreso.pack(pady=5)

        self.txt_logs = tk.Text(self.root, height=8, width=70, font=("Consolas", 9))
        self.txt_logs.pack(padx=15, pady=5)

    def _log(self, mensaje):
        self.txt_logs.insert(tk.END, mensaje + "\n")
        self.txt_logs.see(tk.END)

    def _seleccionar_archivos(self):
        archivos = filedialog.askopenfilenames(
            title="Selecciona uno o más archivos PDF",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if archivos:
            self.archivos_pdf = list(archivos)
            self.lbl_conteo_archivos.config(text=f"✓ {len(self.archivos_pdf)} archivo(s) seleccionado(s).", fg="green")

    def _seleccionar_destino(self):
        destino = filedialog.askdirectory(title="Selecciona la carpeta para guardar los resultados")
        if destino:
            self.carpeta_destino = destino
            self.lbl_destino.config(text=f"✓ Guardar en: {self.carpeta_destino}", fg="green")

    def _iniciar_procesamiento_hilo(self):
        if not self.archivos_pdf:
            messagebox.showwarning("Atención", "Por favor selecciona al menos un archivo PDF.")
            return
        if not self.carpeta_destino:
            messagebox.showwarning("Atención", "Por favor selecciona la carpeta de destino.")
            return

        self.btn_procesar.config(state=tk.DISABLED)
        self.txt_logs.delete("1.0", tk.END)
        
        # Ejecutar en segundo plano para no congelar la ventana
        hilo = threading.Thread(target=self._procesar_archivos)
        hilo.start()

    def _procesar_archivos(self):
        try:
            if not self.pipeline:
                self._log("Cargando modelos de Inteligencia Artificial (spaCy + Presidio)...")
                self.pipeline = PipelineAnonimizacion() #[cite: 4]
                self._log("¡Modelos cargados exitosamente!\n")

            total = len(self.archivos_pdf)
            self.progreso["maximum"] = total
            self.progreso["value"] = 0

            for i, ruta_pdf in enumerate(self.archivos_pdf, 1):
                nombre_archivo = os.path.basename(ruta_pdf)
                ruta_salida = os.path.join(self.carpeta_destino, f"anonimo_{nombre_archivo}")

                self._log(f"[{i}/{total}] Procesando: {nombre_archivo}...")
                self.pipeline.ejecutar(ruta_pdf, ruta_salida) #[cite: 4]
                
                self.progreso["value"] = i
                self._log(f"  └─ Guardado en: anonimo_{nombre_archivo}")

            self._log("\n✅ ¡Todos los documentos han sido anonimizados con éxito!")
            messagebox.showinfo("Finalizado", "El proceso de anonimización ha terminado correctamente.")

        except Exception as e:
            self._log(f"\n❌ Error durante el proceso: {str(e)}")
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")

        finally:
            self.btn_procesar.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = AnonimerApp(root)
    root.mainloop()