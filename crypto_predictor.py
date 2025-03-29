import requests import numpy as np import talib from flask import Flask, jsonify

app = Flask(name)

Function to fetch real-time crypto prices

def get_crypto_price(symbol): url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}" response = requests.get(url) data = response.json() return float(data['price']) if 'price' in data else None

Function to fetch historical data for technical analysis

def get_historical_data(symbol, interval='1h', limit=50): url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}" response = requests.get(url) data = response.json() close_prices = [float(candle[4]) for candle in data]  # Closing prices return np.array(close_prices)

Function to analyze market trends using technical indicators

def analyze_market(symbol): prices = get_historical_data(symbol) if len(prices) < 20: return {"error": "Not enough data for analysis"}

# Apply technical indicators
rsi = talib.RSI(prices, timeperiod=14)[-1]
macd, signal, _ = talib.MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9)
macd_signal = macd[-1] - signal[-1]

# Determine trend
if rsi > 70 and macd_signal > 0:
    signal = "Strong Bullish"
elif rsi < 30 and macd_signal < 0:
    signal = "Strong Bearish"
elif macd_signal > 0:
    signal = "Bullish"
elif macd_signal < 0:
    signal = "Bearish"
else:
    signal = "Neutral"

return {"symbol": symbol, "latest_price": prices[-1], "RSI": round(rsi, 2), "MACD_Signal": round(macd_signal, 2), "prediction": signal}

@app.route('/predict/<symbol>', methods=['GET']) def predict(symbol): result = analyze_market(symbol.upper()) return jsonify(result)

if name == 'main': app.run(host='0.0.0.0', port=5000)

