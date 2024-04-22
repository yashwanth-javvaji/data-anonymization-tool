import spacy

from fastapi import APIRouter, HTTPException
from presidio_analyzer import AnalyzerEngine
from presidio_analyzer.nlp_engine import NlpEngineProvider
from presidio_anonymizer import AnonymizerEngine
from pydantic import BaseModel

from ..helpers import TransformerRecognizer

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

nlp = spacy.load("en_core_web_trf")

# Initialize NLP engine provider
provider = NlpEngineProvider(nlp_configuration={
    "nlp_engine_name": "spacy",
    "models": [{"lang_code": "en", "model_name": "en_core_web_trf"}]
})

# Initialize Analyzer engine
analyzer = AnalyzerEngine(
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
analyzer.registry.add_recognizer(transformers_recognizer)
            
def anonymize(text: str) -> str:
    try:
        analyzer_results = analyzer.analyze(text, entities = DEFAULT_ANOYNM_ENTITIES, language = "en")
        engine = AnonymizerEngine()
        return engine.anonymize(text, analyzer_results)
    except Exception as ex:
        return f"An error occurred during anonymization: {str(ex)}"

router = APIRouter()

class AnonymizeTextRequest(BaseModel):
    text: str

@router.post("/")
async def anonymize_text(request: AnonymizeTextRequest):
    try:
        text = request.text
        if not text.strip():
            raise Exception("Text is empty")
        
        result = anonymize(text)
        
        return {
            "status_code": 200,
            "text": result.text
        }
    except Exception as ex:
        return HTTPException(status_code=500, detail=str(ex))