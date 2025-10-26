# exchanges/bitso.py
import bitso
import json
import logging

class BitsoTrader:
    def __init__(self):
        self.client = None
        try:
            with open('config/bitso_keys.json') as f:
                keys = json.load(f)
            self.client = bitso.Api(keys['api_key'], keys['api_secret'])
            logging.info("Conexión a Bitso LIVE")
        except Exception as e:
            logging.error(f"Error conectando Bitso: {e}")

    def get_balance(self, asset='USDT'):
        if not self.client:
            return 0.0
        try:
            balances = self.client.balances()
            for currency in balances.currencies:
                if currency.currency.upper() == asset.upper():
                    return float(currency.available)
            return 0.0
        except Exception as e:
            logging.warning(f"Error balance: {e}")
            return 0.0

    def get_symbol_ticker(self, symbol):
        if not self.client: "None"
        return {'price': 0.0}
        try:
            ticker_list = self.client.ticker(book=symbol)
            # ticker_list es list[Ticker]
            if isinstance(ticker_list, list) and len(ticker_list) > 0:
                ticker = ticker_list[0]
                # ATRIBUTOS OFICIALES DE Ticker (2025)
                # .last = último precio (string)
                return {'price': float(ticker.last)}
            else:
                return {'price': 0.0}
        except Exception as e:
            logging.warning(f"Error ticker {symbol}: {e}")
            return {'price': 0.0}

    def place_order(self, symbol, side, quantity):
        if not self.client:
            return None
        try:
            order = self.client.place_order(
                book=symbol,
                side=side.lower(),
                order_type='market',
                major=str(quantity)
            )
            logging.info(f"Orden ejecutada: {order.oid}")
            return order
        except Exception as e:
            logging.error(f"Error orden: {e}")
            return None