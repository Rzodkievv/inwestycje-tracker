from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Twój klucz Finnhub
API_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Brak symbolu"}), 400

    # Jeśli polska spółka (zakładamy końcówkę .WA), używamy GPW
    if symbol.endswith(".WA") or symbol.isalpha():
        # GPW prefix w Finnhub
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
    app.run(host="0.0.0.0", port=5000)
