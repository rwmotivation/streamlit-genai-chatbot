import os

from dotenv import load_dotenv
import streamlit as st
from langchain_groq import ChatGroq


load_dotenv()


PROVIDERS = {
    "OpenAI": ["gpt-3.5-turbo", "gpt-4.1"],
    "Gemini": ["gemini-2.5-pro", "gemini-2.5-flash"],
    "Groq": ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
    "Ollama": ["gemma3", "llama3.1"],
}


def call_openai(model: str, messages: list[dict]) -> str:
    # Placeholder implementation – add real OpenAI call here when ready.
    return f"(Demo response from OpenAI {model}. Real API call not yet configured.)"


def call_gemini(model: str, messages: list[dict]) -> str:
    # Placeholder implementation – add real Gemini call here when ready.
    return f"(Demo response from Gemini {model}. Real API call not yet configured.)"


def call_groq(model: str, messages: list[dict]) -> str:
    llm = ChatGroq(
        model=model,
        temperature=0.0,
        api_key=os.getenv("GROQ_API_KEY"),
    )
    response = llm.invoke(input=messages)
    return response.content


def call_ollama(model: str, messages: list[dict]) -> str:
    # Placeholder implementation – add real Ollama call here when ready.
    return f"(Demo response from Ollama {model}. Real API call not yet configured.)"


def get_response(provider: str, model: str, messages: list[dict]) -> str:
    if provider == "OpenAI":
        return call_openai(model, messages)
    if provider == "Gemini":
        return call_gemini(model, messages)
    if provider == "Groq":
        return call_groq(model, messages)
    if provider == "Ollama":
        return call_ollama(model, messages)
    return "Unknown provider selected."


st.set_page_config(
    page_title="Multi-Provider Chatbot",
    page_icon="🤖",
    layout="centered",
)
st.title("💬 Multi-Provider Generative AI Chatbot")


if "chat_history" not in st.session_state:
    st.session_state.chat_history = []


with st.sidebar:
    st.header("Model settings")
    provider = st.selectbox("Provider", list(PROVIDERS.keys()), index=2)
    model = st.selectbox("Model", PROVIDERS[provider])


for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


user_prompt = st.chat_input("Type your message...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})

    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    messages.extend(st.session_state.chat_history)

    assistant_response = get_response(provider, model, messages)

    st.session_state.chat_history.append(
        {"role": "assistant", "content": assistant_response}
    )

    with st.chat_message("assistant"):
        st.markdown(assistant_response)

