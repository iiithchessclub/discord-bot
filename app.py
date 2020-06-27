from discord.ext import commands
import logging
import json

from pathlib import Path
from os import environ

def setup_logging(config):
    loglevel = logging.DEBUG if config.get('DEBUG_MODE') else logging.INFO

    botlog = config.get('botlogfile') or 'discord.log'
    bot_logger = logging.getLogger('discord')
    bot_logger.setLevel(loglevel)
    handler = logging.FileHandler(filename='logs/' + botlog, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    bot_logger.addHandler(handler)

    applog = config.get('applogfile') or 'app.log'
    app_logger = logging.getLogger()
    app_logger.setLevel(loglevel)
    handler = logging.FileHandler(filename='logs/' + applog, encoding='utf-8', mode='a+')
    handler.setFormatter(logging.Formatter('[%(levelname)s] (%(asctime)s) %(name)s: %(message)s'))
    app_logger.addHandler(handler)

def main():
    # Load config
    config = json.load(open('config/config.json'))

    # Setup logging
    setup_logging(config)

    # Setup Bot
    bot = commands.Bot(command_prefix=commands.when_mentioned_or(config.get('prefix')))
    cog_list = [str(file).replace('/', '.').replace('.py', '') for file in Path('cogs').glob('**/*.py')]
    for extension in cog_list:
        try:
            bot.load_extension(extension)
        except:
            logging.warning(f'[COG] LOAD FAILED: {extension}')
        else:
            logging.info(f'[COG] Loaded {extension}!')

    @bot.event    
    async def on_ready():
        logging.info(f'Logged in as {bot.user}')

    # Connect
    bot.run(config.get('token') or environ['DISCORD_BOT_TOKEN'])

if __name__ == "__main__":
    main()
