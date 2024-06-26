
# Chat Bot Arena API
I mocked [LMSYS Chatbot Arena: Benchmarking LLMs in the Wild](https://chat.lmsys.org/)'s functionality with RestAPI/Flask.
## Installation

This project uses Poetry for dependency management. To install Poetry, follow the instructions on the [Poetry website](https://python-poetry.org/docs/#installation).

Once you have Poetry installed, you can install the project dependencies with:

```bash
  poetry install
```
    
## Environment Variables

To run this project, you will need to add environment variables to your .env file. Please copy and paste .env.example to .env.

## Run Locally

To run the application, use the following command:

```bash
  poetry run flask --app src/main run
```
## Routes

This application has the following routes:

- **/**: Returns "Check /generate, /feedback, /scores".
- **/generate**: Accepts a POST request with user input(i.e. prompt message) and generates a response.
- **/feedback**: Accepts a POST request with user feedback and changes the scores.
- **/scores**: Returns the current scores for the models.
## Classes

This application uses several classes, which are defined in separate files:

- **AzureOpenAIFactory**: This class is responsible for creating instances of Azure OpenAI.
- **ResponseGenerator**: This class is responsible for generating responses based on user input.
- **Other classes in models.py**: These classes are either Pydantic model or dataclass that represent data formats.
## API Reference

#### Generate Response from randomly selected two AI models

```http
  POST /generate
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `prompt` | `string` | **Required**. The prompt for the randomly selected two AI models to generate a response |

Example:
![generate_1](https://github.com/takahiromitsui/chatbot_arena_api/assets/78789212/2f9c63f5-f0e9-454a-9fa3-89c7105a9958)
![generate_2](https://github.com/takahiromitsui/chatbot_arena_api/assets/78789212/e7cd23f3-22f5-4218-b05b-462d9806329f)

Two models are randomly picked.

#### Provide Feedback

```http
  POST /feedback
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `model_response`      | `list` | **Required**. List of model responses |
| `user_feedback`      | `string` | **Required**. User's feedback on the responses |

#### 

Please note that the /generate and /feedback routes accept JSON data in the request body. The model_responses parameter for the /feedback route is a list of objects, each with a blind_name and full_name property. The user_feedback parameter is a string that represents the user's feedback on the responses.

Example:

![feedback1](https://github.com/takahiromitsui/chatbot_arena_api/assets/78789212/b45f8515-6f75-4eb2-b286-dbb19d5c67a2)
![feedback](https://github.com/takahiromitsui/chatbot_arena_api/assets/78789212/6106d10f-8bc6-41fc-a49f-f4ac9d246ff7)


#### Get Scores

```http
  GET /scores
```

No parameters are required. Returns the current scores for the models.

This route returns a JSON object with the scores for each model. The keys in the object are the names of the models, and the values are the scores. The scores are updated based on user feedback.

Example:

![scores](https://github.com/takahiromitsui/chatbot_arena_api/assets/78789212/0fbd0658-a30e-4bc9-8b8c-5978e118517b)

A user picked model A in the feedback(see the first example of feedback). Model A was gpt3; therefore, gpt3 got one point.
