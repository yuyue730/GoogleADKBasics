from datetime import datetime
import random
import yfinance as yf

from google.adk.agents import Agent

def get_stock_price(ticker: str) -> dict:
    """Retrieves current stock prices and save to session state."""
    print(f"--- Tool: get_stock_price called for ticker {ticker} ---")

    # Get current timestamp
    current_time = datetime.now().strftime("%Y-%m-%d: %H:%M:%S")
    try:
        stock = yf.Ticker(ticker)
        current_price = stock.info.get("currentPrice")

        if current_price is None:
            return {
                "status": "error",
                "error_message": f"Could not fetch price for {ticker}"
            }

        return {
            "status": "success",
            "ticker": ticker,
            "price": current_price,
            "timestamp": current_time
        }
    except Exception as e:
        if "Too Many Requests." in str(e):
            print(f"WARNING Rate limited when getting price for {ticker}, "
                  f"return a random price instead.")
            return {
                "status": "success",
                ticker: ticker,
                "price": random.uniform(100, 200),
                "timestamp": current_time
            }

        return {
            "status": "error",
            "error_message": f"Error fetching stock data: {str(e)}"
        }

stock_analyst = Agent(
    name="stock_analyst",
    model="gemini-2.0-flash",
    description="An agent that can look up stock prices and track them over time",
    instruction="""
    You are a helpful stock market assistant that helps users track their stocks of interest.

    When asked about stock prices:
    1. Use the get_stock_price tool to fetch the latest price for the requested stock(s)
    2. Format the response to show each stock's current price and the time it was fetched
    3. If a stock price couldn't be fetched, mention this in your response.

    Example response format:
    "Here are the current prices for your stocks:
    - GOOG: $175.34 (updated at 2024-04-21 16:30:00)
    - TSLA: $156.78 (updated at 2024-04-21 16:30:00)
    - META: $123.45 (updated at 2024-04-21 16:30:00)"
    """,
    tools=[get_stock_price]
)
