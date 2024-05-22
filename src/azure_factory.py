import random
from openai import AsyncAzureOpenAI

# local
from src.config import Settings
from src.models import Model, Feedback, ModelResponse


class AzureOpenAIFactory:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.models = {
            "gpt3": self.settings.AZURE_MODEL_PREFIX + "-gpt-35-turbo",
            "gpt4": self.settings.AZURE_MODEL_PREFIX + "-gpt4-turbo-2024-04-09",
            "gpt4-se": self.settings.AZURE_MODEL_PREFIX + "-gpt4-1106-se",
        }
        # this variable could be used for actual database storage
        self.scores = {
            self.models["gpt3"]: 0,
            self.models["gpt4"]: 0,
            self.models["gpt4-se"]: 0,
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

    # this method could be used for actual database storage
    def update_scores(
        self, model_responses: list[ModelResponse], user_feedback: Feedback
    ):
        res = {}
        for model_response in model_responses:
            res[model_response.blind_name] = model_response.full_name

        if user_feedback.user_feedback == "A":
            self.scores[res.get("A", "")] = self.scores.get(res.get("A", ""), 0) + 1
        elif user_feedback.user_feedback == "B":
            self.scores[res.get("B", "")] = self.scores.get(res.get("B", ""), 0) + 1
        elif user_feedback.user_feedback == "tie":
            pass  # No need to do anything if it's a tie
        elif user_feedback.user_feedback == "bad":
            self.scores[res.get("A", "")] = self.scores.get(res.get("A", ""), 0) - 1
            self.scores[res.get("B", "")] = self.scores.get(res.get("B", ""), 0) - 1
        else:
            raise ValueError("Invalid feedback")

    # this method could be used for actual database storage
    def get_scores(self):
        return self.scores


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
    print(factory.get_scores())
    factory.update_scores(
        [
            ModelResponse("A", "gpt3", "sometech-gpt-35-turbo", "response"),
            ModelResponse("B", "gpt4", "sometech-gpt4-turbo-2024-04-09", "response"),
        ],
        Feedback("A"),
    )
    print(factory.get_scores())
