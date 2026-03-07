from app.core.logging import logger


class ChatContext:
    """
    Manages the chat context for interactions with the Ollama model.
    This includes storing recent messages and ensuring the context size
    does not exceed the model's token limit.
    """

    def __init__(self, max_context_size: int):
        self.max_context_size = max_context_size
        self.current_context_size = 0
        self.messages: list[tuple[str, int]] = (
            []
        )  # List of (message, token_count) tuples

    def add_chat_context(self, chat: str, token_count: int):
        """Add a chat message to the context and trim if necessary."""

        self.current_context_size += token_count
        self.messages.append((chat, token_count))
        self._trim_chat_context()
        logger.info(
            f"Current chat context size: {self.current_context_size} tokens with {len(self.messages)} messages"
        )

    def _trim_chat_context(self):
        """Trim the context to ensure it does not exceed the maximum size."""

        while self.current_context_size > self.max_context_size:
            (_, token_count) = self.messages.pop(0)  # Remove the oldest message
            self.current_context_size -= token_count

    def get_chat_context(self) -> list[str]:
        return [x[0] for x in self.messages]
    
    def get_current_context_size(self) -> int:
        return self.current_context_size
