from dotenv import load_dotenv
import os
from app.core.logging import logger

load_dotenv()

HOST_ADDRESS = os.getenv("HOST_ADDRESS", "127.0.0.1")
HOST_PORT = int(os.getenv("HOST_PORT", "8000"))

BLUE_BUBBLES_HOST = os.getenv("BLUE_BUBBLES_SERVER_HOST", "http://localhost:1234")
BLUE_BUBBLES_PASSWORD = os.getenv("BLUE_BUBBLES_SERVER_PASSWORD", "")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:4b")
MODEL_CONTEXT_SIZE = int(os.getenv("MODEL_CONTEXT_SIZE", "64000"))
logger.info(f"Chat model is: {OLLAMA_MODEL}")

# guid values permitted to trigger the agent.  Provide a comma-separated
# list via environment variable; defaults to empty, meaning only `isFromMe`
# messages will be considered.
_allowed = os.getenv("ALLOWED_CONTACTS", "")
ALLOWED_CONTACTS = [v.strip() for v in _allowed.split(",") if v.strip()]
