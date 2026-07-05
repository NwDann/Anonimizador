import os
import fitz  # PyMuPDF

class RedactorPDF:
    def __init__(self, ruta_entrada):
        self.doc = fitz.open(ruta_entrada)

    def obtener_num_paginas(self):
        return len(self.doc)

    def obtener_texto_pagina(self, num_pagina):
        return self.doc[num_pagina].get_text()

    def redactar_entidades_en_pagina(self, num_pagina, texto_pagina, resultados_analisis):
        pagina = self.doc[num_pagina]
        
        for entidad in resultados_analisis:
            # Extraer la palabra exacta que el analizador detectó como sensible
            texto_sensible = texto_pagina[entidad.start:entidad.end]
            
            # Buscar dónde está físicamente esa palabra en la página del PDF
            rects = pagina.search_for(texto_sensible)
            
            for rect in rects:
                # Añadir anotación de censura (Cuadro negro)
                pagina.add_redact_annot(rect, fill=(0, 0, 0))
                
        # Aplicar el borrado definitivo en esta página
        pagina.apply_redactions()

    def guardar_y_cerrar(self, ruta_salida):
        # Asegurar que la carpeta de destino exista
        os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
        self.doc.save(ruta_salida)
        self.doc.close()