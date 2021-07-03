#!/usr/bin/env python3
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# import stuff
from model import db

from utils import register_all_error_handlers

# import views
from views import AuthmeView, BackupsView, PlayerdataView, StatusView, MaprenderView

from config import Config


if Config.SENTRY_DSN:
    sentry_sdk.init(
        dsn=Config.SENTRY_DSN,
        integrations=[FlaskIntegration()],
        send_default_pii=True
    )

# create flask app
app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1)
app.config.from_object(Config)

# initialize stuff
db.init_app(app)

# register error handlers
register_all_error_handlers(app)

# register views
for view in [AuthmeView, BackupsView, PlayerdataView, StatusView, MaprenderView]:
    view.register(app, trailing_slash=False)

# start debugging if needed
if __name__ == "__main__":
    app.run(debug=True)
