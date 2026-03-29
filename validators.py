"""
Input validation helpers for CLI arguments.

Every public function either returns silently on success
or raises a ``ValueError`` with a human-readable message.
"""

import re

SUPPORTED_SIDES = ("BUY", "SELL")
SUPPORTED_ORDER_TYPES = ("MARKET", "LIMIT")

# Valid symbol pattern: 2+ uppercase letters followed by "USDT"
# e.g. BTCUSDT, ETHUSDT, SOLUSDT — not "USDT" alone, not "btcusdt"
_SYMBOL_PATTERN = re.compile(r"^[A-Z]{2,}USDT$")


def validate_symbol(symbol: str) -> None:
    """
    Symbol must be an uppercase trading pair ending with USDT.

    Rules:
      - At least 5 characters (e.g. BNBUSDT is the shortest common pair)
      - Must end with "USDT"
      - Letters only (no slashes, numbers, or spaces)
    """
    if not symbol:
        raise ValueError("Symbol cannot be empty.")

    if not symbol.isupper():
        raise ValueError(
            f"Invalid symbol '{symbol}'. "
            f"Symbol must be uppercase — did you mean '{symbol.upper()}'?"
        )

    if not _SYMBOL_PATTERN.match(symbol):
        raise ValueError(
            f"Invalid symbol '{symbol}'. "
            "Symbol must be an uppercase pair ending with USDT "
            "(e.g. BTCUSDT, ETHUSDT, SOLUSDT)."
        )


def validate_side(side: str) -> None:
    """Side must be BUY or SELL."""
    if side not in SUPPORTED_SIDES:
        raise ValueError(
            f"Invalid side '{side}'. Choose from: {', '.join(SUPPORTED_SIDES)}"
        )


def validate_order_type(order_type: str) -> None:
    """Order type must be MARKET or LIMIT."""
    if order_type not in SUPPORTED_ORDER_TYPES:
        raise ValueError(
            f"Invalid order type '{order_type}'. "
            f"Choose from: {', '.join(SUPPORTED_ORDER_TYPES)}"
        )


def validate_quantity(quantity: float) -> None:
    """Quantity must be a positive number."""
    if not isinstance(quantity, (int, float)):
        raise ValueError(
            f"Quantity must be a number, got {type(quantity).__name__}."
        )
    if quantity <= 0:
        raise ValueError(
            f"Quantity must be a positive number, got {quantity}."
        )


def validate_price(price: float | None, order_type: str) -> None:
    """Price is required (and must be positive) for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None:
            raise ValueError(
                "--price is required for LIMIT orders. "
                "Example: --price 60000"
            )
        if not isinstance(price, (int, float)):
            raise ValueError(
                f"Price must be a number, got {type(price).__name__}."
            )
        if price <= 0:
            raise ValueError(
                f"Price must be a positive number, got {price}."
            )


def validate_all(
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None,
) -> None:
    """Run every validation check in sequence."""
    validate_symbol(symbol)
    validate_side(side)
    validate_order_type(order_type)
    validate_quantity(quantity)
    validate_price(price, order_type)
