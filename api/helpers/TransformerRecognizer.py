from presidio_analyzer import EntityRecognizer, RecognizerResult
from presidio_analyzer.nlp_engine import NlpArtifacts
from transformers import pipeline

class TransformerRecognizer(EntityRecognizer):
    def __init__(
        self,
        model_id_or_path,
        mapping_labels,
        aggregation_strategy = "simple",
        supported_language = "en",
        ignore_labels = ["O", "MISC"],
    ):
        # inits transformers pipeline for given mode or path
        self.pipeline = pipeline(
            "token-classification",
            model = model_id_or_path,
            aggregation_strategy = aggregation_strategy,
            ignore_labels = ignore_labels
        )
        
        # map labels to presidio labels
        self.label2presidio = mapping_labels

        # passes entities from model into parent class
        super().__init__(supported_entities = list(self.label2presidio.values()), supported_language = supported_language)

    def analyze(
        self,
        text: str,
        entities = None,
        nlp_artifacts: NlpArtifacts = None
    ):
        results = []

        predicted_entities = self.pipeline(text)
        
        for predicted_entity in predicted_entities:
            if (predicted_entity['entity_group'] not in self.label2presidio):
                continue 
            
            converted_entity = self.label2presidio[predicted_entity["entity_group"]]
            if converted_entity in entities or entities is None:
                results.append(
                    RecognizerResult(
                        entity_type = converted_entity,
                        start = predicted_entity["start"],
                        end = predicted_entity["end"],
                        score = predicted_entity["score"]
                    )
                )
                    
        return results