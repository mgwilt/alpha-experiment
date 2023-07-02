from enum import Enum
import openai
import configparser
import json
import inspect
from typing import Dict
from alpha_vantage import AlphaVantage

# earnings per share
# quarterly revenue growth yoy
# price to earnings ratio
# return on equity
# current price
# 52 week high
# 52 week low
# RSI
# MACD
# Debt to Equity Ratio D/E (calculated from balance sheet data total liabalities / total shareholder equity)

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

# print(generate_schema(alpha_vantage.get_bbands))

def run_conversation():
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": "Get the 14 day RSI for IBM"}]
    functions = [
        generate_schema(alpha_vantage.Fundamental.get_roe),
        generate_schema(alpha_vantage.Technical.get_macd),
        generate_schema(alpha_vantage.Technical.get_rsi),
    ]
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=functions,
        function_call="auto",  # auto is default, but we'll be explicit
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_sma": alpha_vantage.get_sma,
            "get_macd": alpha_vantage.get_macd,
            "get_rsi": alpha_vantage.get_rsi,
            #"get_bbands": alpha_vantage.get_bbands,
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
