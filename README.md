# Binance Futures Testnet — Trading Bot

This project was built with a focus on clean architecture, reliability, and handling real-world API edge cases such as minimum notional requirements and insufficient margin.

A clean, modular CLI bot for placing **MARKET** and **LIMIT** orders on the
Binance USDT-M **Futures Testnet**. No real money is used.

---
## Notes

- Binance requires a minimum notional value (~$100) for orders
- Insufficient margin errors can occur on larger quantities
- Orders may remain in NEW status until matched in market

## Project Structure

```
trading_bot/
├── cli.py              # CLI entry point (argparse)
├── client.py           # Binance client setup & connectivity
├── orders.py           # Order building, placement & response display
├── validators.py       # Input validation (symbol, side, type, qty, price)
├── logging_config.py   # Dual-output logging (console + bot.log)
├── .env                # API credentials (never commit this)
├── .gitignore          # Excludes .env, bot.log, __pycache__, venv
├── requirements.txt    # Python dependencies
└── README.md           # ← you are here
```

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Python      | 3.10+   |
| pip         | latest  |

---

## Setup

### 1. Navigate to the project

```bash
cd trading_bot
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Testnet API keys

1. Go to <https://testnet.binancefuture.com/> and create an account.
2. Generate an **API Key** and **Secret**.
3. Open `.env` and replace the placeholders:

```dotenv
BINANCE_API_KEY=your_actual_key
BINANCE_API_SECRET=your_actual_secret
```

> ⚠️ **Never commit `.env` to version control.** A `.gitignore` is included.

---

## Usage

```bash
python cli.py --symbol <PAIR> --side <BUY|SELL> --type <MARKET|LIMIT> --quantity <QTY> [--price <PRICE>]
```

### Arguments

| Flag         | Required   | Description                                  |
|--------------|------------|----------------------------------------------|
| `--symbol`   | ✅ Yes     | Trading pair ending with USDT (e.g. BTCUSDT) |
| `--side`     | ✅ Yes     | `BUY` or `SELL`                              |
| `--type`     | ✅ Yes     | `MARKET` or `LIMIT`                          |
| `--quantity` | ✅ Yes     | Amount in base asset (e.g. 0.01)             |
| `--price`    | LIMIT only | Limit price (ignored for MARKET orders)      |

---

## Example Commands

### Market Buy — 0.01 BTC

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
```

### Market Sell — 0.1 ETH

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.1
```

### Limit Buy — 0.01 BTC at $60,000

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.01 --price 60000
```

### Limit Sell — 0.5 ETH at $3,200

```bash
python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3200
```

---

## Sample Output

```
INFO     | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFO     |   Binance Futures Testnet Trading Bot
INFO     | ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
INFO     | Connected to Binance Futures Testnet ✓

╔════════════════════════════════════════╗
║           📋  ORDER SUMMARY           ║
╠════════════════════════════════════════╣
║  Symbol         :  BTCUSDT              ║
║  Side           :  BUY                  ║
║  Type           :  MARKET               ║
║  Quantity       :  0.01                 ║
╚════════════════════════════════════════╝

╔════════════════════════════════════════╗
║          ✅  ORDER RESPONSE           ║
╠════════════════════════════════════════╣
║  Order ID       :  123456789            ║
║  Status         :  FILLED               ║
║  Executed Qty   :  0.01                 ║
║  Avg Price      :  87654.32             ║
╚════════════════════════════════════════╝

🎉  Order executed successfully!
```

---

## Logging

All activity is logged to **two outputs**:

| Destination | Level   | Format                                | Purpose               |
|-------------|---------|---------------------------------------|------------------------|
| Console     | `INFO`  | `LEVEL \| message`                    | Quick user feedback    |
| `bot.log`   | `DEBUG` | `timestamp \| LEVEL \| module \| msg` | Detailed debugging log |

Each run adds a session separator in `bot.log` for easy navigation.

---

## Error Handling

| Scenario              | What happens                                     |
|-----------------------|--------------------------------------------------|
| Invalid input         | Clear error message + exit code 1                |
| Missing API keys      | Points you to the `.env` file + signup URL       |
| Network failure       | Connection error with detail + exit code 1       |
| Binance API error     | Error code + message logged + exit code 1        |

---

## Validation Rules

| Field      | Rule                                      |
|------------|-------------------------------------------|
| `symbol`   | Uppercase, letters only, must end in USDT |
| `side`     | Must be `BUY` or `SELL`                   |
| `type`     | Must be `MARKET` or `LIMIT`               |
| `quantity` | Must be a positive number                 |
| `price`    | Required and positive for LIMIT orders    |

---

## License

MIT — use freely.
