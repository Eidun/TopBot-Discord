import datetime

import discord
from discord.ext import commands

import data
from utils.users_sorter import get_join_rank, get_messages_rank, get_top20


class Info:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def info(self, ctx, user: discord.Member=None):
        """<User> User self if empty. Shows user info"""
        if user is None:
            user = ctx.message.author
        print(user.id)
        print(data.users)
        if user.id not in data.users:
            return

        user = data.users[user.id]
        print(user)
        embed = discord.Embed(
            title=user.name,
            color=0x0f5ea3
        )
        join_rank = get_join_rank(user)
        messages_rank = get_messages_rank(user)
        date = user.join_date.strftime("%d.%m.%y")
        embed.add_field(name='Joined:', value=date + ' (' + str(join_rank) + '/' + str(len(data.users)) + ')')
        embed.add_field(name='Messages:',
                        value=str(user.messages) + ' (' + str(messages_rank) + '/' + str(len(data.users)) + ')')
        await self.bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def top20(self, ctx):
        """Top 20 best users"""
        top = get_top20()
        output = 'Top 20:\n'
        count = 1
        for user in top:
            output += '#' + str(count) + '- ' + user.name + ' - ' + str(user.messages) + ' messages\n'
            count += 1
        await self.bot.send_message(ctx.message.channel, output)

    @commands.command(pass_context=True)
    async def inactive(self, ctx):
        """Users that didn't write a message in 6 months"""
        users = data.users.values()
        today = datetime.date.today()

        # We subtract 6 months
        new_month = today.month
        new_year = today.year
        if today.month < 7:
            new_month += 12
            new_year -= 1
        new_month -= 6
        inactive_barrier = datetime.date(new_year, new_month, today.day)
        # Get uses with last message date before than the inactive barrier
        inactive_users = list(filter(lambda x: x.last_message_date.date() < inactive_barrier, users))
        inactive_users.sort(key=lambda x: x.last_message_date, reverse=True)

        # Build the output message
        output = 'Inactive users:\n'
        for inactive in inactive_users:
            date = inactive.last_message_date.strftime("%d.%m.%y")
            output += inactive.name + ' - Last Message: ' + date + '\n'
        await self.bot.send_message(ctx.message.channel, output)


def setup(bot):
    bot.add_cog(Info(bot))
