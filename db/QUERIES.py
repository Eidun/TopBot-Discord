# Creation queries
CREATE_USERS_TABLE ='CREATE TABLE USERS (' \
                   'id bigint PRIMARY KEY,' \
                   ' name text, join_date date,' \
                   ' last_message_date date,' \
                   ' messages int, rank text,' \
                   ' active int);'
CREATE_CHANNELS_TABLE = 'CREATE TABLE CHANNELS (id bigint PRIMARY KEY, name text, bot boolean);'

# Get values queries
GET_USER_BY_ID = "SELECT * FROM users WHERE id=%s"
GET_CHANNEL_BY_ID = "SELECT * FROM channels WHERE id=%s"
GET_USERS = "SELECT * FROM users"
GET_CHANNELS = "SELECT * FROM channels"

# Insert values queries
INSERT_USER = "INSERT INTO users" \
              "(id, name, join_date, last_message_date, messages, rank, active)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s);"
INSERT_CHANNEL = "INSERT INTO channels (id, name, bot) VALUES (%s, %s, %s)"

# Update queries
UPDATE_USER = "UPDATE users SET name=%s, join_date=%s, last_message_date=%s, messages=%s, rank=%s, active=%s WHERE id=%s"

# Drop queries
DROP_USERS = "DROP TABLE IF EXISTS users;"
DROP_CHANNELS = "DROP TABLE IF EXISTS channels;"
