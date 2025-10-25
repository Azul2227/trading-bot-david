import bitso
import json
import logging

class BitsoTrader:
    def __init__(self):
        try:
            with open('config/bitso_keys.json') as f:
                keys = json.load(f)
            self.client = bitso.Api(keys['api_key'], keys['api_secret'], keys['phrase'])
            logging.info("Conexión a Bitso LIVE")
        except Exception as e:
            logging.error(f"Error conectando Bitso: {e}")
            self.client = None

    def get_balance(self, asset='USDT'):
        if not self.client:
            return 1000  # Simulación
        try:
            balances = self.client.balances()
            for currency in balances.currencies:
                if currency.name == asset:
                    return float(currency.available)
            return 0.0
        except Exception as e:
            logging.warning(f"Error balance: {e}")
            return 0.0

    def get_symbol_ticker(self, symbol):
        try:
            ticker = self.client.ticker(book=symbol)
            return {'price': ticker.last}
        except Exception as e:
            logging.warning(f"Error ticker {symbol}: {e}")
            return {'price': '0'}

    def place_order(self, symbol, side, quantity):
        try:
            if side == 'BUY':
                order = self.client.buy_market_order(book=symbol, amount=quantity)
            else:
                order = self.client.sell_market_order(book=symbol, amount=quantity)
            logging.info(f"Orden ejecutada: {order}")
            return order
        except Exception as e:
            logging.error(f"Error orden: {e}")
            return None