"""Program to start botting..."""

import os

from host import Host
from bot import Bot


def main() :
    """Start botting"""
    # Get Bot Token from envirement
    # load_dotenv(dotenv_path=Path(".env"))
    token = os.getenv('TOKEN') or ""
    host = os.getenv('RM_HOST') or ''
    port = os.getenv('RM_PORT') or ''
    username = os.getenv('RM_USER') or ''
    password = os.getenv('RM_PASSWORD') or ''

    host = Host(host=host, port=int(port), login=username, password=password)

    # Create new Bot
    bot = Bot(token, host=host)

    # Start echoBot
    bot.start_botting()



if __name__ == "__main__":
    main()
