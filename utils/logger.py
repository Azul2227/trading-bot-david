# utils/logger.py
# LOGS PROFESIONALES EN ARCHIVO Y CONSOLA (CORREGIDO)

import logging
import os
from datetime import datetime

def setup_logger(name="trading_bot"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Evita duplicar handlers
    if logger.handlers:
        return logger

    # FORMATO CORRECTO: usa %(asctime)s con strftime
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'  # ← AQUÍ SE DEFINE %Y
    )

    # Archivo de logs
    os.makedirs("logs", exist_ok=True)
    file_handler = logging.FileHandler(f"logs/bot_{datetime.now():%Y%m%d}.log", encoding='utf-8')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger
