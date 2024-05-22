from flask import Flask, request, jsonify
from pydantic import ValidationError

# local
from src.azure_factory import AzureOpenAIFactory
from src.config import settings
from src.response_generator import ResponseGenerator
from src.models import UpdateScoresInput, UserInput

app = Flask(__name__)

# This is the temporal solution for storing scores
# Global variable for scores
SCORES = {
    settings.AZURE_MODEL_PREFIX + "-gpt-35-turbo": 0,
    settings.AZURE_MODEL_PREFIX + "-gpt4-turbo-2024-04-09": 0,
    settings.AZURE_MODEL_PREFIX + "-gpt4-1106-se": 0,
}


@app.route("/")
def hello_world():
    return "Check /generate, /feedback, /scores"


@app.route("/generate", methods=["POST"])
async def generate():
    try:
        data = UserInput(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors(), status=400)
    factory = AzureOpenAIFactory(settings)
    generator = ResponseGenerator(factory)
    responses = await generator.generate_response(data.prompt)
    return jsonify(responses)


@app.route("/feedback", methods=["POST"])
def feedback():
    try:
        data = UpdateScoresInput(**request.get_json())
    except ValidationError as e:
        return jsonify(e.errors(), status=400)
    """
      these methods could be used for actual database storage
      factory = AzureOpenAIFactory(settings)
      factory.update_scores(data.model_responses, data.user_feedback) 
    """
    # Temporal solution for storing scores
    res = {}
    for model_response in data.model_responses:
        res[model_response.blind_name] = model_response.full_name

    if data.user_feedback == "A":
        SCORES[res.get("A", "")] = SCORES.get(res.get("A", ""), 0) + 1
    elif data.user_feedback == "B":
        SCORES[res.get("B", "")] = SCORES.get(res.get("B", ""), 0) + 1
    elif data.user_feedback == "tie":
        pass  # No need to do anything if it's a tie
    elif data.user_feedback == "bad":
        SCORES[res.get("A", "")] = SCORES.get(res.get("A", ""), 0) - 1
        SCORES[res.get("B", "")] = SCORES.get(res.get("B", ""), 0) - 1
    else:
        raise ValueError("Invalid feedback")
    return jsonify({"message": "Feedback received"})


@app.route("/scores", methods=["GET"])
def get_scores():
    return jsonify(SCORES)


if __name__ == "__main__":
    # poetry run flask --app src/main run
    app.run(debug=True)
