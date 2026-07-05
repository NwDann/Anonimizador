from src.pipeline import PipelineAnonimizacion

if __name__ == "__main__":
    # Instanciar el pipeline principal
    pipeline = PipelineAnonimizacion()
    
    # Definir rutas
    archivo_entrada = "datos/entrada/RolPagos_0127.pdf"
    archivo_salida = "datos/salida/documento_anonimo.pdf"
    
    print("Iniciando pipeline de anonimización modular...")
    
    try:
        pipeline.ejecutar(archivo_entrada, archivo_salida)
        print(f"¡Proceso completado con éxito! Archivo seguro en: {archivo_salida}")
    except Exception as e:
        print(f"Ocurrió un error durante el proceso: {e}")