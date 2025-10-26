# exchanges/kucoin.py
import kucoin
import os
import logging
from dotenv import load_dotenv
from typing import Dict

load_dotenv()

class KuCoinTrader:
    def __init__(self):
        self.client = None
        try:
            api_key = os.getenv('KUCOIN_API_KEY')
            api_secret = os.getenv('KUCOIN_SECRET_KEY')
            passphrase = os.getenv('KUCOIN_PASSPHRASE')
            if not api_key or not api_secret or not passphrase:
                raise ValueError("Faltan claves KuCoin en .env")

            self.client = kucoin.Client(api_key, api_secret, passphrase)
            logging.info("Conexión a KuCoin LIVE")
        except Exception as e:
            logging.error(f"Error conectando KuCoin: {e}")

    def get_balance(self, asset: str = 'USDT') -> float:
        if not self.client:
            return 0.0
        try:
            balances = self.client.get_accounts(currency=asset)
            if balances:
                return float(balances[0]['available'])
            return 0.0
        except Exception as e:
            logging.warning(f"Error balance: {e}")
            return 0.0

    def get_symbol_ticker(self, symbol: str) -> Dict[str, float]:
        if not self.client:
            return {'price': 0.0}
        try:
            ticker = self.client.get_ticker(symbol=symbol)
            return {'price': float(ticker['price'])}
        except Exception as e:
            logging.warning(f"Error ticker {symbol}: {e}")
            return {'price': 0.0}

    def place_order(self, symbol: str, side: str, quantity: float):
        if not self.client:
            return None
        try:
            order = self.client.create_order(
                symbol=symbol,
                side=side.lower(),
                type='market',
                size=str(quantity)
            )
            logging.info(f"Orden ejecutada: {order['id']}")
            return order
        except Exception as e:
            logging.error(f"Error orden: {e}")
            return None