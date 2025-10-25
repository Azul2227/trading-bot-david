import logging
import os

def setup_logger():
    os.makedirs('data', exist_ok=True)
    logging.basicConfig(
        filename='data/bot.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    logging.getLogger().addHandler(console)
    return logging.getLogger()