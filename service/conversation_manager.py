from openai import OpenAI
import tiktoken
from config.settings import (
    DEFAULT_API_KEY,
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    DEFAULT_TEMPERATURE,
    DEFAULT_MAX_TOKENS,
    DEFAULT_TOKEN_BUDGET,
  
)


class ConversationManager:
    def __init__(
        self, api_key=DEFAULT_API_KEY, 
        base_url=DEFAULT_BASE_URL, 
        model=DEFAULT_MODEL
        ):

        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)
        self.model = model
        self.system_message = "You are a helpful assistant."
        self.conversation_history = [{"role": "system", "content": self.system_message}]

    def set_api_key(self, api_key):
        self.api_key = api_key
        self.client = OpenAI(api_key=self.api_key, base_url=self.client.base_url)
        
    def reset_api_key(self):
        self.api_key = DEFAULT_API_KEY

    def chat_completion(self, prompt, stream=False):
        if not self.api_key:
            raise ValueError("API Key is not set.")

        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                stream=stream,
            )
            if stream:
                return response
        except Exception as e:
            print(f"Error generating response: {e}")
            return None

        ai_response = response.choices[0].message.content
        self.conversation_history.append({"role": "assistant", "content": ai_response})

        return ai_response