from dataclasses import dataclass
from typing import Literal

from pydantic import BaseModel


@dataclass
class Model:
    blind_name: str  # A or B
    display_name: str  # e.g., gpt3
    full_name: str  # e.g., sometech-gpt-35-turbo


@dataclass
class Feedback:
    user_feedback: Literal["A", "B", "tie", "bad"]


@dataclass
class ModelResponse:
    blind_name: Literal["A", "B"]  # A or B
    display_name: str  # e.g., gpt3
    full_name: str  # e.g., sometech-gpt-35-turbo
    response: str  # answer from a model


class UserInput(BaseModel):
    prompt: str


class UpdateScoresInput(BaseModel):
    model_responses: list[ModelResponse]
    user_feedback: Literal["A", "B", "tie", "bad"]
