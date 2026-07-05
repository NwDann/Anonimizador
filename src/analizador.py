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
        # 1. Cédula / DNI
        reconocedor_cedula = PatternRecognizer(
            supported_entity="CEDULA",
            patterns=[Pattern(name="patron_cedula", regex=r"\b\d{10}\b", score=0.95)],
            supported_language="es"
        )

        # 2. Teléfonos (Ampliando cobertura)
        reconocedor_telefono = PatternRecognizer(
            supported_entity="TELEFONO_CUSTOM",
            patterns=[Pattern(name="patron_telefono", regex=r"\b(?:\+?\d{1,3}[\s-]?)?(?:09\d{8}|[2-9]\d{6,8})\b", score=0.85)],
            supported_language="es"
        )

        # 3. Correos Electrónicos (Forzando detección 100% precisa)
        reconocedor_email = PatternRecognizer(
            supported_entity="EMAIL_CUSTOM",
            patterns=[Pattern(name="patron_email", regex=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", score=1.0)],
            supported_language="es"
        )

        # 4. Direcciones Físicas (Captura nomenclaturas comunes en español)
        reconocedor_direccion = PatternRecognizer(
            supported_entity="DIRECCION_CUSTOM",
            patterns=[Pattern(name="patron_direccion", regex=r"\b(?:Av\.|Avenida|Calle|C\.|Pje\.|Pasaje|Blvd\.|Mz\.|Manzana|Lote|Sector)\s+[A-ZÁÉÍÓÚÑa-záéíóúñ0-9\s.,-]{5,50}\b", score=0.85)],
            supported_language="es"
        )

        # Inyectar los reconocedores al motor
        for reconocedor in [reconocedor_cedula, reconocedor_telefono, reconocedor_email, reconocedor_direccion]:
            self.analizador.registry.add_recognizer(reconocedor)
        
    def analizar_texto(self, texto):
        # nativas de spaCy (PERSON, ORG) con (CEDULA, TELEFONO_CUSTOM)
        entidades_a_buscar = ["PERSON", "ORG", "CEDULA", "TELEFONO_CUSTOM", "EMAIL_CUSTOM", "DIRECCION_CUSTOM"]
        
        return self.analizador.analyze(
            text=texto,
            language="es",
            entities=entidades_a_buscar
        )