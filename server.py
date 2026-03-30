from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='.')

# Wklej tutaj swój klucz API z Finnhub
API_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

# Endpoint pobierający aktualną cenę
@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    if not symbol:
        return jsonify({"error": "Brak symbolu"}), 400
    try:
        # Pobieramy dane z Finnhub
        res = requests.get(
            f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={API_KEY}"
        )
        data = res.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serwowanie pliku index.html pod adresem głównym
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

# Obsługa statycznych plików (np. JS, CSS)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

if __name__ == "__main__":
    # Render ustawia port przez zmienną środowiskową
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
