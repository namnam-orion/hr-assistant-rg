from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    azure_oai_endpoint: str
    azure_oai_key: str
    azure_oai_deployment: str
    azure_search_endpoint: str
    azure_search_key: str
    azure_search_index: str

    class Config:
        env_file = ".env"

settings = Settings()
