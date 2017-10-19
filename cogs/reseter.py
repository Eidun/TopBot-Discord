from discord.ext import commands
import db.db_adapter as db
import data

class Reset:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def warning_reset(self, ctx):
        db.initialize()
        data.users = {}
        data.bot_channels = {}
        data.total_messages = 0
        data.text_channels = {}
        await self.bot.send_message(ctx.message.channel, 'Database reset')


def setup(bot):
    bot.add_cog(Reset(bot))
