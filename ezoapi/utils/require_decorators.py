#!/usr/bin/env python3
from flask import request, current_app, abort

from functools import wraps


def apikey_required(priv: bool = False):
    def apikey_required_factory(f):

        @wraps(f)
        def call(*args, **kwargs):

            apikey_recieved = request.headers.get('Authorization', None)

            apikeys_accepted = [current_app.config['LOCAL_PRIV_API_KEY']]  # Always accept Privileged key
            if not priv:
                # Accept BASIC key only on non-privileged-only endpoints
                apikeys_accepted.append(current_app.config['LOCAL_BASIC_API_KEY'])

            if apikey_recieved in apikeys_accepted:
                return f(*args, **kwargs)
            else:
                abort(401, "Unauthorized")

        return call

    return apikey_required_factory


def json_required(f):
    @wraps(f)
    def call(*args, **kwargs):

        if request.is_json:
            return f(*args, **kwargs)
        else:
            abort(400, "JSON required")

    return call
