import requests
from typing import Dict, Any

COINGECKO_API = "https://api.coingecko.com/api/v3"

class CoinGeckoAPI:
    def __init__(self):
        self.session = requests.Session()

    def get_price(self, crypto_id: str = "bitcoin") -> float:
        response = self.session.get(
            f"{COINGECKO_API}/simple/price",
            params={"ids": crypto_id, "vs_currencies": "usd"}
        )
        response.raise_for_status()
        return response.json()[crypto_id]["usd"]

    def get_market_data(self, crypto_id: str = "bitcoin") -> Dict[str, Any]:
        response = self.session.get(
            f"{COINGECKO_API}/coins/{crypto_id}/market_chart",
            params={"vs_currency": "usd", "days": "1", "interval": "hourly"}
        )
        response.raise_for_status()
        return response.json()