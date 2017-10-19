import data
import discord
from models.active_user import UserModel


def register_message(message: discord.Message):
    member = message.author
    if member.bot:
        # Bots are not registered
        return
    if member.id in data.users:
        data.users[member.id].last_message_date = message.timestamp
        data.users[member.id].messages += 1
        data.users[member.id].update = True
    else:
        last_message_date = message.timestamp
        new_user = UserModel(member.id, member.display_name, member.joined_at,
                             last_message_date, messages=1, active=0, update=True)
        data.users[new_user.user_id] = new_user
