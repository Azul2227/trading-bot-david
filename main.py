# main.py
# CARGA .env DESDE LA RAÍZ DEL PROYECTO (100% GARANTIZADO)

from dotenv import load_dotenv
from pathlib import Path
import os

# CARGA .env DESDE LA RAÍZ DEL PROYECTO
BASE_DIR = Path(__file__).resolve().parent
env_path = BASE_DIR / '.env'
load_dotenv(dotenv_path=env_path)

# VERIFICA QUE CARGÓ
print(f"[DEBUG] .env cargado desde: {env_path}")
print(f"[DEBUG] kucoin_API_KEY: {os.getenv('kucoin_API_KEY')}")

# AHORA IMPORTS
import logging
from core.bot import TradingBot
from utils.logger import setup_logger

if __name__ == "__main__":
    logger = setup_logger()
    logger.info("Iniciando bot en modo LIVE + PayPal P2P...")
    print("Iniciando bot en modo LIVE + PayPal P2P...")

    bot = TradingBot()
    bot.start()