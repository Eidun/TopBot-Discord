from discord.ext import commands
import db.db_adapter as db
import data
import utils.roles_assigment as r


class Reset:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @r.has_role_id(370630936561451008)
    async def warning_reset(self, ctx):
        """WARNING, deletes everything"""
        db.initialize()
        data.users = {}
        data.bot_channels = {}
        data.total_messages = 0
        data.text_channels = {}
        await self.bot.send_message(ctx.message.channel, 'Database reset')


def setup(bot):
    bot.add_cog(Reset(bot))
