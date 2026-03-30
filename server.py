from flask import Flask, request, jsonify
import requests
import csv
from io import StringIO

app = Flask(__name__)

# Twój Finnhub API Key
FINNHUB_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

def get_price_finnhub(symbol):
    try:
        res = requests.get(f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_KEY}")
        data = res.json()
        if 'c' in data and data['c'] > 0:
            return data['c']
    except:
        pass
    return None

def get_price_stooq(symbol):
    # symbol np. PEO → strona Stooq: PEO
    try:
        url = f"https://stooq.pl/q/l/?s={symbol.lower()}&f=sd2t2ohlc&h&e=csv"
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
    return None

@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "No symbol provided"}), 400

    # Polski symbol? GPW zwykle bez kropki albo z .WA
    if symbol.upper().endswith(".WA") or symbol.isalpha() and symbol.isupper():
        stooq_symbol = symbol.replace(".WA","")
        price = get_price_stooq(stooq_symbol)
        if price is not None:
            return jsonify({"price": price})

    # Zagraniczny symbol (Finhub)
    price = get_price_finnhub(symbol)
    if price is not None:
        return jsonify({"price": price})

    return jsonify({"price": 0})

# Root – może służyć do testu, np. w Renderze
@app.route("/")
def index():
    return "Backend działa. Użyj /get_price?symbol=XXX"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
