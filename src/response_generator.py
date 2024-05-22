import asyncio
from dataclasses import dataclass
from flask import json

# local
from src.azure_factory import AzureOpenAIFactory
from src.models import ModelResponse


class ResponseGenerator:
    def __init__(self, factory: AzureOpenAIFactory):
        self.factory = factory

    async def generate_response(self, prompt: str) -> list[ModelResponse]:
        client = self.factory.create()
        models = self.factory.pick_two_random_models()
        responses = []
        for model in models:
            completion = await client.chat.completions.create(
                model=model.full_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
            )
            res = json.loads(completion.model_dump_json(indent=2))
            message_content = res["choices"][0]["message"]["content"]
            data = {
                "blind_name": model.blind_name,
                "display_name": model.display_name,
                "full_name": model.full_name,
                "response": message_content,
            }
            responses.append(data)
        return responses


if __name__ == "__main__":
    # poetry run python -m src.response_generator
    from src.config import settings

    factory = AzureOpenAIFactory(settings)
    generator = ResponseGenerator(factory)
    responses = asyncio.run(generator.generate_response("What is the meaning of life?"))
    print(responses)
