# OpenAI and Alpha Vantage Integration

This project integrates the OpenAI GPT-4 model and the Alpha Vantage API for financial data analysis. It uses GPT-4 for natural language understanding to parse user queries, and Alpha Vantage to fetch the relevant stock market data.

## Prerequisites

Before you begin, ensure you have met the following requirements:

* You have a valid API key from OpenAI. Visit [OpenAI](https://beta.openai.com/) to get one.
* You have a valid API key from Alpha Vantage. Visit [Alpha Vantage](https://www.alphavantage.co/) to get one.
* You have installed the necessary Python packages listed in the `requirements.txt` file.

## Configuration

This project uses a configuration file `config.ini` to store the API keys. Make sure to fill in your keys:

```ini
[DEFAULT]
ALPHAVANTAGE_API_KEY = your_alpha_vantage_api_key
OPENAI_API_KEY = your_openai_api_key
```
# How it works
This script works in a conversation-based manner where a user provides a query, and the AI understands and responds. If a user asks for a financial analysis function like 'Get the RSI for AAPL', the model understands this query and uses Alpha Vantage API to fetch the RSI data for AAPL.

The available functions are:

* get_sma: To get Simple Moving Average (SMA) data.
* get_macd: To get Moving Average Convergence Divergence (MACD) data.
* get_rsi: To get Relative Strength Index (RSI) data.
* get_bbands: To get Bollinger Bands (BBands) data.

# Running the Code
Just run the main script:
```sh
python main.py
```

It will start a conversation where you can ask for stock market data using natural language.
