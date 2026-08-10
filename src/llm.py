import os 
from anthropic import Anthropic 
from dotenv import load_dotenv 
from config import MODEL_NAME 

load_dotenv()


class ClaudeLLM:

    def __init__(self): 
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY") 
        )

    def generate_response(self, prompt):

        response = self.client.messages.create( 
           model=MODEL_NAME,
            max_tokens=1000,
            temperature=0, 
            messages=[ 
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text 