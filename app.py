import os
import requests
import time
from dotenv import load_dotenv
from bitget.spot import Spot
from bitget.mix import Mix

# Charger les variables d'environnement
load_dotenv()

API_KEY = os.getenv("BITGET_API_KEY")
API_SECRET = os.getenv("BITGET_API_SECRET")
API_PASSPHRASE = os.getenv("BITGET_API_PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

symbol = "BTCUSDT"
product_type = "umcbl"  # USDT-M Futures

mix = Mix(API_KEY, API_SECRET, API_PASSPHRASE)

def get_order_book():
    try:
        depth = mix.market_api().get_depth(symbol, product_type, limit=1000)
        bids = [[float(x[0]), float(x[1])] for x in depth['data']['bids']]
        asks = [[float(x[0]), float(x[1])] for x in depth['data']['asks']]
        return bids, asks
    except Exception as e:
        print("Erreur récupération order book:", e)
        return [], []

def analyze_order_book(bids, asks):
    top_bids = bids[:100]
    top_asks = asks[:100]

    total_bid_liquidity = sum([price * volume for price, volume in top_bids])
    total_ask_liquidity = sum([price * volume for price, volume in top_asks])
    total_bid_volume = sum([volume for _, volume in top_bids])
    total_ask_volume = sum([volume for _, volume in top_asks])

    imbalance = (total_bid_volume - total_ask_volume) / max(total_bid_volume + total_ask_volume, 1)

    print(f"🔍 BID Vol: {total_bid_volume:.2f} | ASK Vol: {total_ask_volume:.2f}")
    print(f"📦 BID Liquidity: {total_bid_liquidity:.2f} | ASK Liquidity: {total_ask_liquidity:.2f}")
    print(f"📊 Imbalance: {imbalance:.4f}")

    # Conditions précises pour signaux puissants
    if imbalance > 0.25 and total_bid_liquidity > total_ask_liquidity * 1.2:
        return "LONG"
    elif imbalance < -0.25 and total_ask_liquidity > total_bid_liquidity * 1.2:
        return "SHORT"
    else:
        return "NO SIGNAL"

def send_telegram_signal(signal):
    if signal in ["LONG", "SHORT"]:
        message = f"📈 Signal détecté : {signal} sur BTC/USDT ⚡️\n🔹 Levier : x500\n🕒 Session : {time.strftime('%H:%M')}"
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        try:
            requests.post(url, json=payload)
        except Exception as e:
            print("Erreur Telegram:", e)

def main():
    bids, asks = get_order_book()
    if bids and asks:
        signal = analyze_order_book(bids, asks)
        send_telegram_signal(signal)
        print(f"✅ Signal actuel : {signal}")
    else:
        print("❌ Order book vide ou erreur API")

if __name__ == "__main__":
    main()
