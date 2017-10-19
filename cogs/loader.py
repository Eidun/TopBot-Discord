import discord
from discord.ext import commands
from models.active_user import UserModel
import db.db_adapter as db
import data


class Loader:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def load(self, ctx):
        """Gets all messages data"""
        # Initializing values
        counter = 0
        checkpoint = 0
        channels = self.bot.get_all_channels()
        members = ctx.message.server.members
        # Bots are not members
        members = list(filter(lambda x: not x.bot, members))
        messages = []

        for channel in channels:
            # Check if test channel
            if channel.id in data.text_channels:
                await self.bot.send_message(ctx.message.channel, 'Recovering from ' + channel.name + '...')
                checkpoint = 0
                channel_counter = 0
                # Messages from channel
                async for message in self.bot.logs_from(channel, limit=80000):
                    counter += 1
                    channel_counter += 1
                    checkpoint += 1
                    # Add new message
                    messages.append(message)
                    if checkpoint == 5000:
                        checkpoint = 0
                        await self.bot.send_message(ctx.message.channel, '----{}: {} messages...'.format(channel.name, counter))
                await self.bot.send_message(ctx.message.channel, '----Done with {} messages'.format(channel_counter))

        # Assign messages to users
        for member in members:
            member_messages = list(filter(lambda x: x.author == member, messages))
            member_messages.sort(key=lambda x: x.timestamp, reverse=True)
            # At least one message
            if member_messages.__len__() > 0:
                last_message_date = member_messages[0].timestamp
                new_user = UserModel(member.id, member.display_name, member.joined_at,
                                     last_message_date, member_messages.__len__(), active=0, update=True)
                data.users[new_user.user_id] = new_user

        data.total_messages = counter
        await self.bot.send_message(ctx.message.channel, 'There are {} messages'.format(counter))

    @commands.command()
    @commands.has_role('Admin')
    async def save(self):
        """Saves current data in DB"""
        db.user_saving()
        db.channel_saving()


def setup(bot):
    bot.add_cog(Loader(bot))
