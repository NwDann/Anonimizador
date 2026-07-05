from src.analizador import AnalizadorPII
from src.redactor import RedactorPDF

class PipelineAnonimizacion:
    def __init__(self):
        # Inicializamos el motor de IA una sola vez para ahorrar memoria
        self.analizador = AnalizadorPII()

    def ejecutar(self, ruta_entrada, ruta_salida):
        # Inicializar el lector/redactor de PDF
        redactor = RedactorPDF(ruta_entrada)
        total_paginas = redactor.obtain_num_paginas() if hasattr(redactor, 'obtain_num_paginas') else redactor.obtener_num_paginas()
        
        # Procesar página por página
        for num_pagina in range(total_paginas):
            texto_pagina = redactor.obtener_texto_pagina(num_pagina)
            
            # 1. Detectar datos sensibles en el texto de la página
            entidades_detectadas = self.analizador.analizar_texto(texto_pagina)
            
            # 2. Aplicar la censura por coordenadas si se encontraron datos
            if entidades_detectadas:
                redactor.redactar_entidades_en_pagina(num_pagina, texto_pagina, entidades_detectadas)
                
        # 3. Guardar el archivo final limpio
        redactor.guardar_y_cerrar(ruta_salida)