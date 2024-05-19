"""Program to start botting..."""
import logging
import os

from pathlib import Path
from dotenv import load_dotenv

from host import Host
from bot import Bot

logger = logging.getLogger(__name__)

def main() :
    """Start botting"""
    # Get environments from file
    load_dotenv(dotenv_path=Path(".env"))

    # Get environments
    token = os.getenv('TOKEN') or ''
    host = os.getenv('RM_HOST') or 'localhost'
    port = os.getenv('RM_PORT') or '22'
    username = os.getenv('RM_USER') or 'root'
    password = os.getenv('RM_PASSWORD') or ''
    db_name = os.getenv('DB_DATABASE') or 'tgbot'

    logging.basicConfig(
        filename='logfile.txt',
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.INFO
    )

    # Create connections to host
    host = Host(host=host, port=int(port), login=username, password=password,
                logger=logger)

    # Create new Bot
    bot = Bot(token, host=host, db_name=db_name, logger=logger)

    # Start echoBot
    bot.start_botting()



if __name__ == "__main__":
    main()
