import os
import streamlit as st
from dotenv import load_dotenv
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.models.openai._openai_client import ModelInfo, ModelFamily

# Load from .env for local development
load_dotenv()

def get_model_client():
    # Try Streamlit secrets first (for cloud deployment), then fall back to env variables (for local)
    try:
        open_router_api_key = st.secrets["OPEN_ROUTER_API_KEY"]
    except (KeyError, FileNotFoundError):
        open_router_api_key = os.getenv("OPEN_ROUTER_API_KEY") or os.getenv("open_router_api_key")
    
    # Validate that we have an API key
    if not open_router_api_key:
        raise ValueError(
            "OpenRouter API key not found. Please set OPEN_ROUTER_API_KEY in:\n"
            "- Streamlit Cloud: App Settings > Secrets\n"
            "- Locally: .streamlit/secrets.toml or .env file"
        )
    
    # Create model info for DeepSeek
    model_info = ModelInfo(
        vision=False,
        function_calling=True,
        json_output=True,
        family=ModelFamily.UNKNOWN,
        context_window=128000,  # Adjust based on DeepSeek's actual context window
    )
    
    open_router_model_client = OpenAIChatCompletionClient(
        base_url="https://openrouter.ai/api/v1",
        model="deepseek/deepseek-chat-v3.1:free",
        api_key=open_router_api_key,
        model_info=model_info
    )
    
    return open_router_model_client