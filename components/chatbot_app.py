import streamlit as st
from services.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id


class Chatbot:
    def __init__(self, page_title="TemanTenang | Tim 7 CendekiAwan"):
        self.instance_id = get_instance_id()
        self.page_title = page_title

    def GenerateUI(self):
        st.set_page_config(page_title=self.page_title)

        ### Streamlit code ###
        st.title("TemanTenang")

        # # Display EC2 Instance ID
        st.write(f"**EC2 Instance ID**: {self.instance_id}")

        self.display_sidebar()

        # Initialize the ConversationManager object
        if "chat_manager" not in st.session_state:
            st.session_state["chat_manager"] = ConversationManager()

        chat_manager = st.session_state["chat_manager"]

        if "conversation_history" not in st.session_state:
            st.session_state["conversation_history"] = chat_manager.conversation_history

        conversation_history = st.session_state["conversation_history"]

        # Chat input from the user
        user_input = st.chat_input("Write a message")

        # Call the chat manager to get a response from the AI
        if user_input:
            response = chat_manager.chat_completion(user_input)

        # Display the conversation history
        for message in conversation_history:
            if message["role"] != "system":
                with st.chat_message(message["role"]):
                    st.write(message["content"])

    def display_sidebar(self):
        with st.sidebar:
            personality = st.selectbox("Select personality", ("Formal", "Casual"))
