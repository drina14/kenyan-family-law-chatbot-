"""
Named Entity Recognition module.

Uses SpaCy's pretrained NER together with an EntityRuler
to recognize important Kenyan family law terms.
"""
import json 
from pathlib import Path 
import spacy 
from spacy.pipeline import EntityRuler 

nlp = spacy.load("en_core_web_sm") 

if "entity_ruler" not in nlp.pipe_names: 
    ruler = nlp.add_pipe("entity_ruler", before="ner")

patterns_path = Path(__file__).parent.parent / "data" / "patterns" / "legal_patterns.json"

with open(patterns_path, "r", encoding="utf-8") as file:
    patterns = json.load(file)

ruler.add_patterns(patterns)

class NamedEntityRecognizer:

    def __init__(self): 
        self.nlp = nlp

    def extract_entities(self, text):
        
        doc = self.nlp(text)

        entities = []

        for ent in doc.ents:
            entities.append({
                "text": ent.text,
                "label": ent.label_
            })

        return entities

#Test
if __name__ == "__main__":

    ner = NamedEntityRecognizer()

    question = "What does the law say about a wife inheriting land from her husband in Kenya?"

    entities = ner.extract_entities(question)

    print("\nDetected Entities:\n")

    for entity in entities:
        print(entity)    