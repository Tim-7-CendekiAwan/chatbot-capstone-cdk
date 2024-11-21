import streamlit as st
from services.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id


class Chatbot(ConversationManager):
    def __init__(self, page_title="TemanTenang | Tim 7 CendekiAwan"):
        self.instance_id = get_instance_id()
        self.page_title = page_title
        super().__init__()

    def GenerateUI(self):
        st.set_page_config(
            page_title=self.page_title, page_icon="❤️", initial_sidebar_state="auto"
        )

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

        # update system role message
        self.conversation_history[0] = SYSTEM_ROLE
