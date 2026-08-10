"""
Main Chatbot

Coordinates the entire pipeline.
"""

from intent_classifier import IntentClassifier # import the IntentClassifier class from the intent_classifier module to predict the intent of user questions.
from ner import NamedEntityRecognizer # import the NamedEntityRecognizer class from the ner module to extract named entities from user questions.
from vector_store import VectorStore # import the VectorStore class from the vector_store module to retrieve relevant legal context for user questions.
from prompt_builder import PromptBuilder # import the PromptBuilder class from the prompt_builder module to construct prompts for the LLM using user questions, detected intent, entities, and retrieved legal context.
from llm import ClaudeLLM # import the ClaudeLLM class from the llm module to generate responses from the Claude LLM using the constructed prompts.

class LegalChatbot:

    def __init__(self): #Initializes all the components required for the legal chatbot before it starts answering questions.
        print("Loading chatbot...\n")

        self.intent_classifier = IntentClassifier(dataset_path=None) #does not load the training dataset, since the chatbot only needs the already-trained model.
        self.intent_classifier.load_model() #loads intent classifier model and TF-IDF vectorizer from disk, so it can predict the intent of user questions without retraining.

        self.vector_store = VectorStore()
        self.vector_store.load()

        self.ner = NamedEntityRecognizer() #creaes the ner

        self.llm = ClaudeLLM() #creates LLM client 

        print("Chatbot ready!\n")

    def ask(self, question): 
        greetings = [
            "hi",
            "hello",
            "hey",
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if question.lower().strip() in greetings: #Converts the question to lowercase and removes extra spaces.
            return {
                "intent": "greeting",
                "entities": [],
                "sources": [],
                "answer": (
                    "Hello! I'm your Kenyan Family Law AI Assistant. "
                    "Ask me any question about inheritance, marriage, divorce, child custody, or matrimonial property."
                )
            }

        intent = self.intent_classifier.predict_intent(question) #Predicts the intent of the user's legal question using the trained classifier.

        entities = [
    entity["text"]
    for entity in self.ner.extract_entities(question)
]

        retrieved_chunks = self.vector_store.search(question) #Searches the FAISS vector store for the most relevant legal document chunks.

        prompt = PromptBuilder.build_prompt( #Combines the question, intent, entities, and retrieved legal context into a prompt for the LLM.
            question,
            intent,
            entities,
            retrieved_chunks
        )

        answer = self.llm.generate_response(prompt) #sends prompt to LLM

        return {
            "intent": intent,
            "entities": entities,
            "sources": retrieved_chunks,
            "answer": answer
        }

#test
if __name__ == "__main__":
    chatbot = LegalChatbot()

    while True:
        question = input("\nAsk NyumbaLex: ")

        if question.lower() in ["exit", "quit"]:
            print("Thank you for using NyumbaLex. Goodbye!")
            break

        response = chatbot.ask(question)
        print()
        print(response["answer"])
        if response["sources"]:
            print("\nSources:")
            for source in response["sources"]:
                print(f"- {source['document_name']} (Page {source['page_number']})")