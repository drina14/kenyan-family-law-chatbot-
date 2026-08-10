"""
Vector Store Module

Creates, saves, loads and searches
a FAISS vector index.

the retrieval engine — given a question, it finds the most relevant law chunks.
"""
print("vector_store.py started")

import os # import the os module for interacting with the operating system ; handling file paths.
import pickle # library for saving and loading Python objects.
import faiss #import the FAISS library for efficient similarity search and clustering of dense vectors.
import numpy as np # import the numpy library for numerical operations, particularly for handling arrays and matrices.

from sentence_transformers import SentenceTransformer # import the SentenceTransformer class from the sentence_transformers library to generate embeddings for text chunks.
class VectorStore:

    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2") #loads the embedding model into memory.
        self.index = None
        self.chunks = None

    def build_index(self, embeddings, chunks): #builds the vector database that allows the chatbot to search legal documents efficiently.
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))

        self.chunks = chunks

        print(f"\nIndexed {self.index.ntotal} chunks.")

    def save(self):  #saves the FAISS index and the corresponding chunks to disk for later retrieval.
        os.makedirs("data/embeddings", exist_ok=True)

        faiss.write_index(
            self.index,
            "data/embeddings/faiss_index.bin"
        )

        with open("data/embeddings/chunks.pkl", "wb") as file:
            pickle.dump(self.chunks, file)

        print("\nVector store saved.")

    def load(self): #loads it back into memory so your chatbot can immediately start searching documents
        self.index = faiss.read_index(
            "data/embeddings/faiss_index.bin"
        )

        with open("data/embeddings/chunks.pkl", "rb") as file:
            self.chunks = pickle.load(file)

        print("\nVector store loaded.")

    def search(self, question, top_k=5): #find the most relevant document chunks for a user's question.
        query_embedding = self.embedding_model.encode(
            [question],
            convert_to_numpy=True
        )

        distances, indices = self.index.search(
            query_embedding.astype(np.float32),
            top_k
        )

        results = []

        for distance, idx in zip(distances[0], indices[0]):
            chunk = self.chunks[idx].copy()
            similarity = 1 / (1 + distance)
            chunk["similarity_score"] = round(float(similarity), 3)
            results.append(chunk)

        return results
from pdf_loader import PDFLoader #import the PDFLoader class from the pdf_loader module.
from chunker import TextChunker #import the TextChunker class from the chunker module.
from embeddings_generator import EmbeddingGenerator #import the EmbeddingGenerator class from the embeddings_generator module.

#test
if __name__ == "__main__":

    loader = PDFLoader("data/raw")
    documents = loader.load_documents()

    chunker = TextChunker()
    chunks = chunker.chunk_documents(documents)

    generator = EmbeddingGenerator()
    embeddings = generator.generate_embeddings(chunks)

    store = VectorStore()

    store.build_index(
        embeddings,
        chunks
    )

    store.save()

    print("\nSearching...\n")

    results = store.search(
        "Can a widow inherit land?"
    )

    for i, result in enumerate(results, 1):

        print(f"\nResult {i}")

        print(f"Document : {result['document_name']}")

        print(f"Page : {result['page_number']}")

        print(result["text"][:300])

        print("-" * 60)    