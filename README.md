# Binance Futures Trading Bot

Simple Python CLI bot that places Market and Limit orders on Binance Futures Testnet.

## Setup

1 Install dependencies

pip install -r requirements.txt

2 Create .env file

BINANCE_API_KEY=your_key
BINANCE_API_SECRET=your_secret

3 Run examples

Market order:

python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001

Limit order:

python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 60000

## Logs

Logs are stored in:

trading_bot.log
