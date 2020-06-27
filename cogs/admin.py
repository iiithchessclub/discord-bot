from discord.ext import commands

from time import time
from os.path import getmtime
from pathlib import Path
import sys
import logging

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_loaded = time()
        self.limit = 0
        self.cog_list = []
        self._cache_cog_list()

    def _cache_cog_list(self):
        self.cog_list = [str(file).replace('/', '.').replace('.py', '') for file in Path('cogs').glob('**/*.py')]

    @commands.group(brief='Bot management commands', invoke_without_command=True)
    @commands.is_owner()
    async def hotpatch(self, ctx):
        await ctx.send_help(ctx.command)

    @hotpatch.command(brief='Hotpatch all modified cogs. Cooldown of 60s.')
    @commands.is_owner()
    async def reload(self, ctx):
        cur_time = time()
        if cur_time - self.last_loaded < self.limit:
            await ctx.send(f'Please wait for {self.limit}s before reloading')

        else:
            reloaded = []

            for extension in self.cog_list:
                if extension in ['cogs.admin', 'cogs.errors']:
                    continue

                if getmtime(extension.replace('.', '/') + '.py') > self.last_loaded:
                    try:
                        self.bot.reload_extension(extension)
                        logging.info(f'[HOTPATCH] reloaded cog: {extension}')
                    except commands.errors.ExtensionNotLoaded:
                        self.bot.load_extension(extension)
                        logging.info(f'[HOTPATCH] loaded new cog: {extension}')

                    reloaded.append(extension)

            self.last_loaded = cur_time
            await ctx.send(f'Reloaded cogs: {", ".join(reloaded)}')

    @hotpatch.command(brief='Set the cooldown limit for hotpatching.', usage='[seconds]')
    @commands.is_owner()
    async def setlimit(self, ctx, lim: int):
        self.limit = lim
        await ctx.send(f'Changed the reload limit to {lim}s.')
    
    @hotpatch.command(brief='Recompute extensions list.')
    @commands.is_owner()
    async def recache(self, ctx):
        self._cache_cog_list()
        await ctx.send(f'Recached cogs: {", ".join(self.cog_list)}.')

    @hotpatch.command(brief='Shutdown the bot.')
    @commands.is_owner()
    async def shutdown(self, ctx):
        sys.exit(0)

def setup(bot):
    bot.add_cog(Admin(bot))
