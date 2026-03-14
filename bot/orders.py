import logging
from binance.enums import *

logger = logging.getLogger(__name__)

class OrderManager:

    def __init__(self, client):
        self.client = client

    def place_market_order(self, symbol, side, quantity):

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )

            logger.info(f"Market order response: {order}")
            return order

        except Exception as e:
            logger.error(f"Market order failed: {e}")
            raise

    def place_limit_order(self, symbol, side, quantity, price):

        try:
            order = self.client.futures_create_order(
                symbol=symbol,
                side=side,
                type=FUTURE_ORDER_TYPE_LIMIT,
                quantity=quantity,
                price=price,
                timeInForce=TIME_IN_FORCE_GTC
            )

            logger.info(f"Limit order response: {order}")
            return order

        except Exception as e:
            logger.error(f"Limit order failed: {e}")
            raise