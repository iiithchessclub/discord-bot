from discord.ext import commands

class Lichess(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.group(brief='Commands for using Lichess', invoke_without_command=True)
    async def lichess(self, ctx):
        await ctx.send_help(ctx.command)

def setup(bot):
    bot.add_cog(Lichess(bot))
