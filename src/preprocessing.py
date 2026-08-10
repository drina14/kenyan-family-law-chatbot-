# Prepares raw user questions (not the law text) for the intent classifier, 
# using standard NLP text-cleaning steps.

import re
import spacy

nlp = spacy.load("en_core_web_sm")


class TextPreprocessor:

    def __init__(self):
        self.nlp = nlp

    def clean_text(self, text: str) -> str:  #lowercases the text and strips out punctuation.
        text = text.lower()
        text = re.sub(r"[^\w\s]", "", text)
        return text

    def tokenize(self, text: str):  #splits the sentence into individual words (tokens) using spaCy.
        doc = self.nlp(text)
        return [token.text for token in doc]

    def remove_stopwords(self, text: str): #removes common filler words ("the," "is," "and") that don't carry meaning.
        doc = self.nlp(text)
        return [
            token.text
            for token in doc
            if not token.is_stop
        ]

    def lemmatize(self, text: str): #reduces words to their base or dictionary form (e.g., "running" becomes "run").
        doc = self.nlp(text)
        return [
            token.lemma_
            for token in doc
        ]

    def preprocess(self, text: str): #runs all of the above in sequence and returns everything for the intent classifier to use.
        cleaned = self.clean_text(text)
        tokens = self.tokenize(cleaned)
        filtered = self.remove_stopwords(cleaned)
        lemmas = self.lemmatize(" ".join(filtered))

        return {
            "original": text,
            "cleaned": cleaned,
            "tokens": tokens,
            "filtered_tokens": filtered,
            "lemmas": lemmas,
            "processed_text": " ".join(lemmas),
        }

# Test the preprocessor

if __name__ == "__main__":
    preprocessor = TextPreprocessor()

    sample_question = "Can MY Wife keep inheriting My LAND???"

    result = preprocessor.preprocess(sample_question)

    print("\n = PREPROCESSING RESULTS = ")
    print(f"Original: {result['original']}")
    print(f"Cleaned: {result['cleaned']}")
    print(f"Tokens: {result['tokens']}")
    print(f"Filtered Tokens: {result['filtered_tokens']}")
    print(f"Lemmas: {result['lemmas']}")
    print(f"Processed Text: {result['processed_text']}")