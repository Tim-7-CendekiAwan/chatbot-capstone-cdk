import streamlit as st
from services.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id


class Chatbot(ConversationManager):
    def __init__(self, page_title="TemanTenang | Tim 7 CendekiAwan"):
        self.instance_id = get_instance_id()
        self.page_title = page_title
        super().__init__()

    def GenerateUI(self):
        st.set_page_config(page_title=self.page_title, page_icon="❤️")

        st.title("TemanTenang")

        st.write(f"**EC2 Instance ID**: {self.instance_id}")

        self.display_sidebar()

        if "chat_manager" not in st.session_state:
            st.session_state["chat_manager"] = ConversationManager()

        chat_manager = st.session_state["chat_manager"]

        if "conversation_history" not in st.session_state:
            st.session_state["conversation_history"] = chat_manager.conversation_history

        conversation_history = st.session_state["conversation_history"]

        user_input = st.chat_input("Write a message")

        if user_input:
            self._display_conversation_history(
                user_input, conversation_history, chat_manager
            )

    def _display_user_input(self, user_input: str):
        self.conversation_history.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

    def _display_streamed_response(
        self, chat_manager, user_input, conversation_history
    ):
        response_stream = chat_manager.chat_completion(prompt=user_input, stream=True)
        with st.chat_message("assistant"):
            streamed_response = st.write_stream(response_stream)

        conversation_history.append({"role": "assistant", "content": streamed_response})

    def _display_conversation_history(
        self, user_input: str, conversation_history, chat_manager
    ):
        for message in conversation_history:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

        self._display_user_input(user_input)

        self._display_streamed_response(chat_manager, user_input, conversation_history)

    def display_sidebar(self):
        PERSONALITIES = ["Formal", "Casual", "Friendly"]
        with st.sidebar:
            chosen_persona = st.selectbox("Select personality", PERSONALITIES)
            self.set_chatbot_persona(chosen_persona)

    def set_chatbot_persona(self, persona: str = "Formal"):
        SYSTEM_MESSAGE = f"""You are a friendly and supportive guide. 
                    You answer questions with kindness, encouragement, and patience, 
                    always looking to help the user feel comfortable and confident. 
                    You should act as a professional mental health conselor. Also, use a {persona} tone"""

        SYSTEM_ROLE = self.conversation_history[0]
        SYSTEM_ROLE.update({"content": SYSTEM_MESSAGE})

        self.conversation_history[0] = SYSTEM_ROLE
