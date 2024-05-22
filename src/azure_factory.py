from dataclasses import dataclass
import random
from openai import AsyncAzureOpenAI

# local
from src.config import Settings


@dataclass
class Model:
    blind_name: str  # A or B
    display_name: str  # e.g., gpt3
    full_name: str  # e.g., sometech-gpt-35-turbo


class AzureOpenAIFactory:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.models = {
            "gpt3": self.settings.AZURE_MODEL_PREFIX + "-gpt-35-turbo",
            "gpt4": self.settings.AZURE_MODEL_PREFIX + "-gpt4-turbo-2024-04-09",
            "gpt4-se": self.settings.AZURE_MODEL_PREFIX + "-gpt4-1106-se",
        }

    def create(self):
        return AsyncAzureOpenAI(
            azure_endpoint=self.settings.AZURE_OPENAI_API_BASE_URL,
            api_key=self.settings.AZURE_OPENAI_API_KEY,
            api_version=self.settings.AZURE_OPENAI_API_VERSION,
        )

    def pick_two_random_models(self) -> list[Model]:
        keys = random.sample(list(self.models.keys()), 2)
        blind_names = ["A", "B"]
        models = []
        for i, key in enumerate(keys):
            model = Model(blind_names[i], key, self.models[key])
            models.append(model)
        return models


if __name__ == "__main__":
    # poetry run python -m src.azure_factory
    settings = Settings(
        AZURE_OPENAI_API_BASE_URL="random_base_url",
        AZURE_OPENAI_API_KEY="random_api_key",
        AZURE_OPENAI_API_VERSION="random_api_version",
        AZURE_MODEL_PREFIX="random_model_prefix",
    )
    factory = AzureOpenAIFactory(settings)
    client = factory.create()
    random_two_models = factory.pick_two_random_models()
    print(random_two_models)
