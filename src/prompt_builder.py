"""
Builds the prompt that will be sent to the Large Language Model (LLM) 
by combining the user's question, detected intent, entities, and retrieved legal context.
"""


class PromptBuilder:

    @staticmethod #Declares build_prompt() as a static method.
    def build_prompt(question, intent, entities, retrieved_chunks):

        # Build the context from retrieved chunks
        context = ""

        for chunk in retrieved_chunks:

            context += (
                f"Document: {chunk['document_name']}\n"
                f"Page: {chunk['page_number']}\n"
                f"Similarity: {chunk['similarity_score']}\n\n"
                f"{chunk['text']}\n"
                f"{'-'*60}\n\n"
            )

        # Format entities nicely
        entity_text = ", ".join(entities) if entities else "None"

        prompt = f"""
You are an AI Legal Assistant specializing in Kenyan Family Law.

Your task is to answer ONLY using the legal context provided below.

Rules:
1. Do NOT make up legal information.
2. If the answer is not contained in the retrieved context, clearly state that the information was not found in the provided legal documents.
3. Keep the answer professional but easy to understand.
4. Mention which legal document(s) you relied on.
5. Do not claim to be a lawyer or give definitive legal advice.

Detected Intent:
{intent}

Named Entities:
{entity_text}

Retrieved Legal Context:
{context}

User Question:
{question}

Provide your response in this format:

Answer:
...

Explanation:
...

Sources:
...
"""

        return prompt