#!/usr/bin/env python3
import os

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# import stuff
from model import db

from utils import register_all_error_handlers

# import views
from views import AuthmeView, BackupsView, PlayerdataView, StatusView

SENTRY_DSN = os.environ.get("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[FlaskIntegration()],
        send_default_pii=True
    )

# create flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
# configure flask app
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI', "sqlite://")  # Default to memory db
app.config['LOCAL_BASIC_API_KEY'] = os.environ['LOCAL_BASIC_API_KEY']
app.config['LOCAL_PRIV_API_KEY'] = os.environ['LOCAL_PRIV_API_KEY']
app.config['BACKUPS_FOLDER'] = os.environ['BACKUPS_FOLDER']
app.config['RCON_HOST'] = os.environ['RCON_HOST']
app.config['RCON_PASSWORD'] = os.environ['RCON_PASSWORD']
app.config['QUERY_ADDRESS'] = os.environ['QUERY_ADDRESS']

# important stuff
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(12))
# disable this for better performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize stuff
db.init_app(app)

# register error handlers
register_all_error_handlers(app)

# register views
for view in [AuthmeView, BackupsView, PlayerdataView, StatusView]:
    view.register(app, trailing_slash=False)

# start debuggig if needed
if __name__ == "__main__":
    app.run(debug=True)
