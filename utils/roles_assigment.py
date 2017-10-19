import data
import datetime
import discord


def check_activity_today():
    today = datetime.datetime.today().day
    for user in data.users.values():
        if today == user.last_message_date.day:
            user.add_activity()
        else:
            user.sub_activity()

        print(data.members)
        for member in data.members:
            print(member.display_name)
        member = discord.utils.get(data.members, display_name=user.name)
        print(data.roles)
        member.add_role(data.roles[user.rank])


def has_role_id(id):

    def predicate(ctx):
        msg = ctx.message
        ch = msg.channel
        if ch.is_private:
            return False

        role = discord.utils.get(msg.author.roles, id=id)
        return role is not None

    return check(predicate)
