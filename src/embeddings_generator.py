"""
Embedding Generator

Creates sentence embeddings for every chunk
using Sentence Transformers.
"""

from sentence_transformers import SentenceTransformer 
import numpy as np 


class EmbeddingGenerator:

    def __init__(self):

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        print("Model loaded.\n")

    def generate_embeddings(self, chunks): 

        texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True,
            convert_to_numpy=True
        )

        print(f"\nGenerated {len(embeddings)} embeddings.")

        return embeddings

#test
from pdf_loader import PDFLoader
from chunker import TextChunker

if __name__ == "__main__":

    loader = PDFLoader("data/raw")
    documents = loader.load_documents()

    chunker = TextChunker()

    chunks = chunker.chunk_documents(documents)

    generator = EmbeddingGenerator()

    embeddings = generator.generate_embeddings(chunks)

    print("\nEmbedding Shape:")

    print(embeddings.shape)

    print("\nFirst embedding (first 10 values):")

    print(embeddings[0][:10])    