from flask import Flask, request, jsonify
from pydantic import ValidationError

# local
from src.azure_factory import AzureOpenAIFactory
from src.config import settings
from src.response_generator import ResponseGenerator
from src.models import UserInput

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


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


if __name__ == "__main__":
    # poetry run flask --app src/main run
    app.run(debug=True)
