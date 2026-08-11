# NyumbaLex 

## Kenyan Family Law AI Assistant

NyumbaLex is an AI-powered legal information chatbot designed to help users find information about **Kenyan family law** using a collection of Kenyan legal documents.

The system combines **Natural Language Processing (NLP)**, **Named Entity Recognition (NER)**, **intent classification**, **semantic embeddings**, **FAISS vector search**, **Retrieval-Augmented Generation (RAG)**, and **Claude Sonnet 4.6** to retrieve relevant legal information and generate clear answers.

>  **Disclaimer:** NyumbaLex provides legal information for educational and informational purposes only. It does not constitute legal advice and should not replace consultation with a qualified legal professional.

---

## 1. Project Overview

Finding relevant information in lengthy legal documents can be difficult, especially for users who are unfamiliar with legal terminology.

NyumbaLex addresses this problem by allowing a user to ask a legal question in natural language.

For example:

> "What are the rights of a spouse in Kenya?"

The chatbot processes the question, searches the available Kenyan legal documents for relevant passages, and provides an answer based on the retrieved information.

The system also provides references to the legal documents and pages used to generate the response.

---

## 2. Main Objectives

The project aims to:

- Provide an accessible interface for asking Kenyan family law questions.
- Reduce the difficulty of searching lengthy legal documents.
- Apply NLP techniques to understand user questions.
- Identify relevant legal concepts and entities.
- Retrieve semantically relevant sections of legal documents.
- Use an LLM to generate natural-language responses.
- Ground responses in retrieved legal documents.
- Provide document and page references for transparency.
- Demonstrate the practical application of NLP and RAG in the legal domain.

---

## 3. Legal Documents

The current knowledge base contains the following Kenyan legal documents:

- Constitution of Kenya
- Children Act
- Law of Succession Act
- Marriage Act
- Matrimonial Property Act

These documents are processed and converted into searchable representations before being used by the chatbot.

---

# 4. System Architecture

The overall pipeline is:

```text
                  USER
                    │
                    ▼
             Legal Question
                    │
                    ▼
          ┌───────────────────┐
          │ Text Preprocessing │
          └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Intent Classifier  │
          └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │       NER         │
          │ Named Entities    │
          └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │    Embeddings     │
          └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │   FAISS Search    │
          │ Vector Retrieval  │
          └───────────────────┘
                    │
                    ▼
          Relevant Legal Text
                    │
                    ▼
          ┌───────────────────┐
          │   Prompt Builder  │
          └───────────────────┘
                    │
                    ▼
          ┌───────────────────┐
          │  Claude Sonnet    │
          │      4.6          │
          └───────────────────┘
                    │
                    ▼
              Final Answer
                    │
                    ▼
             User Interface


5. Technologies Used
Technology	Purpose
Python	Main programming language
Streamlit	Web interface
spaCy	NLP and Named Entity Recognition
scikit-learn	Intent classification and TF-IDF
Sentence Transformers	Semantic embeddings
FAISS	Vector similarity search
LangChain Text Splitters	Document chunking
PyPDF	PDF text extraction
Anthropic Claude	Large Language Model
Joblib	Saving/loading ML models
NumPy	Numerical operations
python-dotenv	Environment variables


6. Natural Language Processing


NyumbaLex uses several NLP techniques:

6.1 Text Preprocessing

Text preprocessing prepares user input for downstream NLP components.

The preprocessing stage performs operations such as:

Converting text to lowercase.
Cleaning unnecessary characters.
Normalizing the input.
Preparing text for NLP analysis.

The goal is to provide consistent text to the other components.

6.2 Intent Classification

The chatbot uses an intent classifier to determine what type of legal question the user is asking.

Examples of possible intents include:

inheritance
marriage
divorce
child custody
child maintenance
matrimonial property
adoption

The classifier helps the system understand the general purpose of a question.

For example:

"Will my wife inherit my land?"

may be classified as:

inheritance

The detected intent is used internally by the chatbot and is not displayed to the end user.

7. Named Entity Recognition

Named Entity Recognition, or NER, identifies important entities in the user's question.

For example:

"Can my wife inherit our family land?"

may contain entities related to:

Person
Property
Legal concepts

NER helps provide additional information about the user's question.

The entities are used internally rather than being displayed in the final response.

8. PDF Processing

The legal documents are stored as PDF files.

The PDF loader extracts text from the documents while preserving important metadata such as:

Document name
Page number

This metadata is important because it allows the chatbot to provide references to the source of its answer.

9. Text Chunking

Long legal documents cannot be sent directly to the language model as one large block of text.

The documents are therefore divided into smaller sections called chunks.

NyumbaLex uses:

RecursiveCharacterTextSplitter

The chunking process uses overlapping sections so that important information near the boundaries of chunks is less likely to be lost.

Each chunk retains metadata such as:

chunk_id
document_name
page_number
text


10. Embeddings

Embeddings convert text into numerical vectors.

A legal passage such as:

"The surviving spouse may have rights in the estate..."

is converted into a numerical representation.

The same process is applied to the user's question.

This allows the system to compare the meaning of the question with the meaning of stored legal passages.

Unlike simple keyword matching, semantic embeddings can identify passages that are conceptually related even when they do not use exactly the same words.


11. FAISS Vector Search

FAISS is used to efficiently search the embedding database.

The process is:

User Question
      ↓
Question Embedding
      ↓
FAISS Similarity Search
      ↓
Most Relevant Legal Chunks

The system retrieves the legal passages that are most semantically similar to the user's question.

The retrieved chunks are then passed to the next stage.



12. Retrieval-Augmented Generation

NyumbaLex uses a Retrieval-Augmented Generation architecture.

RAG combines:

Information Retrieval
+
Large Language Model

Instead of asking Claude to answer a legal question entirely from its pretrained knowledge, NyumbaLex first retrieves relevant passages from its legal document collection.

The retrieved information is then included in the prompt sent to Claude.

This helps keep responses grounded in the project's legal knowledge base.



13. Prompt Building

The prompt builder combines:

The user's question
Relevant legal context
Instructions for answering
Legal-response formatting requirements

The resulting prompt is sent to the language model.

The model is instructed to answer based on the retrieved legal context rather than inventing unsupported information.


14. Claude Sonnet 4.6

NyumbaLex uses Claude Sonnet 4.6 as its language model.

Claude receives the constructed prompt and generates the final natural-language response.

The model is responsible for:

Understanding the retrieved legal information.
Explaining it in understandable language.
Structuring the answer.
Providing appropriate limitations where the retrieved documents do not contain enough information.


15. Source References

One of the important features of NyumbaLex is source transparency.

The chatbot returns references containing information such as:

Law of Succession Act — Page 48
Children Act — Page 53

This allows the user to see which documents contributed to the retrieved context.

The references are particularly important in a legal-information application because users should be able to distinguish between generated explanations and the underlying legal sources.


16. Streamlit Interface

The application uses Streamlit as its frontend.

The interface provides:

NyumbaLex branding
Legal question input
AI-generated responses
Source references
Legal disclaimer

The Streamlit application connects directly to the existing Python chatbot backend.

The architecture is:

Streamlit
   │
   ▼
app.py
   │
   ▼
LegalChatbot
   │
   ├── Intent Classifier
   ├── NER
   ├── Retriever
   ├── Prompt Builder
   └── Claude


17. Project Structure
kenyan-family-law-chatbot/
│
├── data/
│   │
│   ├── embeddings/
│   │   ├── chunks.pkl
│   │   └── faiss_index.bin
│   │
│   ├── models/
│   │   ├── intent_classifier.pkl
│   │   └── tfidf_vectorizer.pkl
│   │
│   ├── patterns/
│   │   └── legal_patterns.json
│   │
│   ├── raw/
│   │   ├── Children Act.pdf
│   │   ├── Constitution of Kenya.pdf
│   │   ├── Law of Succession Act.pdf
│   │   ├── Marriage Act.pdf
│   │   └── Matrimonial Property Act.pdf
│   │
│   └── training/
│       └── intent_dataset.csv
│
├── src/
│   │
│   ├── app.py
│   ├── chatbot.py
│   ├── chunker.py
│   ├── config.py
│   ├── embeddings_generator.py
│   ├── intent_classifier.py
│   ├── llm.py
│   ├── ner.py
│   ├── pdf_loader.py
│   ├── preprocessing.py
│   ├── prompt_builder.py
│   └── vector_store.py
│
├── .gitignore
├── README.md
└── requirements.txt


18. Important Files
app.py:

The Streamlit frontend.

It:

Creates the user interface.
Displays conversations.
Accepts legal questions.
Sends questions to the chatbot.
Displays answers.
Displays references.


chatbot.py:

The central controller of the application.

It coordinates the different NLP and AI components.

Conceptually:

Question
   ↓
Preprocessing
   ↓
Intent
   ↓
NER
   ↓
Retrieval
   ↓
Prompt
   ↓
Claude
   ↓
Response

pdf_loader.py:

Responsible for extracting text from the legal PDF documents.

chunker.py:

Splits extracted legal text into smaller searchable chunks.

embeddings_generator.py:

Creates vector embeddings for the legal document chunks.

vector_store.py:

Stores and searches the vector representations using FAISS.

intent_classifier.py:

Loads and uses the trained intent classification model.

preprocessing.py:

Prepares text for NLP processing and supports the spaCy pipeline.

ner.py:

Handles Named Entity Recognition.

prompt_builder.py:

Constructs the prompt containing the user's question and retrieved legal context.

llm.py:

Handles communication with the Anthropic API and Claude.

config.py:

Contains configuration values used by the application.


19. Running the Project Locally

Clone the repository:

git clone <YOUR_GITHUB_REPOSITORY_URL>

Move into the project:

cd kenyan-family-law-chatbot

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file and add your Anthropic API key:

ANTHROPIC_API_KEY=your_api_key_here

Run the application:

streamlit run src/app.py


20. Environment Variables

The application requires an Anthropic API key.

Example:

ANTHROPIC_API_KEY=your_api_key_here


For deployment, the API key should be configured through the hosting platform's secrets management system.

21. Example Questions

Users can ask questions such as:

What are the grounds for divorce in Kenya?
What rights does a surviving spouse have?
Can a father get custody of his child?
How is matrimonial property divided?
What does Kenyan law say about inheritance?
What are the requirements for marriage in Kenya?


22. Limitations

NyumbaLex has several important limitations.

Limited Knowledge Base

The chatbot can only retrieve information from the legal documents included in its knowledge base.

If a question concerns legislation or case law that is not included, the system may not be able to provide a complete answer.

Retrieval Limitations

The quality of an answer depends partly on whether the retrieval system finds relevant legal passages.

AI Limitations:

Claude generates natural-language explanations and may still make mistakes.

Legal Disclaimer:

The chatbot is an educational legal-information system and is not a replacement for a qualified lawyer.

23. Why RAG Instead of a General Chatbot?

A general-purpose language model may already know information about Kenyan law, but relying entirely on its pretrained knowledge creates several problems.

RAG allows NyumbaLex to provide the model with relevant passages from a controlled legal document collection.

This provides:

Better grounding
Source references
More transparency
Easier knowledge-base updates
Reduced reliance on unsupported model knowledge

24. End-to-End Example

Suppose a user asks:

Will my wife inherit my land?

The system processes the question through several stages.

Step 1 — Preprocessing

The question is cleaned and prepared for NLP processing.

Step 2 — Intent Classification

The system identifies the likely legal intent.

inheritance
Step 3 — NER

Relevant entities and concepts are identified.

Step 4 — Embedding

The question is converted into a numerical vector.

Step 5 — Retrieval

FAISS searches the legal knowledge base for semantically similar passages.

Step 6 — Context

The most relevant passages are collected.

Step 7 — Prompt Construction

The question and retrieved legal passages are combined into a structured prompt.

Step 8 — Claude

Claude Sonnet 4.6 generates the explanation.

Step 9 — References

The retrieved documents and page numbers are returned with the answer.

Step 10 — Streamlit

The final answer and references are displayed to the user.

25. Security

Sensitive configuration values should not be committed to the repository.

The following should remain private:

.env
API keys
credentials
tokens

The .gitignore file should prevent sensitive files from being tracked by Git.

26. Deployment

NyumbaLex can be deployed using Streamlit Community Cloud.

The deployment configuration uses:

Repository: kenyan-family-law-chatbot
Branch: main
Main file: src/app.py

Dependencies are installed from:

requirements.txt

Secrets such as the Anthropic API key should be configured through Streamlit's secrets management rather than committed to the repository.

27. Future Improvements

Potential improvements include:

Expanding the legal document collection.
Adding more Kenyan legislation.
Adding Kenyan case law.
Improving retrieval accuracy.
Adding conversation memory.
Adding document upload functionality.
Improving citation accuracy.
Adding automated evaluation.
Adding multilingual support.
Adding Kiswahili support.
Improving accessibility.
Adding authentication for restricted deployments.

28. Project Significance

NyumbaLex demonstrates how multiple AI and NLP techniques can be combined to solve a practical problem.

The project brings together:

NLP
+
Machine Learning
+
Named Entity Recognition
+
Semantic Search
+
Vector Databases
+
Retrieval-Augmented Generation
+
Large Language Models
+
Web Application Development

The result is a domain-specific AI assistant capable of retrieving information from Kenyan family-law documents and presenting it in a more accessible form.

Author

Developed as an NLP and AI project focused on applying artificial intelligence to legal information retrieval and accessibility by Drina Musili.



NyumbaLex is an AI-powered legal information tool. It is not a law firm, does not provide legal representation, and does not replace professional legal advice. Users should consult a qualified Kenyan legal professional for advice regarding their specific circumstances.