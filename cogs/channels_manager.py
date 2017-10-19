import discord
import data
from discord.ext import commands
from models.active_channels import ChannelsModel

class Channels:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def add_channel(self, ctx, channel: discord.Channel):
        """<channel name>"""
        if channel.id not in data.text_channels:
            active_channel = ChannelsModel(channel.id, channel.name, False)
            data.text_channels[channel.id] = active_channel
            await self.bot.send_message(ctx.message.channel, channel.name + ' added to text channels.')

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def remove_channel(self, ctx, channel: discord.Channel):
        """<channel name>"""
        if channel.id in data.text_channels:
            del data.text_channels[channel.id]
            await self.bot.send_message(ctx.message.channel, channel.name + ' removed from text channels.')

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def get_channels(self, ctx):
        """Writes the list of the text channels"""
        output = 'There is a total of {} channels:'.format(len(data.text_channels))
        for channel in data.text_channels.values():
            output += '\n\t-' + channel.name
        await self.bot.send_message(ctx.message.channel, output)

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def get_bot_channels(self, ctx):
        """Writes the list of the bot channels"""
        output = 'Number of {} channels:'.format(len(data.bot_channels))
        for channel in data.bot_channels.values():
            output += '\n\t-' + channel.name
        await self.bot.send_message(ctx.message.channel, output)

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def add_bot_channel(self, ctx, channel: discord.Channel):
        """<channel name>"""
        if channel.id not in data.bot_channels:
            active_channel = ChannelsModel(channel.id, channel.name, True)
            data.bot_channels[channel.id] = active_channel
            await self.bot.send_message(ctx.message.channel, channel.name + ' added to bot channels.')

    @commands.command(pass_context=True)
    @commands.has_role('Admin')
    async def remove_bot_channel(self, ctx, channel: discord.Channel):
        """<channel name>"""
        if channel.id in data.bot_channels:
            del data.bot_channels[channel.id]
            await self.bot.send_message(ctx.message.channel, channel.name + ' removed from bot channels.')


def setup(bot):
    bot.add_cog(Channels(bot))
