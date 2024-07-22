import re
from .base_llm import BaseLLMKernel
import time

# could be dynamically imported similar to other models
from openai import OpenAI

from pyopenagi.utils.chat_template import Response
import json

class GPTLLM(BaseLLMKernel):

    def __init__(self, llm_name: str,
                 max_gpu_memory: dict = None,
                 eval_device: str = None,
                 max_new_tokens: int = 256,
                 log_mode: str = "console"):
        super().__init__(llm_name,
                         max_gpu_memory,
                         eval_device,
                         max_new_tokens,
                         log_mode)

    def load_llm_and_tokenizer(self) -> None:
        self.model = OpenAI()
        self.tokenizer = None

    def parse_tool_calls(self, tool_calls):
        if tool_calls:
            parsed_tool_calls = []
            for tool_call in tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                parsed_tool_calls.append(
                    {
                        "name": function_name,
                        "parameters": function_args
                    }
                )
            return parsed_tool_calls
        return None

    def process(self,
            agent_process,
            temperature=0.0
        ):
        # ensures the model is the current one
        assert re.search(r'gpt', self.model_name, re.IGNORECASE)

        """ wrapper around openai api """
        agent_process.set_status("executing")
        agent_process.set_start_time(time.time())
        messages = agent_process.query.messages
        print(messages)
        self.logger.log(
            f"{agent_process.agent_name} is switched to executing.\n",
            level = "executing"
        )
        time.sleep(2)

        max_retries = 3
        delay = 10
        for attempt in range(max_retries):
            try:
                response = self.model.chat.completions.create(
                    model=self.model_name,
                    messages = messages,
                    tools = agent_process.query.tools,
                    tool_choice = "required" if agent_process.query.tools else None
                )
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise


        response_message = response.choices[0].message.content
        tool_calls = self.parse_tool_calls(
            response.choices[0].message.tool_calls
        )
        # print(tool_calls)
        # print(response.choices[0].message)
        agent_process.set_response(
            Response(
                response_message = response_message,
                tool_calls = tool_calls
            )
        )
        agent_process.set_status("done")
        agent_process.set_end_time(time.time())
        return
