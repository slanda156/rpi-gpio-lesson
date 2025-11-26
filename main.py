#!/usr/bin/env python3
# Import built-in modules
import logging
# Import third-party modules

# Import local modules
from src import createCrashLog
from src.app import GPIOApp
from src.config import saveConfig, CONFIG

logger = logging.getLogger(__name__)

# Define the main function
def main() -> None:
    app = GPIOApp()
    app.run()
    saveConfig(CONFIG)


# Run the program if it is the main module
if __name__ == "__main__":
    try:
        main()
    # Log any exceptions
    except Exception as e:
        logger.critical("An unhandled exception occurred:", exc_info=True)
        createCrashLog(e)
        raise
