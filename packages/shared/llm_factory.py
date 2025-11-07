from langchain_core.language_models import BaseChatModel

from shared.config import LLMProvider, Settings


def create_llm(settings: Settings) -> BaseChatModel:
    if settings.llm_provider == LLMProvider.AZURE:
        from langchain_mistralai import ChatMistralAI

        if not settings.azure_mistral_endpoint or not settings.azure_mistral_api_key:
            raise ValueError(
                "Azure Mistral endpoint and API key must be configured when using Azure provider"
            )

        return ChatMistralAI(
            endpoint=settings.azure_mistral_endpoint,
            mistral_api_key=settings.azure_mistral_api_key,
            model=settings.mistral_model,
            temperature=settings.model_temperature,
            max_retries=settings.model_max_retries,
            timeout=settings.model_timeout,
        )

    elif settings.llm_provider == LLMProvider.LOCAL:
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.model_temperature,
        )

    elif settings.llm_provider == LLMProvider.OPENAI:
        try:
            from langchain_openai import ChatOpenAI
        except ImportError:
            raise ImportError(
                "langchain-openai is not installed. Install it with: pip install langchain-openai"
            )

        if not settings.openai_api_key:
            raise ValueError("OpenAI API key must be configured when using OpenAI provider")

        return ChatOpenAI(
            model=settings.openai_model,
            temperature=settings.openai_temperature,
            api_key=settings.openai_api_key,
        )

    else:
        raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
