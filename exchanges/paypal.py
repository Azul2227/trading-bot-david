from paypalrestsdk import Payout
import paypalrestsdk
import json
import logging

class PayPalP2P:
    def __init__(self):
        try:
            with open('config/paypal_keys.json') as f:
                keys = json.load(f)
            paypalrestsdk.configure({
                "mode": keys["mode"],  # "sandbox" o "live"
                "client_id": keys["client_id"],
                "client_secret": keys["client_secret"]
            })
            logging.info("PayPal P2P configurado correctamente")
        except FileNotFoundError:
            logging.error("config/paypal_keys.json no encontrado")
        except json.JSONDecodeError:
            logging.error("config/paypal_keys.json tiene formato inválido")
        except Exception as e:
            logging.error(f"Error configurando PayPal: {e}")

    def buy_crypto(self, amount_usd, crypto='BTC'):
        # Futuro: integrar con Binance P2P
        logging.info(f"Comprando {amount_usd} USD de {crypto} vía PayPal P2P")
        return True