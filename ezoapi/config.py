import os
from urllib.parse import urlparse


class Config:
    # API Access Keys
    LOCAL_BASIC_API_KEY = os.environ['LOCAL_BASIC_API_KEY']
    LOCAL_PRIV_API_KEY = os.environ['LOCAL_PRIV_API_KEY']

    # Stuff used by EZOAPI
    # This is the same MySQL db that minecraft connects to
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI', "sqlite://")
    BACKUPS_FOLDER = os.environ['BACKUPS_FOLDER']
    RCON_HOST = os.environ['RCON_HOST']
    RCON_PASSWORD = os.environ['RCON_PASSWORD']
    QUERY_ADDRESS = os.environ['QUERY_ADDRESS']
    MAPRENDER_STATUS_URL = urlparse(os.environ['MAPRENDER_STATUS_URL'])

    # Important stuff
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(12))

    # Other stuff
    # disable this for better performance
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Sentry
    SENTRY_DSN = os.environ.get("SENTRY_DSN")
