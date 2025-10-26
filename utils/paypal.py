# utils/paypal.py
# SIMULACIÓN DE RECARGA CON PAYPAL P2P

import logging

class PayPalP2P:
    def __init__(self):
        logging.info("PayPal P2P configurado correctamente")

    def buy_crypto(self, amount):
        logging.info(f"Simulando recarga de {amount} USD vía PayPal P2P")
        return True