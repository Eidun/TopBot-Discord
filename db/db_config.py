import urllib.parse as urlparse
import os

# Deploy the bot with a local DB
config_local = {
    'database': 'Top-Bot',
    'user': 'Tester',
    'password': 'tester123',
    'host': 'localhost',
    'port': 5432
}

# Set which config
config = config_local

if 'DATABASE_URL' in os.environ:
    # Deploy the bot in heroku
    heroku = urlparse.urlparse(os.environ['DATABASE_URL'])
    config_heroku = {
        'database': heroku.path[1:],
        'user': heroku.username,
        'password': heroku.password,
        'host': heroku.hostname,
        'port': heroku.port
        }
    # Set which config
    config = config_heroku

# Your config:
config_new = {
    'database': '',
    'user': '',
    'password': '',
    'host': '',
    'port': ''
}

