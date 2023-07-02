import requests
from typing import Dict
from enum import Enum

class DataType(Enum):
    JSON = 'json'
    CSV = 'csv'

class MovingAverageType(Enum):
    SMA = 0
    EMA = 1
    WMA = 2
    DEMA = 3
    TEMA = 4
    TRIMA = 5
    T3 = 6
    KAMA = 7
    MAMA = 8

class AlphaVantage:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.fundamentals = AlphaVantage.Fundamental(api_key)

    class Fundamental:
        def __init__(self, api_key: str):
            self.api_key = api_key
        
        def get_quarterly_revenue_growth_yoy(self, symbol: str) -> float:
            """
            Get the quarterly revenue growth year over year (YOY) for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The quarterly revenue growth YOY for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            quarterly_revenue_growth_yoy = float(data["QuarterlyRevenueGrowthYOY"])
            return quarterly_revenue_growth_yoy
        
        def get_pe_ratio(self, symbol: str) -> float:
            """
            Get the price to earnings (P/E) ratio for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The P/E ratio for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            pe_ratio = float(data["PERatio"])
            return pe_ratio      
        
        def get_roe(self, symbol: str) -> float:
            """
            Get the return on equity (ROE) for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The return on equity for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            roe = float(data["ReturnOnEquityTTM"])
            return roe
        
        def get_total_liabilities(self, symbol: str) -> float:
            """
            Get the total liabilities for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The total liabilities for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            total_liabilities = float(data["quarterlyReports"][0]["totalLiabilities"])
            return total_liabilities
    
        def get_total_shareholder_equity(self, symbol: str) -> float:
            """
            Get the total liabilities for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The total liabilities for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=BALANCE_SHEET&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            total_liabilities = float(data["quarterlyReports"][0]["totalShareholderEquity"])
            return total_liabilities
        
        def get_debt_to_equity(self, symbol: str) -> float:
            """
            Get the total debt to equity ratio for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The total debt to equity ratio for the specified stock.
            """
            total_liabilities = self.get_total_liabilities(symbol)
            total_shareholder_equity = self.get_total_shareholder_equity(symbol)
            total_debt_to_equity = total_liabilities / total_shareholder_equity
            return total_debt_to_equity
    
    class Technical:
        def get_current_price(self, symbol: str) -> float:
            """
            Get the current price for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The current price for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            current_price = float(data["Global Quote"]["05. price"])
            return current_price
        
        def get_52_week_high(self, symbol: str) -> float:
            """
            Get the 52-week high for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The 52-week high for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            weekly_data = data["Weekly Time Series"]
            high_prices = [float(weekly_data[date]["2. high"]) for date in weekly_data]
            fifty_two_week_high = max(high_prices)
            return fifty_two_week_high
        
        def get_52_week_low(self, symbol: str) -> float:
            """
            Get the 52-week low for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.

            Returns:
            float: The 52-week low for the specified stock.
            """
            url = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={symbol}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            weekly_data = data["Weekly Time Series"]
            low_prices = [float(weekly_data[date]["3. low"]) for date in weekly_data]
            fifty_two_week_low = min(low_prices)
            return fifty_two_week_low

        def get_sma(
            self,
            symbol: str,
            interval: str = "daily",
            time_period: int = 60,
            series_type: str = "close",
        ) -> Dict[str, Dict[str, str]]:
            """
            Get the simple moving average for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.
            interval (str): The time interval for the SMA calculation (default: daily).
            time_period (int): The time period for the SMA calculation (default: 60).
            series_type (str): The series type for the SMA calculation (default: close).

            Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the simple moving average data for the specified stock.
            The keys are dates and the values are dictionaries containing the simple moving averages for each date.
            """
            url = f"https://www.alphavantage.co/query?function=SMA&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            sma_data = data["Technical Analysis: SMA"]
            return sma_data

        def get_macd(
            self,
            symbol: str,
            interval: str = "daily",
            series_type: str = "close",
            fastperiod: int = 12,
            slowperiod: int = 26,
            signalperiod: int = 9,
            datatype: str = "json",
        ) -> Dict[str, Dict[str, str]]:
            """
            Get the Moving Average Convergence Divergence (MACD) for a given stock.

            Parameters:
            symbol (str): The stock ticker symbol.
            interval (str): The time interval for the MACD calculation (default: daily).
            series_type (str): The series type for the MACD calculation (default: close).
            fastperiod (int): The time period for the fast EMA calculation (default: 12).
            slowperiod (int): The time period for the slow EMA calculation (default: 26).
            signalperiod (int): The time period for the signal EMA calculation (default: 9).
            datatype (str): The data type to return (default: json).

            Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the MACD data for the specified stock.
            The keys are dates and the values are dictionaries containing the MACD data for each date.
            """
            url = f"https://www.alphavantage.co/query?function=MACD&symbol={symbol}&interval={interval}&series_type={series_type}&fastperiod={fastperiod}&slowperiod={slowperiod}&signalperiod={signalperiod}&datatype={datatype}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            macd_data = data["Technical Analysis: MACD"]
            return macd_data
        
        def get_rsi(self, symbol, interval, time_period, series_type, datatype=DataType.JSON):
            """
            Returns the RSI (Relative Strength Index) data for the specified stock.

            Args:
            symbol (str): The name of the ticker of your choice.
            interval (str): Time interval between two consecutive data points in the time series.
            time_period (int): Number of data points used to calculate each RSI value.
            series_type (str): The desired price type in the time series.
            datatype (DataType): The data type to return (default: JSON).

            Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the RSI data for the specified stock.
            The keys are dates and the values are dictionaries containing the RSI data for each date.
            """
            url = f"https://www.alphavantage.co/query?function=RSI&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&datatype={datatype.value}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            rsi_data = data["Technical Analysis: RSI"]
            return rsi_data
        
        def get_bbands(self, symbol: str, interval: str, time_period: int, series_type: str, nbdevup: int = 2, nbdevdn: int = 2, matype: MovingAverageType = MovingAverageType.SMA, datatype: DataType = DataType.JSON) -> Dict[str, Dict[str, str]]:
            """
            Returns the Bollinger Bands data for the specified stock.

            Args:
            symbol (str): The name of the ticker of your choice.
            interval (str): Time interval between two consecutive data points in the time series.
            time_period (int): Number of data points used to calculate each BBANDS value.
            series_type (str): The desired price type in the time series.
            nbdevup (int): The standard deviation multiplier of the upper band (default: 2).
            nbdevdn (int): The standard deviation multiplier of the lower band (default: 2).
            matype (MovingAverageType): Moving average type of the time series (default: SMA). By default, matype=SMA. The following moving average types are accepted:
            - SMA (Simple Moving Average)
            - EMA (Exponential Moving Average)
            - WMA (Weighted Moving Average)
            - DEMA (Double Exponential Moving Average)
            - TEMA (Triple Exponential Moving Average)
            - TRIMA (Triangular Moving Average)
            - T3 (T3 Moving Average)
            - KAMA (Kaufman Adaptive Moving Average)
            - MAMA (MESA Adaptive Moving Average)
            datatype (DataType): The data type to return (default: JSON).

            Returns:
            Dict[str, Dict[str, str]]: A dictionary containing the Bollinger Bands data for the specified stock.
            The keys are dates and the values are dictionaries containing the Bollinger Bands data for each date.
            """
            url = f"https://www.alphavantage.co/query?function=BBANDS&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&nbdevup={nbdevup}&nbdevdn={nbdevdn}&matype={matype.value}&datatype={datatype.value}&apikey={self.api_key}"
            response = requests.get(url)
            data = response.json()
            bbands_data = data["Technical Analysis: BBANDS"]
            return bbands_data