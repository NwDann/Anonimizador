import os
import shutil
import uuid
from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Importar tu pipeline existente
from src.pipeline import PipelineAnonimizacion

# 1. Inicializar la aplicación de FastAPI
app = FastAPI(
    title="Anonimer API",
    description="API para anonimización automática de documentos PDF",
    version="1.0"
)

# 2. Configurar CORS (Crucial para que tu frontend web pueda comunicarse con esta API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, cambia "*" por la URL de tu frontend (ej. "https://anonimer.com")
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Inicializar el motor de IA una sola vez al arrancar el servidor
# Esto evita que el modelo de lenguaje se cargue en cada petición, haciéndolo súper rápido
print("Cargando motor de Inteligencia Artificial...")
pipeline = PipelineAnonimizacion()
print("¡Motor listo!")

# Función auxiliar para eliminar archivos temporales
def limpiar_archivos_temporales(*rutas):
    for ruta in rutas:
        if os.path.exists(ruta):
            os.remove(ruta)

@app.post("/api/anonimizar")
async def anonimizar_documento(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...)
):
    """
    Recibe un archivo PDF, procesa la detección de PII y devuelve el PDF censurado.
    """
    # Crear carpeta temporal si no existe
    os.makedirs("datos/temp", exist_ok=True)
    
    # Generar nombres únicos para evitar colisiones si varios usuarios suben archivos a la vez
    id_unico = str(uuid.uuid4())
    ruta_entrada = f"datos/temp/in_{id_unico}.pdf"
    ruta_salida = f"datos/temp/out_{id_unico}.pdf"
    
    try:
        # Guardar el archivo subido en el disco local temporalmente
        with open(ruta_entrada, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Ejecutar el proceso de anonimización
        pipeline.ejecutar(ruta_entrada, ruta_salida)
        
        # Programar la limpieza para que se ejecute DESPUÉS de enviar la respuesta
        background_tasks.add_task(limpiar_archivos_temporales, ruta_entrada, ruta_salida)
        
        # Devolver el archivo procesado al cliente
        return FileResponse(
            path=ruta_salida, 
            filename=f"seguro_{file.filename}",
            media_type="application/pdf"
        )
        
    except Exception as e:
        # En caso de error, limpiar los archivos que se hayan creado y lanzar un error
        limpiar_archivos_temporales(ruta_entrada, ruta_salida)
        return {"error": f"Ocurrió un error al procesar el documento: {str(e)}"}