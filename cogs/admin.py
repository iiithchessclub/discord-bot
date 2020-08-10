from discord.ext import commands
import discord.utils as utils

from time import time
from os.path import getmtime
from pathlib import Path
import sys
import logging

import config

WHITE_CHECK_MARK = u"\u2705"

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.last_loaded = time()
        self.limit = 60
        self.cog_list = []
        self._cache_cog_list()

    def _cache_cog_list(self):
        self.cog_list = [str(file).replace('/', '.').replace('.py', '') for file in Path('cogs').glob('**/*.py')]

    @commands.group(brief='Bot management commands', invoke_without_command=True)
    @commands.is_owner()
    async def admin(self, ctx):
        await ctx.send_help(ctx.command)

    @admin.command(brief='Hotpatch all modified cogs. Cooldown of 60s.')
    @commands.is_owner()
    async def reload(self, ctx):
        cur_time = time()
        if cur_time - self.last_loaded < self.limit:
            await ctx.send(f'Please wait for {self.limit}s before reloading')

        else:
            logging.info('Hotpatching cogs...')

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

    @admin.command(brief='Set the cooldown limit for hotpatching.', usage='[seconds]')
    @commands.is_owner()
    async def setlimit(self, ctx, lim: int):
        self.limit = lim
        await ctx.send(f'Changed the reload limit to {lim}s.')
    
    @admin.command(brief='Recompute extensions list.')
    @commands.is_owner()
    async def recache(self, ctx):
        self._cache_cog_list()
        await ctx.send(f'Recached cogs: {", ".join(self.cog_list)}.')

    @admin.command(brief='Shutdown the bot.')
    @commands.is_owner()
    async def shutdown(self, ctx):
        sys.exit(0)

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild = None
        self.verified_role = None
        self.unregistered_role = None

    def update_guild(self, guild_id):
        self.guild = utils.get(self.bot.guilds, id=guild_id)
        self.verified_role = utils.get(self.guild.roles, name='Verified')
        self.unregistered_role = utils.get(self.guild.roles, name='unregistered')

    # Verify user when they react to the rules message
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.guild_id is None:
            return

        if payload.message_id != config.dynamic.get('rules_accept_message'):
            return

        self.update_guild(payload.guild_id)

        member = self.guild.get_member(payload.user_id)

        await member.add_roles(self.verified_role)
        await member.remove_roles(self.unregistered_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.guild_id is None:
            return

        if payload.message_id != config.dynamic.get('rules_accept_message'):
            return

        self.update_guild(payload.guild_id)

        member = self.guild.get_member(payload.user_id)

        await member.remove_roles(self.verified_role)

    @commands.group(brief='Server management commands', invoke_without_command=True)
    @commands.has_role('Admin')
    async def server(self, ctx):
        await ctx.send_help(ctx.command)

    @server.command(brief='Select new rules messages')
    @commands.has_role('Admin')
    async def rulesmessage(self, ctx, type: str, id: int):
        if type == 'rules':
            config.dynamic.set('rules_message', id)

        if type == 'accept':
            config.dynamic.set('rules_accept_message', id)
            rules_channel = utils.get(ctx.guild.text_channels, name='server-rules')
            rules_message = await rules_channel.fetch_message(id)
            await rules_message.add_reaction(WHITE_CHECK_MARK)

        await ctx.send('Updated IDs')

    @server.command(brief='Update the rules')
    @commands.has_role('Admin')
    async def updaterules(self, ctx):
        self.update_guild(ctx.guild.id)
        rules_channel = utils.get(self.guild.text_channels, name='server-rules')

        rules_id = config.dynamic.get('rules_message')
        rules_data = ''
        try:
            with open('data/rules.txt') as f:
                rules_data = f.readlines()
                rules_data = ''.join(rules_data)
        except:
            pass

        if rules_id and rules_data:
            rules_message = await rules_channel.fetch_message(rules_id)
            await rules_message.edit(content=rules_data)

        rules_accept_id = config.dynamic.get('rules_accept_message')
        rules_accept_data = ''
        try:
            with open('data/rules_accept.txt') as f:
                rules_accept_data = f.readlines()
                rules_accept_data = ''.join(rules_accept_data)
        except:
            pass

        if rules_accept_id and rules_accept_data:
            rules_message = await rules_channel.fetch_message(rules_accept_id)
            await rules_message.edit(content=rules_accept_data)

        await ctx.send('Rules updated successfully!')

def setup(bot):
    bot.add_cog(Admin(bot))
    bot.add_cog(ServerManagement(bot))
