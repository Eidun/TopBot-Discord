import asyncio
import sys
import traceback
import utils.roles_assigment
import datetime
import discord
from discord.ext import commands

import data
import db.db_adapter as db
import utils.messages_logger as msgs

description = '''Top-Bot is a tool for ranking users based on their activity'''

modules = {'cogs.loader', 'cogs.channels_manager', 'cogs.info', 'cogs.reseter'}

bot = commands.Bot(command_prefix='its.', description=description)


@bot.event
async def on_ready():
    print('Top-Bot starting...')
    print(bot.user.name)
    print(bot.user.id)
    await bot.change_presence(game=discord.Game(name='with our minds'))

    print('Loading cogs...')
    if __name__ == '__main__':
        modules_loaded = 0
        for module in modules:
            try:
                bot.load_extension(module)
                print('\t' + module)
                modules_loaded += 1
            except Exception as e:
                traceback.print_exc()
                print(f'Error loading the extension {module}', file=sys.stderr)
        print(str(modules_loaded) + '/' + str(modules.__len__()) + ' modules loaded')
        print('Systems 100%')
    print('------')
    prepare_bot()


@bot.event
async def on_message(message: discord.Message):
    if data.roles.__len__() == 0:
        norank = discord.utils.get(message.server.roles, name='No Rank')
        userrank = discord.utils.get(message.server.roles, name='User')
        plusrank = discord.utils.get(message.server.roles, name='User Plus')
        data.roles['No Rank'] = norank
        data.roles['User'] = userrank
        data.roles['User Plus'] = plusrank
        data.members = list(message.server.members)
    # Check if it is a command
    if message.content.startswith('its.'):
        #  Check if there is a bot channel configured, discard command if it's not in those channels
        if len(data.bot_channels) == 0 or message.channel.id in data.bot_channels:
            await bot.process_commands(message)
    else:
        # Check if the message is from a text channel
        if len(data.text_channels) > 0 and message.channel.id in data.text_channels:
            msgs.register_message(message)


async def check_activity_today():
    while not bot.is_closed:
        await asyncio.sleep(3000)
        print('Checking activity...')
        today = datetime.datetime.today().day
        for user in data.users.values():
            print(user.revised)
            print(user.activity)
            if user.revised is None or user.revised != today:
                user.revised = today
                if today == user.last_message_date.day:
                    user.add_activity()
                else:
                    user.sub_activity()
                member = discord.utils.get(data.members, display_name=user.name)
                if user.update_rank:
                    print('Removing last rank')
                    print(user.last_rank)
                    print(member.roles)
                    print(member.top_role.name)
                    await bot.remove_roles(member, member.top_role)
                    print(member.roles)
                    user.update_last()
                print(user.rank)
                await bot.add_roles(member, data.roles[user.rank])

        print('Done!')


async def saving_routine():
    while not bot.is_closed:
        await asyncio.sleep(600)
        db.user_saving()
        db.channel_saving()


def prepare_bot():
    db.get_users()
    db.get_channels()
    print('Users and channels ready')

# Saving data each 10 minutes

# Test bot
bot.run('MTg3MTU3Nzk1MjA2ODU2NzA0.DMpS3A.OcmUlle6LnAcF-i10SbZnRNdfz8')
