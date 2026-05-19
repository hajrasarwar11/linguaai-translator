import streamlit as st
from datetime import datetime


DEFAULT_DICTIONARY = {
    "hello": "hola",
    "goodbye": "adiós",
    "thank you": "gracias",
    "please": "por favor",
    "yes": "sí",
    "no": "no",
    "water": "agua",
    "food": "comida",
    "love": "amor",
    "friend": "amigo",
    "beautiful": "hermoso",
    "house": "casa",
    "book": "libro",
    "time": "tiempo",
    "world": "mundo",
    "good morning": "buenos días",
    "good night": "buenas noches",
    "how are you": "cómo estás",
    "i love you": "te amo",
    "welcome": "bienvenido",
}


def init_session_state():
    defaults = {
        "page": "chat",
        "messages": [],
        "dictionary": DEFAULT_DICTIONARY.copy(),
        "favorites": [],
        "groq_model": "llama-3.1-8b-instant",
        "save_new_words": True,
        "total_api_calls": 0,
        "total_local_hits": 0,
        "app_version": "2.0.0",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
