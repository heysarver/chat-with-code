from langchain_anthropic import ChatAnthropic

def new_chat_model(temperature: float = 0.2, provider: str = "voyageai", model_name: str = "claude-3-sonnet-20240229"):
    if provider == "anthropic":
        model = chat_anthropic(temperature=temperature, model_name=model_name)
    return model

def chat_anthropic(temperature: float = 0.2, model_name: str = "claude-3-sonnet-20240229"):
    model = ChatAnthropic(temperature=temperature, model_name=model_name)
    return model
