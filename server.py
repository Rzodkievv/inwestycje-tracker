from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# <-- tutaj wstaw swój klucz Finnhub
API_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

# Endpoint główny: zwraca index.html
@app.route("/")
def index():
    return send_from_directory(os.path.dirname(os.path.abspath(__file__)), "index.html")

# Endpoint do pobierania ceny
@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Brak symbolu"}), 400

    # Polska spółka (GPW) kończy się .WA lub sam symbol jest z GPW
    if symbol.endswith(".WA") or symbol.isalpha():
        fetch_symbol = f"GPW:{symbol.replace('.WA','')}"
    else:
        fetch_symbol = symbol

    try:
        res = requests.get(f"https://finnhub.io/api/v1/quote?symbol={fetch_symbol}&token={API_KEY}")
        data = res.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 0.0.0.0 żeby Render mógł wystawić serwis publicznie
    app.run(host="0.0.0.0", port=5000)
