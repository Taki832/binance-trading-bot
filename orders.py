"""
Order placement logic for Binance Futures (USDT-M Testnet).

Provides a single high-level function ``place_order`` that
builds the correct payload, sends it, and returns the API response.
"""

from __future__ import annotations

import logging
from typing import Any

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceRequestException

logger = logging.getLogger("trading_bot.orders")


# ── Helpers ────────────────────────────────────────────────────


def _build_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> dict[str, Any]:
    """Assemble the keyword arguments for ``futures_create_order``."""
    params: dict[str, Any] = {
        "symbol": symbol.upper(),
        "side": side.upper(),
        "type": order_type.upper(),
        "quantity": quantity,
    }

    if order_type.upper() == "LIMIT":
        params["timeInForce"] = "GTC"
        params["price"] = str(price)

    return params


def _format_avg_price(response: dict[str, Any]) -> str:
    """
    Extract a human-readable average price from the API response.

    Binance returns avgPrice as "0" or "0.00000000" for unfilled
    LIMIT orders — display "N/A" in those cases.
    """
    raw = response.get("avgPrice")
    if raw is None:
        return "N/A"
    try:
        value = float(raw)
        return f"{value:g}" if value > 0 else "N/A"
    except (ValueError, TypeError):
        return "N/A"


def _print_order_summary(params: dict[str, Any]) -> None:
    """Display a human-friendly order preview before placing."""
    border = "═" * 40
    print(f"\n╔{border}╗")
    print(f"║{'📋  ORDER SUMMARY':^40}║")
    print(f"╠{border}╣")
    print(f"║  {'Symbol':<14}:  {params['symbol']:<20}  ║")
    print(f"║  {'Side':<14}:  {params['side']:<20}  ║")
    print(f"║  {'Type':<14}:  {params['type']:<20}  ║")
    print(f"║  {'Quantity':<14}:  {str(params['quantity']):<20}  ║")
    if "price" in params:
        print(f"║  {'Price':<14}:  {params['price']:<20}  ║")
        print(f"║  {'Time-in-Force':<14}:  {params['timeInForce']:<20}  ║")
    print(f"╚{border}╝\n")


def _print_order_response(response: dict[str, Any]) -> None:
    """Display the key fields from the API response."""
    avg_price = _format_avg_price(response)
    order_id = str(response.get("orderId", "N/A"))
    status = response.get("status", "N/A")
    executed_qty = response.get("executedQty", "N/A")

    border = "═" * 40
    print(f"╔{border}╗")
    print(f"║{'✅  ORDER RESPONSE':^40}║")
    print(f"╠{border}╣")
    print(f"║  {'Order ID':<14}:  {order_id:<20}  ║")
    print(f"║  {'Status':<14}:  {status:<20}  ║")
    print(f"║  {'Executed Qty':<14}:  {executed_qty:<20}  ║")
    print(f"║  {'Avg Price':<14}:  {avg_price:<20}  ║")
    print(f"╚{border}╝\n")


# ── Public API ─────────────────────────────────────────────────


def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
) -> dict[str, Any]:
    """
    Place a Futures order on Binance Testnet.

    Parameters
    ----------
    client : Client
        An authenticated ``binance.client.Client``.
    symbol : str
        Trading pair (e.g. ``"BTCUSDT"``).
    side : str
        ``"BUY"`` or ``"SELL"``.
    order_type : str
        ``"MARKET"`` or ``"LIMIT"``.
    quantity : float
        Order size in base asset units.
    price : float | None
        Required for LIMIT orders.

    Returns
    -------
    dict
        The raw JSON response from the API.

    Raises
    ------
    BinanceAPIException
        On API-level errors (e.g. insufficient balance).
    BinanceRequestException
        On network / request-level errors.
    """
    params = _build_order_params(symbol, side, order_type, quantity, price)

    # ── Pre-flight summary ─────────────────────────────────────
    _print_order_summary(params)

    logger.info(
        "Placing %s %s order: %s × %s%s",
        side, order_type, symbol, quantity,
        f" @ {price}" if price else "",
    )
    logger.debug("Request params: %s", params)

    # ── Send to Binance ────────────────────────────────────────
    try:
        response = client.futures_create_order(**params)

    except BinanceAPIException as exc:
        logger.error(
            "Binance API error [code %s]: %s", exc.code, exc.message
        )
        raise

    except BinanceRequestException as exc:
        logger.error("Binance request / network error: %s", exc)
        raise

    except ConnectionError as exc:
        logger.error("Network connection lost: %s", exc)
        raise

    except Exception as exc:
        logger.error("Unexpected error placing order: %s", exc)
        raise

    # ── Success ────────────────────────────────────────────────
    logger.info(
        "Order placed — ID: %s | Status: %s | Filled: %s",
        response.get("orderId"),
        response.get("status"),
        response.get("executedQty"),
    )
    logger.debug("Full API response: %s", response)

    _print_order_response(response)
    return response
