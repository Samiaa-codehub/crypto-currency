import asyncio
import requests
from agents import Agent, Runner, function_tool
from connection import config
from dotenv import load_dotenv
import rich
load_dotenv()
## create the function and get the crypto price
@function_tool
def get_crypto_price(symbol: str) ->str:
    """Get the latest crypto price from Binance API"""
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return {"price": data["price"]}
    return {"error": "Failed to fetch data"}

# --- Agent Define ---
crypto_agent = Agent(
    name="Crypto Price Agent",
    instructions="You are a helpful agent that gives live crypto prices using the Binance API.",
    tools=[get_crypto_price],
)


async def main():
    result = await Runner.run(crypto_agent,"What is the price of LTCUSDT?",run_config=config)## run the agent
    rich.print(result.final_output)### print the final output
if __name__ == "__main__":
    asyncio.run(main())