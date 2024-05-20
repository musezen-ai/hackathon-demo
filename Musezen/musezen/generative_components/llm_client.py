from abc import ABC, abstractmethod
import replicate
import os
import streamlit as st
from transformers import AutoTokenizer


@st.cache_resource(show_spinner=False)
def get_tokenizer():
    """Get a tokenizer to make sure we're not sending too much text
    text to the Model. Eventually we will replace this with ArcticTokenizer
    """
    return AutoTokenizer.from_pretrained("huggyllama/llama-7b")


def get_num_tokens(prompt: str):
    """Get the number of tokens in a given prompt"""
    tokenizer = get_tokenizer()
    tokens = tokenizer.tokenize(prompt)
    return len(tokens)


def check_safety(prompt: str, response: str, disable=False) -> bool:
    if disable:
        return True

    output = replicate.run(
        "meta/meta-llama-guard-2-8b:b063023ee937f28e922982abdbf97b041ffe34ad3b35a53d33e1d74bb19b36c4",
        input={
            "prompt": prompt,
            "assistant": response,
        },
    )

    if output is not None and "unsafe" in output:
        return False
    else:
        return True


class LLMClient(ABC):
    @abstractmethod
    def send_message(
        self,
        model: str,
        messages: list[dict],
        max_tokens: int | None = None,
        tools: list[dict] | None = None,
    ):
        raise NotImplementedError("This method must be implemented in the child class!")


class ArcticClient(LLMClient):

    def __init__(
        self,
        api_key: str,
    ):
        """
        Initialize the Snowflake Arctic by authenticating using API key.

        Args:
            replicate_api_key (str): The Replicate API key.
        """
        os.environ["REPLICATE_API_TOKEN"] = api_key

    def send_message(
        self,
        model: str,
        messages: list[dict],
        tools: list[dict] = None,
        temperature: float = 0.3,
        top_p: float = 0.9,
    ) -> list[str]:
        """
        Send a message to the OpenAI API.

        Args:
            model (str): Name of the model used
            messages (list[dict]): A list of messages.
            tools (list[dict]): A list of function specifications

        Returns:
            Iterable: The streaming response from the API.
        """
        prompt = []
        for dict_message in messages:
            if dict_message["role"] == "user":
                prompt.append(
                    "<|im_start|>user\n" + dict_message["content"] + "<|im_end|>"
                )
            else:
                prompt.append(
                    "<|im_start|>assistant\n" + dict_message["content"] + "<|im_end|>"
                )

        prompt.append("<|im_start|>assistant")
        prompt.append("")
        prompt_str = "\n".join(prompt)

        if get_num_tokens(prompt_str) >= 3072:
            raise OverflowError

        output = replicate.run(
            model,
            input={
                "prompt": prompt_str,
                "prompt_template": r"{prompt}",
                "temperature": temperature,
                "top_p": top_p,
            },
        )

        is_safe = check_safety(
            prompt=messages[-1]["content"],
            response="".join(output),
        )
        if is_safe:
            return output
        else:
            return ["I'm sorry, I cannot help with that"]
