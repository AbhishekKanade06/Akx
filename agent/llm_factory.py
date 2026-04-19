from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
import config
from .tools.registry import ALL_TOOLS

def make_llm(enable_tools: bool = True):
    if config.PROVIDER == "groq":
        llm = ChatGroq(
            model=config.MODEL,
            api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )

    elif config.PROVIDER == "google":
        llm = ChatGoogleGenerativeAI(
            model=config.MODEL,
            google_api_key=config.API_KEY,
            max_tokens=config.MAX_TOKENS,
        )

    elif config.PROVIDER in ("openai", "ollama"):
        kwargs = dict(model=config.MODEL, api_key=config.API_KEY, max_tokens=config.MAX_TOKENS)
        if config.BASE_URL:
            kwargs["base_url"] = config.BASE_URL
        llm = ChatOpenAI(**kwargs)
    else:
        raise ValueError(f"Unsupported provider: {config.PROVIDER}")

    if enable_tools:
        return llm.bind_tools(ALL_TOOLS)
    return llm
