"""
Main Chatbot

Coordinates the entire pipeline.
"""

from intent_classifier import IntentClassifier 
from ner import NamedEntityRecognizer 
from vector_store import VectorStore 
from prompt_builder import PromptBuilder 
from llm import ClaudeLLM 

class LegalChatbot:

    def __init__(self): 
        print("Loading chatbot...\n")

        self.intent_classifier = IntentClassifier(dataset_path=None) 
        self.intent_classifier.load_model() 

        self.vector_store = VectorStore()
        self.vector_store.load()

        self.ner = NamedEntityRecognizer() 

        self.llm = ClaudeLLM() 

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

        if question.lower().strip() in greetings: 
            return {
                "intent": "greeting",
                "entities": [],
                "sources": [],
                "answer": (
                    "Hello! I'm your Kenyan Family Law AI Assistant. "
                    "Ask me any question about inheritance, marriage, divorce, child custody, or matrimonial property."
                )
            }

        intent = self.intent_classifier.predict_intent(question) 

        entities = [
    entity["text"]
    for entity in self.ner.extract_entities(question)
]

        retrieved_chunks = self.vector_store.search(question) 

        prompt = PromptBuilder.build_prompt( 
            question,
            intent,
            entities,
            retrieved_chunks
        )

        answer = self.llm.generate_response(prompt) 

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