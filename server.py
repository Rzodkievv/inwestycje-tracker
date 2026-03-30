from flask import Flask, request, jsonify, send_from_directory
import requests
import csv
import io
import os

app = Flask(__name__, static_folder='.')

# Twój klucz Finnhub
FINNHUB_API_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

# Funkcja do pobrania ceny polskiej spółki ze Stooq
def get_price_stooq(symbol):
    try:
        # Stooq wymaga małych liter i ".pl" dla GPW
        symbol = symbol.lower() + ".pl"
        url = f"https://stooq.pl/q/l/?s={symbol}&f=sd2t2ohlc&h&e=csv"
        res = requests.get(url)
        res.encoding = 'utf-8'
        f = io.StringIO(res.text)
        reader = csv.DictReader(f)
        row = next(reader)
        price = row.get("Close")
        return float(price.replace(",", ".")) if price not in ("N/D", "") else 0
    except Exception as e:
        print("Błąd Stooq:", e)
        return 0

# Funkcja do pobrania ceny zagranicznej spółki przez Finnhub
def get_price_finnhub(symbol):
    try:
        url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
        res = requests.get(url)
        data = res.json()
        return float(data.get("c", 0))
    except Exception as e:
        print("Błąd Finnhub:", e)
        return 0

# Endpoint pobierający aktualną cenę
@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Brak symbolu"}), 400
    
    # Prosta heurystyka: polskie tickery (GPW) są 2-4 literowe
    if symbol.isalpha() and symbol.isupper() and len(symbol) <= 4:
        price = get_price_stooq(symbol)
    else:
        price = get_price_finnhub(symbol)
    
    return jsonify({"c": price})

# Serwowanie pliku index.html
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Obsługa statycznych plików
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
