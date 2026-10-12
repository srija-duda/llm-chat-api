# LLM Chat API

A REST API built with **FastAPI** that simulates an LLM chat service, with request
validation, model checks, cost estimation and automated tests.

## About

A REST API built with Python and FastAPI that simulates an LLM chat service. It includes
request validation with Pydantic, model availability checks, token-based cost estimation,
async endpoints and an automated test suite. The simulated response layer is designed to
be swapped for real LLM providers (OpenAI, AWS Bedrock).

## Features

- `POST /chat` – async chat endpoint with Pydantic validation (simulated LLM response)
- `GET /models` and `GET /models/{name}` – list and look up supported models
- `GET /cost` – estimate the cost of a request from its token count
- `GET /health` – health check
- Automatic interactive API docs at `/docs` (Swagger UI)
- Proper error handling: `400` unsupported model, `404` unknown model, `422` invalid input
- 10 automated tests with `pytest` and FastAPI's `TestClient`

## Tech stack

Python 3.12 · FastAPI · Pydantic · Uvicorn · pytest

## Project structure

```
llm-chat-api/
├── app/
│   ├── config.py      # constants (supported models, default price)
│   ├── models.py      # Pydantic request/response models
│   └── main.py        # API endpoints
├── tests/
│   └── test_main.py   # automated tests
├── .env.example
└── requirements.txt
```

## Getting started

```bash
git clone https://github.com/srija-duda/llm-chat-api.git
cd llm-chat-api
python -m venv .venv
.venv\Scripts\activate          # Windows  (Mac/Linux: source .venv/bin/activate)
pip install -r requirements.txt
fastapi dev app/main.py
```

Open http://127.0.0.1:8000/docs to try the API.

## Example request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is RAG?"}'
```

Response:

```json
{
  "model": "gpt-4o",
  "answer": "Simulated answer to 'What is RAG?' using model 'gpt-4o'",
  "tokens_used": 3
}
```

## Running tests

```bash
pytest -v
```

## What I learned

- **FastAPI vs Spring Boot:** coming from 7 years of Java/Spring Boot, I mapped familiar
  concepts to Python — `@app.get` instead of `@GetMapping`, Pydantic models instead of
  DTOs with `@Valid`, and built-in Swagger docs instead of adding springdoc-openapi.
- **Validation from type hints:** FastAPI and Pydantic validate requests automatically
  (422 errors) from type hints and `Field` constraints, with no manual validation code.
- **Choosing the right status code:** I learned to distinguish 400 (the request content
  is invalid) from 404 (the resource doesn't exist) and 422 (validation failed).
- **Async endpoints:** `async def` lets the server handle other requests while waiting
  on slow calls such as LLM APIs.
- **Testing with pytest:** I wrote 10 tests with `TestClient`. When a test failed, I
  learned to check whether the code or the test was wrong before changing anything.
## Next steps

- Replace the simulated answer with a real LLM call (OpenAI / AWS Bedrock)
- Add streaming responses
- Add Docker support