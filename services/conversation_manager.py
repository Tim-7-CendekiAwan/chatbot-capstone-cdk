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
        self,
        api_key=None,
        base_url=None,
        model=None,
        temperature=None,
        max_tokens=None,
        token_budget=None,
    ):
        if not api_key:
            api_key = DEFAULT_API_KEY
        if not base_url:
            base_url = DEFAULT_BASE_URL

        self.client = OpenAI(api_key=api_key, base_url=base_url)

        self.model = model if model else DEFAULT_MODEL
        self.temperature = temperature if temperature else DEFAULT_TEMPERATURE
        self.max_tokens = max_tokens if max_tokens else DEFAULT_MAX_TOKENS
        self.token_budget = token_budget if token_budget else DEFAULT_TOKEN_BUDGET

        self.system_message = """You are a friendly and supportive guide. 
                    You answer questions with kindness, encouragement, and patience, 
                    always looking to help the user feel comfortable and confident. 
                    You should act as a professional mental health conselor"""  # Default persona
        self.conversation_history = [{"role": "system", "content": self.system_message}]

    def count_tokens(self, text):
        try:
            encoding = tiktoken.encoding_for_model(self.model)
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
        tokens = encoding.encode(text)
        return len(tokens)

    def total_tokens_used(self):
        try:
            return sum(
                self.count_tokens(message["content"])
                for message in self.conversation_history
            )
        except Exception as e:
            print(f"Error calculating total tokens used: {e}")
            return None

    def enforce_token_budget(self):
        try:
            while self.total_tokens_used() > self.token_budget:
                if len(self.conversation_history) <= 1:
                    break
                self.conversation_history.pop(1)
        except Exception as e:
            print(f"Error enforcing token budget: {e}")

    def chat_completion(
        self, prompt, temperature=None, max_tokens=None, model=None, stream=False
    ):
        temperature = temperature if temperature is not None else self.temperature
        max_tokens = max_tokens if max_tokens is not None else self.max_tokens
        model = model if model is not None else self.model

        self.conversation_history.append({"role": "user", "content": prompt})
        self.enforce_token_budget()

        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=self.conversation_history,
                temperature=temperature,
                max_tokens=max_tokens,
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

    def reset_conversation_history(self):
        self.conversation_history = [{"role": "system", "content": self.system_message}]
