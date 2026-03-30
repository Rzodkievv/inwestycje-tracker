from flask import Flask, request, jsonify, send_from_directory
import requests
import csv
from io import StringIO

app = Flask(__name__, static_folder='static')

# Twój Finnhub API Key
FINNHUB_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

def get_price_finnhub(symbol):
    try:
        res = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}")
        data = res.json()
        return float(data.get('c', 0))
    except:
        return 0

def get_price_stooq(symbol):
    try:
        # KLUCZOWE: dodajemy .wa
        url = f"https://stooq.pl/q/l/?s={symbol.lower()}.wa&f=sd2t2ohlc&h&e=csv"
        res = requests.get(url)
        res.encoding = 'utf-8'
        
        f = StringIO(res.text)
        reader = csv.DictReader(f)
        
        for row in reader:
            price = row.get("Close")
            if price and price != "N/D":
                return float(price.replace(',', '.'))
    except:
        pass
    return 0

@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"price":0})

    # polskie spółki
    if symbol.upper().endswith(".WA") or symbol.isalpha():
        stooq_symbol = symbol.replace(".WA","")
        price = get_price_stooq(stooq_symbol)
        if price > 0:
            return jsonify({"price": price})

    # zagraniczne spółki
    price = get_price_finnhub(symbol)
    return jsonify({"price": price})

@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
