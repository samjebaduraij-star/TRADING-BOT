from flask import Flask, render_template, request, jsonify
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_order
from bot.logging_config import setup_logger

logger = setup_logger()
app = Flask(__name__)

# Initialize Binance client and Order Manager
try:
    client = BinanceClient().client
    orders = OrderManager(client)
except Exception as e:
    logger.error(f"Failed to initialize Binance Client: {e}")
    client = None
    orders = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/order', methods=['POST'])
def place_order():
    if not orders:
         return jsonify({"error": "Binance client is not initialized check your API keys."}), 500

    data = request.json
    try:
        symbol = data.get('symbol')
        side = data.get('side')
        order_type = data.get('type')
        quantity = float(data.get('quantity'))
        price = float(data.get('price')) if data.get('price') else None

        # Validate
        validate_order(symbol, side, order_type, quantity, price)

        # Place Order
        if order_type.upper() == 'MARKET':
            response = orders.place_market_order(symbol, side, quantity)
        else:
            response = orders.place_limit_order(symbol, side, quantity, price)

        return jsonify({
            "status": "success",
            "message": "Order placed successfully!",
            "data": response
        })

    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        logger.error(f"Order failed via API: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
