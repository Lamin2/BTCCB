import requests
import time
from bitget.spot.public_api import SpotPublicAPI
from bitget.spot.market_api import SpotMarketAPI
from telegram import Bot

# Variables d'environnement (à définir sur Render)
import os
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(message):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

def fetch_order_book(symbol="BTCUSDT", limit=1000):
    market_api = SpotMarketAPI()
    try:
        response = market_api.orderbook(symbol)
        return response['data']
    except Exception as e:
        send_telegram_message(f"Erreur API: {e}")
        return None

def analyze_and_trade():
    data = fetch_order_book()
    if not data:
        return

    bids = data['bids']
    asks = data['asks']

    top_buy = sum(float(bid[1]) for bid in bids[:20])
    top_sell = sum(float(ask[1]) for ask in asks[:20])

    imbalance = top_buy - top_sell

    if imbalance > 200:
        send_telegram_message("📈 Signal Long détecté sur BTC avec déséquilibre de volume haussier.")
    elif imbalance < -200:
        send_telegram_message("📉 Signal Short détecté sur BTC avec déséquilibre de volume baissier.")
    else:
        send_telegram_message("🔍 Aucune opportunité claire pour le moment.")

if __name__ == "__main__":
    analyze_and_trade()