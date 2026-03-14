import argparse
from bot.client import BinanceClient
from bot.orders import OrderManager
from bot.validators import validate_order
from bot.logging_config import setup_logger

logger = setup_logger()

def main():

    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot")

    parser.add_argument("--symbol", required=True)
    parser.add_argument("--side", required=True)
    parser.add_argument("--type", required=True)
    parser.add_argument("--quantity", type=float, required=True)
    parser.add_argument("--price", type=float)

    args = parser.parse_args()

    try:

        validate_order(
            args.symbol,
            args.side,
            args.type,
            args.quantity,
            args.price
        )

        client = BinanceClient().client
        orders = OrderManager(client)

        print("\nOrder Request Summary")
        print("-----------------------")
        print("Symbol:", args.symbol)
        print("Side:", args.side)
        print("Type:", args.type)
        print("Quantity:", args.quantity)
        print("Price:", args.price)

        if args.type.upper() == "MARKET":
            response = orders.place_market_order(
                args.symbol,
                args.side,
                args.quantity
            )

        else:
            response = orders.place_limit_order(
                args.symbol,
                args.side,
                args.quantity,
                args.price
            )

        print("\nOrder Response")
        print("-----------------------")
        print("Order ID:", response["orderId"])
        print("Status:", response["status"])
        print("Executed Qty:", response["executedQty"])

        if "avgPrice" in response:
            print("Avg Price:", response["avgPrice"])

        print("\nSUCCESS: Order placed successfully")

    except Exception as e:

        logger.error(f"Order failed: {e}")
        print("ERROR:", e)


if __name__ == "__main__":
    main()