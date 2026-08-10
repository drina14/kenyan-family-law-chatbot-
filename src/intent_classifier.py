
"""
Intent Classification Module

This module trains a machine learning model to classify
the user's intent based on their question.
"""

import os 
import joblib 
import pandas as pd 

from sklearn.feature_extraction.text import TfidfVectorizer 
from sklearn.linear_model import LogisticRegression 
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, classification_report 

from preprocessing import TextPreprocessor 
from config import MODEL_PATH 


class IntentClassifier:

    def __init__(self, dataset_path=None):
        self.dataset = None
        self.preprocessor = TextPreprocessor()
        self.vectorizer = None
        self.model = None

        if dataset_path:
            self.dataset = pd.read_csv(dataset_path)
            self.vectorizer = TfidfVectorizer( 
                ngram_range=(1, 2)
            )
            self.model = LogisticRegression( 
                random_state=42,
                max_iter=1000
            )

    def show_dataset(self): 
        """
        Preview the dataset.
        """

        print("\n=== DATASET PREVIEW ===")
        print(self.dataset.head())

        print("\nQuestions per Intent:")
        print(self.dataset["intent"].value_counts())

    def preprocess_dataset(self): 
    
        self.dataset["processed_question"] = self.dataset["question"].apply(
            lambda text: self.preprocessor.preprocess(text)["processed_text"]
        )

        print("\n=== PREPROCESSED DATASET ===")
        print(
            self.dataset[
                ["question", "processed_question", "intent"]
            ].head()
        )

    def train_model(self): 
        
        X = self.vectorizer.fit_transform(
            self.dataset["processed_question"] 
        )

        y = self.dataset["intent"] 

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        self.model.fit(X_train, y_train) 

        predictions = self.model.predict(X_test) 

        accuracy = accuracy_score(
            y_test,
            predictions
        )

        print(f"\nModel Accuracy: {accuracy:.2f}")

        print("\nClassification Report:\n")

        print(
            classification_report(
                y_test,
                predictions,
                zero_division=0
            )
        )

    def predict_intent(self, question): 
    
        processed = self.preprocessor.preprocess(question)[ 
            "processed_text"
        ]

        vector = self.vectorizer.transform([processed]) 
        prediction = self.model.predict(vector)

        return prediction[0]

    def save_model(self): 

        os.makedirs("data/models", exist_ok=True)

        joblib.dump(
            self.model,
            "data/models/intent_classifier.pkl"
        )

        joblib.dump(
            self.vectorizer,
            "data/models/tfidf_vectorizer.pkl"
        )

        print("\nModel saved successfully!")

    def load_model(self): 
        
        self.model = joblib.load(
        MODEL_PATH / "intent_classifier.pkl"
    )

        self.vectorizer = joblib.load(
        MODEL_PATH / "tfidf_vectorizer.pkl"
    )


        print("Model loaded successfully!")


#test
if __name__ == "__main__":

    classifier = IntentClassifier(
        "data/training/intent_dataset.csv"
    )

    classifier.show_dataset()

    classifier.preprocess_dataset()

    classifier.train_model()

    classifier.save_model()

    print("\n=== TEST PREDICTIONS ===\n")

    questions = [
        "Can my wife inherit land?",
        "How do I file for divorce?",
        "Can I register a marriage?",
        "Who gets custody of my child?",
        "How is matrimonial property divided?"
    ]

    for question in questions:

        prediction = classifier.predict_intent(question)

        print(f"Question : {question}")
        print(f"Intent   : {prediction}")
        print("-" * 50)