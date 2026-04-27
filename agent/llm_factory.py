from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_anthropic import ChatAnthropic
import config

def make_llm(tools=None):
    provider = config.PROVIDER.lower()
    tools    = tools or []

    if provider == "groq":
        llm = ChatGroq(
            model=config.MODEL,
            api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )

    elif provider == "gemini":
        llm = ChatGoogleGenerativeAI(
            model=config.MODEL,
            google_api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )

    elif provider == "anthropic":
        llm = ChatAnthropic(
            model=config.MODEL,
            api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )

    elif provider in ("openai", "ollama", "openai-compatible"):
        kwargs = dict(
            model=config.MODEL,
            api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )
        if config.BASE_URL:
            kwargs["base_url"] = config.BASE_URL
        llm = ChatOpenAI(**kwargs)

    else:
        raise ValueError(
            f"Unsupported provider: '{provider}'. "
            "Choose: groq, gemini, anthropic, openai, ollama, openai-compatible"
        )

    return llm.bind_tools(tools) if tools else llm