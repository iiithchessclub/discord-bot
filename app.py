from discord.ext import commands
import logging
import json

from pathlib import Path
from os import environ
import config

def setup_logging():
    loglevel = logging.DEBUG if config.get('DEBUG_MODE') else logging.INFO
    logdir = config.get('APP_LOG_DIR', 'logs/')

    botlog = logdir + config.get('BOT_LOG_FILE', 'discord.log')
    bot_logger = logging.getLogger('discord')
    bot_logger.setLevel(loglevel)
    handler = logging.FileHandler(filename=botlog, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter('[%(levelname)s] (%(asctime)s) %(name)s: %(message)s'))
    bot_logger.addHandler(handler)

    applog = logdir + config.get('APP_LOG_FILE', 'app.log')
    app_logger = logging.getLogger()
    app_logger.setLevel(loglevel)
    handler = logging.FileHandler(filename=applog, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter('[%(levelname)s] (%(asctime)s) %(name)s: %(message)s'))
    app_logger.addHandler(handler)

def main():
    # Setup logging
    setup_logging()

    # Setup Bot
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.PREFIX))
    cog_list = [str(file).replace('/', '.').replace('.py', '') for file in Path('cogs').glob('**/*.py')]
    for extension in cog_list:
        try:
            bot.load_extension(extension)
        except Exception as e:
            logging.warning(f'[COG] LOAD FAILED: {extension}')
            logging.warning(str(e))
        else:
            logging.info(f'[COG] Loaded {extension}!')

    @bot.event
    async def on_ready():
        logging.info(f'Logged in as {bot.user}')

    # Dry run, to verify the code
    if config.get('DRY_RUN'):
        return

    # Connect
    bot.run(config.BOT_TOKEN)

if __name__ == "__main__":
    main()
