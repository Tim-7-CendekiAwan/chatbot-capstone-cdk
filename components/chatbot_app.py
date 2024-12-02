import streamlit as st
from services.conversation_manager import ConversationManager
from util.get_instance_id import get_instance_id
from config.settings import DEFAULT_TEMPERATURE
from streamlit_chat import message 
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
        else :
            self._display_conversation_history()

    def _display_user_input(self, user_input: str):
        self._send_message(user_input, is_user=True)

    def _display_assistant_response(self, user_input):
        temperature = st.session_state.get("temperature", DEFAULT_TEMPERATURE)
        response_stream = self.chat_manager.chat_completion(
            prompt=user_input, stream=False, temperature=temperature
        )
        self._send_message(response_stream, is_user=False)
        self.conversation_history.append(
            {"role": "assistant", "content":  response_stream}
        )

    def _display_conversation_history(self, user_input: str = None):
       for idx, msg in enumerate(self.conversation_history):
            if msg["role"] != "system":
                is_user_message = msg["role"] != "assistant"
                self._send_message(msg["content"], is_user=is_user_message, idx=idx)
       if user_input:
            self._display_user_input(user_input)
            self._display_assistant_response(user_input)

    def _display_sidebar(self):
        with st.sidebar:
            toggle_custom_persona = st.toggle("Use custom persona", value=False)
            persona = self._display_persona_option(disabled=toggle_custom_persona)
            self._handle_persona_changes(
                persona=persona, toggle_custom_persona=toggle_custom_persona
            )

            temperature = st.slider(
                "Temperature",
                min_value=0.0,
                max_value=1.0,
                value=DEFAULT_TEMPERATURE,
                step=0.01,
                help="Adjusment randomness of chatbot response."
            )

            st.session_state["temperature"] = temperature

    def _display_persona_option(self, disabled=False):
        personalities = ("Professional", "Empathetic", "Motivational")
        return st.selectbox("Select personality", personalities, disabled=disabled)

    def _handle_persona_changes(
        self, persona="Professional", toggle_custom_persona=False
    ):
        if toggle_custom_persona:
            custom_persona = st.text_area(
                "Define your own persona for the chatbot",
                placeholder="e.g. You are a software engineer who love to help others",
            )
            self._set_user_defined_persona(custom_persona)
        else:
            self._set_predefined_persona(persona)

    def _set_user_defined_persona(self, user_prompt: str):
        save_custom_persona = st.button(
            "Save", icon=":material/save:", use_container_width=True
        )
        if user_prompt and save_custom_persona:
            self._handle_custom_persona(user_prompt)

    def _handle_custom_persona(self, user_prompt: str):
        custom_persona = user_prompt
        self.chat_manager.set_system_persona(custom_persona)

    def _set_predefined_persona(self, persona="Professional"):
        persona_prompt = f"""The user has selected {persona} persona.
            Respond accordingly throughout this conversation."""
        system_message_with_chosen_persona = (
            self.chat_manager.system_message + persona_prompt
        )

        self.chat_manager.set_system_persona(system_message_with_chosen_persona)
    
    def _send_message(self, message_content, is_user: bool = False, idx: int = None):
        message_idx = idx if idx is not None else len(self.conversation_history)
        key = f"user_{message_idx}" if is_user else f"assistant_{message_idx}"
        avatar_style = "micah" if is_user else "boots"
        message(message_content, is_user=is_user, key=key, avatar_style=avatar_style if is_user else None)
