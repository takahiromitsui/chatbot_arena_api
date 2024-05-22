from flask import Flask
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    # poetry run flask --app src/main run
    app.run(debug=True)
