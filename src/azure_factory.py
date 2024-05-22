from openai import AsyncAzureOpenAI

# local
from src.config import settings


class AzureOpenAIFactory:
    def __init__(self):
        self.settings = settings

    def create(self):
        return AsyncAzureOpenAI(
            azure_endpoint=self.settings["AZURE_OPENAI_API_BASE_URL"],
            api_key=self.settings["AZURE_OPENAI_API_KEY"],
            api_version=self.settings["AZURE_OPENAI_API_VERSION"],
        )


if __name__ == "__main__":
    # poetry run python -m src.azure_factory
    factory = AzureOpenAIFactory()
    openai = factory.create()
    print(openai)
