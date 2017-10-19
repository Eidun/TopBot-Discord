import data
from models.active_user import UserModel


def get_join_rank(user: UserModel):
    users = data.users.values()
    # Sort by join date
    users = sorted(users, key=lambda x: x.join_date)
    user_rank = 1
    for current in users:
        if current.user_id == user.user_id:
            return user_rank
        user_rank += 1
    return -1


def get_messages_rank(user: UserModel):
    users = data.users.values()
    # Sort by messages number
    users = sorted(users, key=lambda x: x.messages, reverse=True)
    user_rank = 1
    for current in users:
        if current.user_id == user.user_id:
            return user_rank
        user_rank += 1
    return -1


def get_top20():
    users = data.users.values()
    # Sort by messages number
    users = sorted(users, key=lambda x: x.messages, reverse=True)
    # Get first 20 values
    return users[0:20]
