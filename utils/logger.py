# utils/logger.py
import logging
import os
from datetime import datetime

def setup_logger(name="trading_bot"):
    """Configura logger profesional con archivo y consola"""
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Evitar duplicados
    if logger.handlers:
        return logger

    # Formato
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Archivo de log
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = f"{log_dir}/bot_{datetime.now().strftime('%Y%m%d')}.log"

    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger