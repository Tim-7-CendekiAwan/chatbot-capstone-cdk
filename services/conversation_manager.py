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
        api_key=DEFAULT_API_KEY,
        base_url=DEFAULT_BASE_URL,
        model=DEFAULT_MODEL,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        token_budget=DEFAULT_TOKEN_BUDGET,
    ):

        self.client = OpenAI(api_key=api_key, base_url=base_url)

        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.token_budget = token_budget

        self.system_message = """You are a friendly and supportive guide. 
                    You answer questions with kindness, encouragement, and patience, 
                    always looking to help the user feel comfortable and confident. 
                    You should act as a professional mental health conselor"""
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
        self,
        prompt,
        temperature=DEFAULT_TEMPERATURE,
        max_tokens=DEFAULT_MAX_TOKENS,
        model=DEFAULT_MODEL,
        stream=False,
    ):
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
