from abc import ABC, abstractmethod


class LLMClient(ABC):
    @abstractmethod
    def send_message(
        self,
        model: str,
        messages: list[dict],
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ):
        pass