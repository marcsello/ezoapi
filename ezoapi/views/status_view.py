#!/usr/bin/env python3
from flask import jsonify, current_app, abort
from flask_classful import FlaskView
from mcstatus import MinecraftServer

from utils import apikey_required


class StatusView(FlaskView):
    decorators = [apikey_required(False)]

    def index(self):

        try:
            server = MinecraftServer.lookup(current_app.config["QUERY_ADDRESS"])
            status = server.query()

            resp = {
                "online": True,
                "players": {
                    "online": status.players.online,
                    "max": status.players.max,
                    "names": status.players.names
                },
                "software": {
                    "version": status.software.version,
                    "brand": status.software.brand
                }
            }

        except:
            resp = {
                "online": False
            }

        return jsonify(resp)
