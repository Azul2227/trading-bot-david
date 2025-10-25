from flask import Flask, jsonify  # ← AÑADIDO jsonify
from core.bot import TradingBot
import threading
import time

app = Flask(__name__)
bot = TradingBot()

# Iniciar bot en segundo plano
threading.Thread(target=bot.start, daemon=True).start()
time.sleep(2)

@app.route('/')
def home():
    positions = len(bot.trader.risk.positions)
    return f"""
    <h1>🤖 TRADING BOT DAVID</h1>
    <h2>Posiciones abiertas: {positions}</h2>
    <p>Estado: <span style="color:green">ACTIVO 24/7</span></p>
    <p>PayPal P2P: ✅</p>
    <p>Telegram: ✅</p>
    <p>Trading REAL: ✅</p>
    <meta http-equiv="refresh" content="10">
    """

@app.route('/data')
def api_data():
    return jsonify({
        "balance": bot.trader.binance.get_balance(),
        "positions": len(bot.trader.risk.positions)
    })

if __name__ == '__main__':
    print("Dashboard en http://localhost:5000")
    app.run(port=5000, debug=False)