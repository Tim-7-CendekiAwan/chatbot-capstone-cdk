import streamlit as st
from services.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id
from config.settings import DEFAULT_TEMPERATURE


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
        response_stream = self.chat_manager.chat_completion(
            prompt=user_input, stream=True
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
        personalities = ["Formal", "Casual", "Friendly"]
        with st.sidebar:
            chosen_persona = st.selectbox("Select personality", personalities)
            self._set_chatbot_persona(chosen_persona)

            temperature = st.slider(
                "Set Temperature",
                min_value=0.0,
                max_value=1.0,
                value=DEFAULT_TEMPERATURE,
                step=0.01,
                help="Adjusment randomness of chatbot response."
            )

            st.session_state['temperature'] = temperature

    def _set_chatbot_persona(self, persona: str = "Formal"):
        system_message = f"""You are a friendly and supportive guide. 
                    You answer questions with kindness, encouragement, and patience, 
                    always looking to help the user feel comfortable and confident. 
                    You should act as a professional mental health conselor. 
                    Also, use a {persona} tone"""

        system_role = self.conversation_history[0]
        system_role.update({"content": system_message})

        self.conversation_history[0] = system_role
