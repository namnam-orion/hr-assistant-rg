from openai import AzureOpenAI
from .settings import settings

client = AzureOpenAI(
    api_key=settings.azure_oai_key,
    api_version="2024-12-01-preview",
    azure_endpoint=settings.azure_oai_endpoint
)
