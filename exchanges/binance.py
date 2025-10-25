import json
import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException

class BinanceTrader:
    def __init__(self):
        try:
            with open('config/binance_keys.json') as f:
                keys = json.load(f)
            
            api_key = keys.get('api_key', '')
            api_secret = keys.get('api_secret', '')
            testnet = keys.get('testnet', False)
            key_type = keys.get('key_type', 'hmac')

            if not api_key or not api_secret:
                raise ValueError("Faltan api_key o api_secret en binance_keys.json")

            if testnet:
                self.client = Client(api_key, api_secret, testnet=True)
                logging.info("Conexión a Binance (Testnet)")
            else:
                if key_type == 'ed25519':
                    self.client = Client(api_key, api_secret, tld='com')
                    self.client.API_URL = 'https://api.binance.com/api'
                    logging.info("Conexión a Binance (LIVE) con ED25519")
                else:
                    self.client = Client(api_key, api_secret)
                    logging.info("Conexión a Binance (LIVE) con HMAC")
                
        except FileNotFoundError:
            logging.error("config/binance_keys.json no encontrado")
            self.client = None
        except Exception as e:
            logging.error(f"Error conectando Binance: {e}")
            self.client = None

    def get_balance(self, asset='USDT'):
        if not self.client:
            return 1000
        try:
            balance = self.client.get_asset_balance(asset=asset)
            return float(balance['free'])
        except Exception as e:
            logging.warning(f"Error balance: {e}")
            return 1000