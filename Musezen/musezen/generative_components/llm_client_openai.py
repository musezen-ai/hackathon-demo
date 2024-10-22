from musezen.generative_components.llm_client_base import LLMClient
from openai.types.chat import ChatCompletion
from openai import OpenAI


class OpenAIClient(LLMClient):

    def __init__(
        self,
        api_key: str,
        helicone_api_key: str,
        base_url: str = "https://oai.hconeai.com/v1",
    ):
        """
        Initialize the OpenAI client with the API key and the base URL.

        Args:
            api_key (str): The OpenAI API key.
            helicone_api_key (str): The Helicone API key.
            base_url (str, optional): The base URL for the OpenAI API. Defaults to "https://oai.hconeai.com/v1" using Helicone.
        """
        self.client = OpenAI(
            api_key=api_key,
            # default_headers={"Helicone-Auth": f"Bearer {helicone_api_key}"},
            # base_url=base_url,
        )

    def send_message(
        self,
        model: str,
        messages: list[dict],
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ) -> ChatCompletion:
        """
        Send a message to the OpenAI API.

        Args:
            model (str): The model name.
            messages (list[dict]): A list of messages.
            max_tokens (int, optional): The maximum number of tokens to generate. Defaults to None.
            tools (dict, optional): A dictionary of tools to use. Defaults to None.

        Returns:
            ChatCompletion: The response from the API.
        """
        # if there are tools
        if tools:
            response: ChatCompletion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                tools=tools,
                tool_choice="auto",
                max_tokens=max_tokens,
            )

        # if there are no tools
        else:
            response: ChatCompletion = self.client.chat.completions.create(
                model=model,
                messages=messages,
                max_tokens=max_tokens,
            )

        return response