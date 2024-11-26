from os import system
import streamlit as st
from service.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id
from config.settings import DEFAULT_API_KEY, DEFAULT_TEMPERATURE


class Chatbot:
    def __init__(self, page_title="TemanTenang | Tim 7 CendekiAwan"):
        self.instance_id = get_instance_id()
        self.page_title = page_title

        if "chat_manager" not in st.session_state:
            st.session_state["chat_manager"] = ConversationManager()

        self.chat_manager = st.session_state["chat_manager"]

        if "conversation_history" not in st.session_state:
            st.session_state["conversation_history"] = (
                self.chat_manager.conversation_history
            )

        self.conversation_history = st.session_state["conversation_history"]

    def generate_ui(self):
        st.set_page_config(page_title=self.page_title, page_icon="❤️")
        st.title("TemanTenang")
        st.write(f"**EC2 Instance ID**: {self.instance_id}")
        self._display_sidebar()
        user_input = st.chat_input("Write a message")
        if user_input:
            self._display_conversation_history(user_input)

    def _display_user_input(self, user_input: str):
        with st.chat_message("user"):
            st.write(user_input)

    def _display_assistant_response(self, user_input):
        temperature = st.session_state.get("temperature", DEFAULT_TEMPERATURE)
        response_stream = self.chat_manager.chat_completion(
            prompt=user_input, stream=True, temperature=temperature
        )
        with st.chat_message("assistant"):
            streamed_response = st.write_stream(response_stream)

        self.conversation_history.append(
            {"role": "assistant", "content": streamed_response}
        )

    def _display_conversation_history(self, user_input: str):
        for message in self.conversation_history:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        self._display_user_input(user_input)
        self._display_assistant_response(user_input)

    def _display_sidebar(self):
        with st.sidebar:     
             st.header("API Key Settings") 
             api_key = st.text_input("Enter your API Key", type="password", key="api_key_input")
             save_api_key = st.button("Save API Key")
             reset_api_key = st.button("Reset to Default")

        if save_api_key:
            if api_key.strip() == "":
                st.error("API Key cannot be empty.")
            else:
                st.session_state["api_key"] = api_key
                self.chat_manager.set_api_key(api_key)
                st.success("API Key saved successfully!")
            if reset_api_key:
                default_api_key = DEFAULT_API_KEY
                st.session_state["api_key"] = default_api_key
                self.chat_manager.set_api_key(default_api_key)
            st.success("API Key reset to default successfully!")
