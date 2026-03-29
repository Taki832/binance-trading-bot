#!/usr/bin/env python3
"""
CLI entry point for the Binance Futures Testnet trading bot.

Usage examples
--------------
  # Market buy 0.01 BTC
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

  # Limit sell 0.5 ETH at $3,200
  python cli.py --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.5 --price 3200
"""

from __future__ import annotations

import argparse
import sys

from logging_config import setup_logging
from validators import validate_all
from client import get_client
from orders import place_order


def _build_parser() -> argparse.ArgumentParser:
    """Build and return the argument parser."""
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet — place MARKET / LIMIT orders",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Examples:\n"
            "  python cli.py --symbol BTCUSDT --side BUY  --type MARKET --quantity 0.01\n"
            "  python cli.py --symbol ETHUSDT --side SELL --type LIMIT  --quantity 0.5 --price 3200\n"
        ),
    )

    parser.add_argument(
        "--symbol",
        required=True,
        type=str,
        help="Trading pair ending with USDT (e.g. BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["MARKET", "LIMIT"],
        dest="order_type",
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        type=float,
        help="Order quantity in base asset (e.g. 0.01 for BTC)",
    )
    parser.add_argument(
        "--price",
        required=False,
        type=float,
        default=None,
        help="Limit price — required for LIMIT orders (e.g. 60000)",
    )

    return parser


def main() -> None:
    """Parse arguments, validate, connect, and place the order."""
    logger = setup_logging()

    parser = _build_parser()
    args = parser.parse_args()

    # Normalize symbol to uppercase so users can type "btcusdt"
    args.symbol = args.symbol.upper()

    logger.info("━" * 42)
    logger.info("  Binance Futures Testnet Trading Bot")
    logger.info("━" * 42)

    # ── 1. Validate inputs ──────────────────────────────────────
    try:
        validate_all(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        logger.debug("All inputs validated OK")
    except ValueError as exc:
        logger.error("Validation failed: %s", exc)
        print(f"\n❌  Input error: {exc}")
        sys.exit(1)

    # ── 2. Initialise client ────────────────────────────────────
    try:
        client = get_client()
    except EnvironmentError as exc:
        logger.error("Environment error: %s", exc)
        print(f"\n❌  Config error: {exc}")
        sys.exit(1)
    except ConnectionError as exc:
        logger.error("Connection error: %s", exc)
        print(f"\n❌  Network error: {exc}")
        sys.exit(1)

    # ── 3. Place order ──────────────────────────────────────────
    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
        print("🎉  Order executed successfully!")
        print(f"Note: Order may remain NEW until matched in market")
    except Exception as exc:
        logger.error("Order failed: %s", exc)
        print(f"\n❌  Order failed: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
