from typing import Callable


class AgentTool:
    """
    A base class for agent tools that can be used by the chat agent to perform tasks.
    """

    # Template for the description
    description: dict = {
        "type": "function",
        "function": {
            "name": "function_name",
            "description": "function_description",
            "parameters": {
                "type": "object",
                "properties": {
                    "param1": {"type": "string", "description": "param1_description"},
                    "param2": {"type": "int", "description": "param2_description"},
                },
                "required": ["param1", "param2"],  # List of required parameters
            },
        },
    }
    """
    The tool description in the OpenAI tool format
    """

    name: str = description["function"]["name"]
    """
    Name of the tool/function (must be the same as in the description)
    """

    # Template for the executable
    executable: Callable = lambda x: "Hello World!"
    """
    The actual function to be called upon
    """
