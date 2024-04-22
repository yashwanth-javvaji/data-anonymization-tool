import spacy

from flask_restful import Resource, reqparse
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from server.helpers import TransformerRecognizer

DEFAULT_ANOYNM_ENTITIES = [
    # Global
    "CREDIT_CARD",
    "CRYPTO",
    "DATE_TIME",
    "EMAIL_ADDRESS",
    "IBAN_CODE",
    "IP_ADDRESS",
    "NRP",
    "LOCATION",
    "PERSON",
    "PHONE_NUMBER",
    "MEDICAL_LICENSE",
    "URL",
    
    # USA
    "US_BANK_NUMBER",
    "US_DRIVER_LICENSE",
    "US_ITIN",
    "US_PASSPORT",
    "US_SSN",
    
    # UK
    "UK_NHS",
    
    # Spain
    "ES_NIF",
    
    # Italy
    "IT_FISCAL_CODE",
    "IT_DRIVER_LICENSE",
    "IT_VAT_CODE",
    "IT_PASSPORT",
    "IT_IDENTITY_CARD",
    
    # Poland
    "PL_PESEL",
    
    # Singapore
    "SG_NRIC_FIN",
    "SG_UEN",
    
    # Australia
    "AU_ABN",
    "AU_ACN",
    "AU_TFN",
    "AU_MEDICARE",
    
    # India
    "IN_PAN",
    "IN_AADHAAR",
    "IN_VEHICLE_REGISTRATION"
]

class AnonymizeTextHandler(Resource):
    def __init__(self) -> None:
        super().__init__()
        
        nlp = spacy.load("en_core_web_trf")
        
        # Initialize NLP engine provider
        provider = NlpEngineProvider(nlp_configuration={
            "nlp_engine_name": "spacy",
            "models": [{"lang_code": "en", "model_name": "en_core_web_trf"}]
        })

        # Initialize Analyzer engine
        self.analyzer = AnalyzerEngine(
            nlp_engine=provider.create_engine(),
            supported_languages=["en"]
        )

        # Initialize Transformer recognizer
        mapping_labels = {entity: entity for entity in DEFAULT_ANOYNM_ENTITIES}
        transformers_recognizer = TransformerRecognizer(
            model_id_or_path="dslim/bert-base-NER",
            mapping_labels=mapping_labels
        )
        
        # Add Transformer recognizer to the Analyzer engine
        self.analyzer.registry.add_recognizer(transformers_recognizer)
            
    def anonymize(self, text: str) -> str:
        try:
            analyzer_results = self.analyzer.analyze(text, entities = DEFAULT_ANOYNM_ENTITIES, language = "en")
            engine = AnonymizerEngine()
            return engine.anonymize(text, analyzer_results)
        except Exception as ex:
            return f"An error occurred during anonymization: {str(ex)}"

    def post(self) -> dict:
        try:
            # Parse request to get the text
            parser = reqparse.RequestParser()
            parser.add_argument("text", type = str, required = True)            
            args = parser.parse_args()
            text = args.get("text", "")
            
            # Check if the text is empty
            if text.strip() == "":
                raise Exception("Text cannot be empty")
            
            # Anonymize the text
            result = self.anonymize(text)
            
            # Return the anonymized text
            return result.text
        except Exception as ex:
            return {"error": str(ex)}