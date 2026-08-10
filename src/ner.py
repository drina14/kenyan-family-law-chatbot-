"""
Named Entity Recognition module.

Uses SpaCy's pretrained NER together with an EntityRuler
to recognize important Kenyan family law terms.
"""
import json # import the json module to read the legal_patterns.json file containing custom entity patterns.
from pathlib import Path # import the Path class from the pathlib module to handle file paths in a platform-independent way.
import spacy # import the spacy library for natural language processing tasks, including named entity recognition (NER).
from spacy.pipeline import EntityRuler # import the EntityRuler class from the spacy.pipeline module to create custom entity patterns for NER.

nlp = spacy.load("en_core_web_sm") #Loads the pre-trained spaCy English language model for Natural Language Processing ; NER

if "entity_ruler" not in nlp.pipe_names: #Adds a custom EntityRuler to spaCy and loads legal entity patterns from a JSON file.
    ruler = nlp.add_pipe("entity_ruler", before="ner")

patterns_path = Path(__file__).parent.parent / "data" / "patterns" / "legal_patterns.json"

with open(patterns_path, "r", encoding="utf-8") as file:
    patterns = json.load(file)

ruler.add_patterns(patterns)

class NamedEntityRecognizer:

    def __init__(self): #Initializes the Named Entity Recognizer and extracts named entities from a given text.
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