"""
Text Chunking Module

Splits extracted PDF text into overlapping chunks
while preserving metadata.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter 


class TextChunker:

    def __init__(self, chunk_size=500, chunk_overlap=100): 

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                ""
            ]
        )

    def chunk_documents(self, documents):

        chunks = []

        chunk_id = 1

        for doc in documents:  

            split_text = self.splitter.split_text(doc["text"])

            for piece in split_text:

                chunks.append({
                    "chunk_id": chunk_id,
                    "document_name": doc["document_name"],
                    "page_number": doc["page_number"],
                    "text": piece
                })

                chunk_id += 1

        return chunks

from pdf_loader import PDFLoader 

#test
if __name__ == "__main__":

    loader = PDFLoader("data/raw")
    documents = loader.load_documents()

    chunker = TextChunker()

    chunks = chunker.chunk_documents(documents)

    print(f"\nTotal Pages Loaded: {len(documents)}")
    print(f"Total Chunks Created: {len(chunks)}")

    print("\n=== SAMPLE CHUNK ===\n")

    print(chunks[0])    