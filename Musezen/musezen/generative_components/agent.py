import json

from musezen.generative_components.agent_tools import AgentTool
from musezen.generative_components.llm_client_base import LLMClient

from openai.types.chat.chat_completion import ChatCompletion


class ChatAgent:
    def __init__(
        self,
        llm_client: LLMClient,
        chat_history: list[dict],
        tools: list[AgentTool] = [],
    ):
        self.llm_client = llm_client
        self.chat_history = chat_history
        self.tools = []
        self.execs = {}
        if tools:
            [self.add_tools(t) for t in tools]

    def add_tools(self, tool: AgentTool):
        self.tools.append(tool.description)
        self.execs[tool.name] = tool.executable

    def function_calling(self, tool_calls: list):
        """
        This function calls the function specified in the LLM response and appends the result to
        the instance chat history.
        """
        for tool_call in tool_calls:
            print(tool_call)
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            # TODO: Might require error handling since JSON might not always contain valid parameters
            function_response = self.execs[function_name](**function_args)

            # Update chat history with the function responses
            self.chat_history.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": json.dumps(function_response),
                }
            )

    def invoke(self, input_message: str, model: str):
        self.chat_history.append({"role": "user", "content": input_message})

        # Initial request to the language model
        response: ChatCompletion = self.llm_client.send_message(
            model, self.chat_history, tools=self.tools
        )
        continue_function_calls = True

        while continue_function_calls:

            if isinstance(response, ChatCompletion):
                response_message = response.choices[0].message.content
                tool_calls = response.choices[0].message.tool_calls

            # Check if the model wanted to call a function
            if tool_calls:
                # Update chat history with the tool calls
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": response_message,
                        "tool_calls": tool_calls,
                    }
                )

                # Call the function and obtain result
                self.function_calling(tool_calls)

                # Send updated chat history back to the model
                response = self.llm_client.send_message(
                    model=model, messages=self.chat_history, tools=self.tools
                )
            else:
                continue_function_calls = False
                # Update chat history with the response message if no tool calls
                self.chat_history.append(
                    {
                        "role": "assistant",
                        "content": response_message,
                    }
                )

        # Return the last computed response message
        return response_message

    def get_chat_history(self):
        return self.chat_history