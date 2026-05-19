#!/usr/bin/env python3
"""Main Trading Bot Entry Point"""

import json
import logging
import sys
from pathlib import Path
from src.trader import TradingEngine

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("logs/trading_bot.log"),
        logging.StreamHandler(),
    ],
)

logger = logging.getLogger(__name__)


def load_config():
    """Load configuration from config.json"""
    config_path = Path("config.json")
    if not config_path.exists():
        logger.error("config.json not found")
        sys.exit(1)

    with open(config_path) as f:
        return json.load(f)


def main():
    """Main function"""
    logger.info("="*50)
    logger.info("Starting Forex & Binary Options Trading Bot")
    logger.info("="*50)

    try:
        # Load configuration
        config = load_config()
        logger.info("Configuration loaded")

        # Create and start trading engine
        engine = TradingEngine(config)
        logger.info(f"Using strategy: {config['strategies']['default']}")

        # Run bot
        engine.run(interval=60)

    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
