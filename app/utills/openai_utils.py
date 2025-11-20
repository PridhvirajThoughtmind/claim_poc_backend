import json
from openai import AzureOpenAI

from app.core.settings import settings

def get_openai_llm() -> AzureOpenAI:
    """
    Initialize an Azure OpenAI client for LLM interactions.

    Returns:
        AzureOpenAI: Configured Azure OpenAI client for LLM.
    """
    print("inside get_azure_openai_llm")
    return AzureOpenAI(
    azure_endpoint=settings.AZURE_OPENAI_ENDPOINT,
    api_key=settings.AZURE_OPENAI_KEY,
    api_version=settings.AZURE_OPENAI_GPT4o_VERSION,
    azure_deployment="gpt-4o-mini",
)



