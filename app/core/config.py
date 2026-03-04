from dotenv import load_dotenv
import os

load_dotenv()

HOST_PORT = int(os.getenv("HOST_PORT", "8000"))

BLUE_BUBBLES_HOST = os.getenv("BLUE_BUBBLES_SERVER_HOST", "http://localhost:1234")
BLUE_BUBBLES_PASSWORD = os.getenv("BLUE_BUBBLES_SERVER_PASSWORD", "")

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:1.7b")

# guid values permitted to trigger the agent.  Provide a comma-separated
# list via environment variable; defaults to empty, meaning only `isFromMe`
# messages will be considered.
_allowed = os.getenv("ALLOWED_CONTACTS", "")
ALLOWED_CONTACTS = [v.strip() for v in _allowed.split(",") if v.strip()]
