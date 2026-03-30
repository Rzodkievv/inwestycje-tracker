from flask import Flask, request, jsonify, send_from_directory
import requests
import csv

app = Flask(__name__)

FINNHUB_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"  #

@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/price")
def get_price():
    ticker = request.args.get("ticker")
    if not ticker:
        return jsonify({"error": "Brak tickera"}), 400

    try:
        # Polskie spółki GPW: wpisujemy "GPW:PEO"
        if ticker.startswith("GPW:"):
            symbol = ticker.replace("GPW:", "").lower()
            url = f"https://stooq.pl/q/l/?s={symbol}&f=sd2t2ohlc&h&e=csv"
            resp = requests.get(url)
            decoded = resp.text.splitlines()
            reader = csv.DictReader(decoded)
            data = list(reader)[0]
            price = float(data["Close"])
            return jsonify({"price": price})
        else:
            # Zagraniczne spółki
            url = f"https://finnhub.io/api/v1/quote?symbol={ticker}&token={FINNHUB_KEY}"
            resp = requests.get(url)
            data = resp.json()
            return jsonify({"price": data["c"]})
    except Exception as e:
        print(e)
        return jsonify({"error": "Błąd pobierania ceny"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)