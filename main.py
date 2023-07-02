from enum import Enum
import openai
import configparser
import json
import inspect
from typing import Dict
from alpha_vantage import AlphaVantage

config = configparser.ConfigParser()
config.read("config.ini")

ALPHAVANTAGE_API_KEY = config["DEFAULT"]["ALPHAVANTAGE_API_KEY"]
OPENAI_API_KEY = config["DEFAULT"]["OPENAI_API_KEY"]

openai.api_key = OPENAI_API_KEY

alpha_vantage = AlphaVantage(ALPHAVANTAGE_API_KEY)

def generate_schema(func):
    schema = {
        "name": func.__name__,
        "description": func.__doc__,
        "parameters": {
            "type": "object",
            "properties": {},
            "required": []
        }
    }
    signature = inspect.signature(func)
    for param_name, param in signature.parameters.items():
        if issubclass(param.annotation, Enum):
            schema["parameters"]["properties"][param_name] = {
                "type": "string",
                "enum": [e.value for e in param.annotation]
            }
        else:
            schema["parameters"]["properties"][param_name] = {
                "type": "string" if param.annotation == str else "integer",
                "description": param_name + " " + str(param.annotation),
            }
        if param.default == inspect.Parameter.empty:
            schema["parameters"]["required"].append(param_name)
    return schema

class Command:
    """
    A command object that wraps a function call with its arguments and keyword arguments.
    """
    def __init__(self, func_name: str, *args, **kwargs):
        self.func_name = func_name
        self.args = args
        self.kwargs = kwargs

    def execute(self):
        func = globals()[self.func_name]
        return func(*self.args, **self.kwargs)

def execute_commands_in_order(commands: list) -> dict:
    """
    Execute a list of commands in order and aggregate the results into one dictionary.

    Parameters:
    commands (list): A list of Command objects to be executed in order.

    Returns:
    dict: A dictionary containing the results of each command execution.
    """
    results = {}
    for command in commands:
        result = command.execute()
        results[command.func.__name__] = result
    return results

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Using fundamental and technical analysis recommend buy/sell/hold for IBM."}]
    functions = [
        generate_schema(execute_commands_in_order),
        generate_schema(alpha_vantage.Fundamental.get_earnings_per_share),
        generate_schema(alpha_vantage.Fundamental.get_quarterly_revenue_growth_yoy),
        generate_schema(alpha_vantage.Fundamental.get_pe_ratio),
        generate_schema(alpha_vantage.Fundamental.get_roe),
        generate_schema(alpha_vantage.Fundamental.get_debt_to_equity),
        generate_schema(alpha_vantage.Technical.get_52_week_high),
        generate_schema(alpha_vantage.Technical.get_52_week_low),
        generate_schema(alpha_vantage.Technical.get_rsi),
        # generate_schema(alpha_vantage.Technical.get_macd),
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call={ "name": "execute_commands_in_order" },  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "execute_commands_in_order": execute_commands_in_order,
        }
        function_name = response_message["function_call"]["name"]
        fuction_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = fuction_to_call(**function_args)

        # Step 4: send the info on the function call and function response to GPT
        # messages.append(response_message)  # extend conversation with assistant's reply
        # messages.append(
        #     {
        #         "role": "function",
        #         "name": function_name,
        #         "content": function_response,
        #     }
        # )  # extend conversation with function response
        # second_response = openai.ChatCompletion.create(
        #     model="gpt-4-0613",
        #     messages=messages,
        # )  # get a new response from GPT where it can see the function response
        # return second_response

print(run_conversation())
