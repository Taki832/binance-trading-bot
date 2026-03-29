"""
Binance Futures Testnet client initialisation.

Loads API credentials from .env and returns a ready-to-use
``binance.client.Client`` instance pointed at the USDT-M
Futures Testnet.
"""

import os
import logging
from pathlib import Path

from dotenv import load_dotenv
from binance.client import Client

logger = logging.getLogger("trading_bot.client")

# ── Binance Futures Testnet endpoints ──────────────────────────
FUTURES_TESTNET_BASE = "https://testnet.binancefuture.com"
FUTURES_TESTNET_API  = FUTURES_TESTNET_BASE + "/fapi"

# ── Load .env from the project root ───────────────────────────
_env_path = Path(__file__).parent / ".env"
load_dotenv(_env_path)


def get_client() -> Client:
    """
    Build and return a Binance Client configured for the
    Futures Testnet (USDT-M).

    Raises
    ------
    EnvironmentError
        If API key or secret is missing / still set to the placeholder.
    ConnectionError
        If the testnet cannot be reached.
    """
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()

    # ── Guard: missing or placeholder keys ─────────────────────
    if not api_key or api_key == "your_testnet_api_key_here":
        raise EnvironmentError(
            "BINANCE_API_KEY is not set. "
            "Add your Futures Testnet API key to the .env file.\n"
            "  → Get one at https://testnet.binancefuture.com/"
        )
    if not api_secret or api_secret == "your_testnet_api_secret_here":
        raise EnvironmentError(
            "BINANCE_API_SECRET is not set. "
            "Add your Futures Testnet API secret to the .env file.\n"
            "  → Get one at https://testnet.binancefuture.com/"
        )

    logger.debug("Loaded API key: %s…%s", api_key[:4], api_key[-4:])
    logger.debug("Creating Binance client for Futures Testnet …")

    # ── Create client with testnet flag ────────────────────────
    client = Client(
        api_key=api_key,
        api_secret=api_secret,
        testnet=True,
        requests_params={"timeout": 15},   # 15-second timeout
    )

    # Override Futures REST base → USDT-M Testnet
    client.FUTURES_URL = FUTURES_TESTNET_API
    logger.debug("Futures URL set to: %s", client.FUTURES_URL)

    # ── Connectivity check ─────────────────────────────────────
    try:
        client.futures_ping()
        logger.info("Connected to Binance Futures Testnet ✓")
    except Exception as exc:
        logger.error("Ping failed: %s", exc)
        raise ConnectionError(
            f"Cannot reach Binance Futures Testnet at {FUTURES_TESTNET_BASE}. "
            f"Check your internet connection.\n  Detail: {exc}"
        ) from exc

    return client
