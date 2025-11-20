from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    AZURE_OPENAI_ENDPOINT: str
    AZURE_OPENAI_KEY: str
    AZURE_OPENAI_GPT4o_VERSION: str
    AZURE_OPENAI_EMBEDDING_VERSION: str

    class Config:
        env_file = ".env"

settings = Settings()
