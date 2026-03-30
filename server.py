from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

@app.route("/get_price")
def get_price():
    symbol = request.args.get("symbol")
    api_key = "d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg"
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={d6cp7i9r01qsiik32bk0d6cp7i9r01qsiik32bkg}"
    res = requests.get(url)
    data = res.json()
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
