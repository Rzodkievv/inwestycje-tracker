from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# <-- Podmień na swój klucz Finnhub -->
API_KEY = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"

# Lista zagranicznych giełd (przykładowo)
FOREIGN_TICKERS = ['AAPL', 'MSFT', 'TSLA', 'GOOGL', 'AMZN', 'FB']

@app.route('/get_price')
def get_price():
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "Nie podano symbolu"}), 400

    symbol = symbol.upper()

    # Jeśli symbol jest na liście zagranicznych giełd, używamy normalnego tickera
    if symbol in FOREIGN_TICKERS:
        fetch_symbol = symbol
    else:
        # Polskie spółki GPW
        fetch_symbol = f"GPW:{symbol}"

    try:
        res = requests.get(f"https://finnhub.io/api/v1/quote?symbol={fetch_symbol}&token={API_KEY}")
        data = res.json()
        # Finnhub zwraca klucze: c (current), h (high), l (low), o (open), pc (prev close)
        # Jeśli brak ceny, zwracamy 0
        return jsonify({
            "c": data.get("c", 0),
            "h": data.get("h", 0),
            "l": data.get("l", 0),
            "o": data.get("o", 0),
            "pc": data.get("pc", 0),
            "t": data.get("t", 0)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
