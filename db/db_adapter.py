import psycopg2
import db.QUERIES as queries
import data
import datetime
from models.active_user import UserModel
from models.active_channels import ChannelsModel
import data
from db.db_config import config


def create_connection():
    conn = psycopg2.connect(
        database=config['database'],
        user=config['user'],
        password=config['password'],
        host=config['host'],
        port=config['port']
    )
    return conn


def initialize():
    initialize_users()
    initialize_channels()


def initialize_users():
    # Connection to database
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(queries.DROP_USERS)
    cursor.execute(queries.CREATE_USERS_TABLE)

    conn.commit()
    cursor.close()
    conn.close()


def initialize_channels():
    # Connection to database
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(queries.DROP_CHANNELS)
    cursor.execute(queries.CREATE_CHANNELS_TABLE)

    conn.commit()
    cursor.close()
    conn.close()


def user_saving():
    conn = create_connection()
    cursor = conn.cursor()
    # Save all users in memory
    users = data.users.values()
    print('Saving users...')
    update_users = list(filter(lambda x: x.update, users))
    print('{} users to update'.format(update_users.__len__()))
    for user in update_users:

        print('Now saving {}'.format(user.name))
        # Get, if exists, the user
        cursor.execute(queries.GET_USER_BY_ID, (user.user_id, ))
        existing_user = cursor.fetchone()
        if existing_user is None:
            # This is a new user
            cursor.execute(queries.INSERT_USER,
                           (user.user_id, user.name, user.join_date,
                            user.last_message_date, user.messages,
                            user.rank, user.activity))
            print('User saved')
        else:
            cursor.execute(queries.UPDATE_USER, (user.name, user.join_date,
                                                 user.last_message_date, user.messages,
                                                 user.rank, user.activity, user.user_id))
            print('User updated')

    conn.commit()
    cursor.close()
    conn.close()


def channel_saving():
    conn = create_connection()
    cursor = conn.cursor()
    for channel in data.text_channels.values():
        # Get, if exists, the channel
        cursor.execute(queries.GET_CHANNEL_BY_ID, (channel.channel_id,))
        existing_channel = cursor.fetchone()
        if existing_channel is None:
            # This is a new channel
            cursor.execute(queries.INSERT_CHANNEL, (channel.channel_id, channel.name, channel.bot))
            print('Channel saved')
    for channel in data.bot_channels.values():
        # Get, if exists, the channel
        cursor.execute(queries.GET_CHANNEL_BY_ID, (channel.channel_id,))
        existing_channel = cursor.fetchone()
        if existing_channel is None:
            # This is a new channel
            cursor.execute(queries.INSERT_CHANNEL, (channel.channel_id, channel.name, channel.bot))
            print('Channel saved')

    conn.commit()
    cursor.close()
    conn.close()


def get_users():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(queries.GET_USERS)
    rows = cursor.fetchall()

    if cursor.rowcount == 0:
        return
    for row in rows:
        join_date = datetime.datetime(row[2].year, row[2].month, row[2].day)
        last_message_date = datetime.datetime(row[3].year, row[3].month, row[3].day)
        user = UserModel(row[0], row[1], join_date, last_message_date, row[4], row[5], row[6], False)
        data.users[str(user.user_id)] = user
    conn.commit()
    cursor.close()
    conn.close()


def get_channels():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute(queries.GET_CHANNELS)
    rows = cursor.fetchall()

    if cursor.rowcount == 0:
        return
    for row in rows:
        channel = ChannelsModel(row[0], row[1], row[2])
        if channel.bot:
            data.bot_channels[str(channel.channel_id)] = channel
        else:
            data.text_channels[str(channel.channel_id)] = channel
    conn.commit()
    cursor.close()
    conn.close()
