Imessage Agent
===============

Lightweight FastAPI listener for BlueBubbles webhook events that forwards `/agent` messages to an Ollama model and replies via BlueBubbles.

Quick start
-----------

1. Create and activate a Python virtual environment:

    ```bash
    python3 -m venv .venv        # create
    source .venv/bin/activate    # activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file at the project root with these values (example):

    ```env
    HOST_ADDRESS=<app_server_host>     # defaults to 127.0.0.1
    HOST_PORT=<app_server_port>        # defaults to 8000

    BLUE_BUBBLES_HOST=<blue_bubbles_url>        # default http://localhost:1234
    BLUE_BUBBLES_PASSWORD=<blue_bubbles_server_password>

    OLLAMA_HOST=<ollama_url>        # default http://localhost:11434
    OLLAMA_MODEL=<ollama_model>     # defaults to qwen3:1.7b

    # comma-separated list of chat Imessage GUIDs (phone#/email) permitted to trigger agent
    ALLOWED_CONTACTS=<your-email-or-phone>,<another-guid>

    # Logging configuration
    LOG_LEVEL=INFO                  # DEBUG, INFO, WARNING, ERROR, CRITICAL (defaults to INFO)
    LOG_JSON=false                  # true for JSON output, false for readable plaintext
    ```

4. Run the development server:

    ```bash
    uvicorn app.main:app --reload --port 8000
    ```

API
---

- POST `/webhook` — accepts a JSON payload with schema matching `app.models.schemas.WebhookEvent`.

Example payload:

```json
{
  "type": "new-message",
  "data": {
    "text": "/agent Tell me a joke",
    "chats": [{"guid": "iMessage;-;<phone/email>"}],
    "isFromMe": true
  }
}
```

Test with curl:

```bash
curl -s -X POST http://localhost:8000/webhook \
  -H "Content-Type: application/json" \
  -d '{"type":"new-message","data":{"text":"/agent hi","chats":[{"guid":"iMessage;-;<phone/email>"}],"isFromMe":true}}'
```
