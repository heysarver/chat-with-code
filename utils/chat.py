from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI

def chat(temperature: float = 0.2, provider: str = "openai", model_name: str = "gpt-4-0125-preview"):
    if provider == "anthropic":
        model = chat_anthropic(temperature=temperature, model_name=model_name)
    return model

def chat_anthropic(temperature: float = 0.2, model_name: str = "claude-3-sonnet-20240229"):
    model = ChatAnthropic(temperature=temperature, model_name=model_name)
    return model

def chat_openai(temperature: float = 0.2, model_name: str = "gpt-4-0125-preview"):
    model = ChatOpenAI(temperature=temperature, model_name=model_name)
    return model
