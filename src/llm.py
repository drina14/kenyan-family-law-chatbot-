import os #import the os module to interact with the operating system, such as reading environment variables and creating directories.
from anthropic import Anthropic #import the Anthropic class from the anthropic module to interact with the Anthropic API for generating responses from the Claude LLM.
from dotenv import load_dotenv #import the load_dotenv function from the dotenv module to load environment variables from a .env file.
from config import MODEL_NAME #import the MODEL_NAME constant from the config module to specify which model to use for generating responses.

load_dotenv()


class ClaudeLLM:

    def __init__(self): #Initializes the Claude API client and sends a prompt to generate a response from the LLM.
        self.client = Anthropic(
            api_key=os.getenv("ANTHROPIC_API_KEY") #Retrieves the API key from the environment variable
        )

    def generate_response(self, prompt):

        response = self.client.messages.create( #Sends a request to Claude to generate a response.
           model=MODEL_NAME,
            max_tokens=1000,
            temperature=0, #Sets the randomness of the model's response.
            messages=[ #Sends the constructed prompt as the user's message to Claude.
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.content[0].text #Extracts and returns the generated text from Claude's response.