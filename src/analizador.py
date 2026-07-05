from presidio_analyzer import AnalyzerEngine, Pattern, PatternRecognizer
from presidio_analyzer.nlp_engine import NlpEngineProvider

class AnalizadorPII:
    def __init__(self):
        # 1. Configurar el motor NLP para Español
        configuracion_nlp = {
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "es", "model_name": "es_core_news_lg"}]
        }
        proveedor = NlpEngineProvider(nlp_configuration=configuracion_nlp)
        motor_nlp = proveedor.create_engine()
        
        # 2. Inicializar el analizador base
        self.analizador = AnalyzerEngine(nlp_engine=motor_nlp, supported_languages=["es"])
        
        # 3. Cargar nuestras reglas personalizadas
        self._cargar_reconocedores_personalizados()

    def _cargar_reconocedores_personalizados(self):
        # --- RECONOCEDOR PARA CÉDULA / DNI ---
        # Detecta secuencias de 10 dígitos (ej: Ecuador, Colombia)
        # Puedes cambiar el regex si tu formato lleva guiones, ej: r"\b\d{2}-\d{7}-\d{1}\b"
        patron_cedula = Pattern(
            name="patron_cedula",
            regex=r"\b\d{10}\b", 
            score=0.95  # Nivel de confianza alto (0.0 a 1.0)
        )
        reconocedor_cedula = PatternRecognizer(
            supported_entity="CEDULA",
            patterns=[patron_cedula],
            supported_language="es"
        )

        # --- RECONOCEDOR PARA TELÉFONOS LOCALES ---
        # Detecta formatos comunes de celular (ej: que empiecen con 09 y tengan 10 dígitos, o con +593)
        patron_telefono = Pattern(
            name="patron_telefono",
            regex=r"\b(09\d{8}|\+?\d{2,3}\s?9\d{8})\b",
            score=0.90
        )
        reconocedor_telefono = PatternRecognizer(
            supported_entity="TELEFONO_CUSTOM",
            patterns=[patron_telefono],
            supported_language="es"
        )

        # Agregar los nuevos reconocedores al registro de Presidio
        self.analizador.registry.add_recognizer(reconocedor_cedula)
        self.analizador.registry.add_recognizer(reconocedor_telefono)

    def analizar_texto(self, texto):
        # Definimos explícitamente la lista de entidades que queremos rastrear
        # Mezclamos las nativas de spaCy (PERSON, ORG) con las nuestras (CEDULA, TELEFONO_CUSTOM)
        entidades_a_buscar = ["PERSON", "ORG", "CEDULA", "TELEFONO_CUSTOM", "EMAIL"]
        
        return self.analizador.analyze(
            text=texto,
            language="es",
            entities=entidades_a_buscar
        )