# utils/paypal.py
import logging

class PayPalP2P:
    def __init__(self):
        logging.info("PayPal P2P configurado correctamente")

    def buy_crypto(self, amount_usd):
        """Simula recarga vía PayPal P2P"""
        logging.info(f"Recargando {amount_usd} USD vía PayPal P2P")
        # Aquí iría integración real con PayPal REST SDK
        # Por ahora: simulación
        return True