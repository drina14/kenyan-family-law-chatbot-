"""
PDF Loader Module

Reads all PDF files from data/raw/
and extracts their text.
"""

from pathlib import Path 
import fitz 


class PDFLoader:

    def __init__(self, pdf_directory):
        self.pdf_directory = Path(pdf_directory)

    def load_documents(self):

        documents = []

        pdf_files = list(self.pdf_directory.glob("*.pdf"))

        print(f"\nFound {len(pdf_files)} PDF files.\n")

        for pdf_file in pdf_files:

            print(f"Reading: {pdf_file.name}")

            document = fitz.open(pdf_file)

            for page in document:

                page_text = page.get_text().strip()

                if not page_text:
                    continue

                documents.append({
                    "document_name": pdf_file.stem,
                    "page_number": page.number + 1,
                    "text": page_text
                })

        return documents


# Test
if __name__ == "__main__":

    loader = PDFLoader("data/raw")

    documents = loader.load_documents()

    print("\n=== DOCUMENT SUMMARY ===\n")

    for doc in documents:
        print(doc["document_name"])
        print(f"Characters: {len(doc['text'])}")
        print("-" * 50)