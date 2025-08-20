import rich
import asyncio
import httpx
##from connection import config
from pydantic import BaseModel
from agents import (
    Agent,
    Runner,
    input_guardrail,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
)

# ✅ Output schema
class PriceOutput(BaseModel):
    symbol: str
    price: str

# ✅ Binance fetch function
async def get_price(symbol: str) -> PriceOutput:
    async with httpx.AsyncClient() as client:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
        response = await client.get(url)
        data = response.json()
        return PriceOutput(symbol=data["symbol"], price=data["price"])

# ✅ Input Guardrail (allowed symbols only)
@input_guardrail
def symbol_guardrail(user_input: str) -> GuardrailFunctionOutput:
    allowed = ["BTCUSDT", "ETHUSDT", "BNBUSDT"]
    if user_input.upper() not in allowed:
        return GuardrailFunctionOutput(
            is_valid=False,
            message="⚠️ Invalid symbol. Allowed: BTCUSDT, ETHUSDT, BNBUSDT"
        )
    return GuardrailFunctionOutput(is_valid=True)

# ✅ Agent
crypto_agent = Agent(
    name="Crypto Price Agent",
    instructions="You fetch crypto prices from Binance API safely.",
    functions=[get_price],
    input_guardrails=[symbol_guardrail],  # 👈 Input Guardrail again added
)

# ✅ Runner
async def main():
    runner = Runner(agent=crypto_agent)
    try:
        result = await runner.run("BTCUSDT")  # 👈 Test input
        rich.print(result)
    except InputGuardrailTripwireTriggered as e:
        rich.print(f"[red]Input Guardrail Triggered: {e}[/red]")

asyncio.run(main())