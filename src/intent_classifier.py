
"""
Intent Classification Module

This module trains a machine learning model to classify
the user's intent based on their question.
"""

import os # import the os module for interacting with the operating system ; handling file paths.
import joblib # import the joblib library for saving and loading Python objects, particularly machine learning models.
import pandas as pd # import the pandas library for data manipulation and analysis, particularly for handling tabular data.

from sklearn.feature_extraction.text import TfidfVectorizer # import the TfidfVectorizer class from the sklearn library to convert text data into numerical feature vectors using the TF-IDF method.
from sklearn.linear_model import LogisticRegression # import the LogisticRegression class from the sklearn library to create a logistic regression model for classification tasks.  
from sklearn.model_selection import train_test_split # import the train_test_split function from the sklearn library to split the dataset into training and testing sets.
from sklearn.metrics import accuracy_score, classification_report # import the accuracy_score and classification_report functions from the sklearn library to evaluate the performance of the trained model.

from preprocessing import TextPreprocessor # import the TextPreprocessor class from the preprocessing module to preprocess the text data before training the model.
from config import MODEL_PATH # import the MODEL_PATH constant from the config module to specify the path where the trained model and vectorizer will be saved and loaded from.


class IntentClassifier:

    def __init__(self, dataset_path=None): #Initializes the IntentClassifier object and optionally loads the training dataset.
        self.dataset = None
        self.preprocessor = TextPreprocessor()
        self.vectorizer = None
        self.model = None

        if dataset_path:
            self.dataset = pd.read_csv(dataset_path)
            self.vectorizer = TfidfVectorizer( #Converts the preprocessed questions into TF-IDF feature vectors.
                ngram_range=(1, 2)
            )
            self.model = LogisticRegression( #Creates the Logistic Regression model used for intent classification.
                random_state=42,
                max_iter=1000
            )

    def show_dataset(self): #Displays a preview of the dataset and shows how many questions belong to each intent.
        """
        Preview the dataset.
        """

        print("\n=== DATASET PREVIEW ===")
        print(self.dataset.head())

        print("\nQuestions per Intent:")
        print(self.dataset["intent"].value_counts())

    def preprocess_dataset(self): #Preprocesses every question in the dataset and stores the cleaned version in a new column.
    
        self.dataset["processed_question"] = self.dataset["question"].apply(
            lambda text: self.preprocessor.preprocess(text)["processed_text"]
        )

        print("\n=== PREPROCESSED DATASET ===")
        print(
            self.dataset[
                ["question", "processed_question", "intent"]
            ].head()
        )

    def train_model(self): #Trains the intent classification model using the preprocessed dataset and evaluates its performance.
        
        X = self.vectorizer.fit_transform(
            self.dataset["processed_question"] #contains the numerical representation of each question.
        )

        y = self.dataset["intent"] #Stores the target labels (intents) for each question.

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        self.model.fit(X_train, y_train) #Trains the Logistic Regression model using the training data.

        predictions = self.model.predict(X_test) #Uses the trained model to predict the intents of the test questions.

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

    def predict_intent(self, question): #Predicts the intent of a new user question using the trained model.
    
        processed = self.preprocessor.preprocess(question)[ #Preprocesses the user's question (cleans, removes stopwords, lemmatizes).
            "processed_text"
        ]

        vector = self.vectorizer.transform([processed]) #Converts the processed question into a TF-IDF feature vector.

        prediction = self.model.predict(vector)

        return prediction[0]

    def save_model(self): #Saves the trained machine learning model and TF-IDF vectorizer so they can be loaded later without retraining.

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

    def load_model(self): #Loads the previously saved machine learning model and TF-IDF vectorizer from disk.
        
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