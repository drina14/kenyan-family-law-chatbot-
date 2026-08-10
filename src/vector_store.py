"""
Vector Store Module

Creates, saves, loads and searches
a FAISS vector index.

the retrieval engine — given a question, it finds the most relevant law chunks.
"""
print("vector_store.py started")

import os 
import pickle 
import faiss 
import numpy as np 

from sentence_transformers import SentenceTransformer 
class VectorStore:

    def __init__(self):
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2") 
        self.index = None
        self.chunks = None

    def build_index(self, embeddings, chunks): 
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings.astype(np.float32))

        self.chunks = chunks

        print(f"\nIndexed {self.index.ntotal} chunks.")

    def save(self):  
        os.makedirs("data/embeddings", exist_ok=True)

        faiss.write_index(
            self.index,
            "data/embeddings/faiss_index.bin"
        )

        with open("data/embeddings/chunks.pkl", "wb") as file:
            pickle.dump(self.chunks, file)

        print("\nVector store saved.")

    def load(self): 
        self.index = faiss.read_index(
            "data/embeddings/faiss_index.bin"
        )

        with open("data/embeddings/chunks.pkl", "rb") as file:
            self.chunks = pickle.load(file)

        print("\nVector store loaded.")

    def search(self, question, top_k=5): 
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
from pdf_loader import PDFLoader 
from chunker import TextChunker 
from embeddings_generator import EmbeddingGenerator 

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