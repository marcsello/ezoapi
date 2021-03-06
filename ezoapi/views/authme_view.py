#!/usr/bin/env python3
from flask import abort, jsonify, request, current_app
from flask_classful import FlaskView, route
from marshmallow import ValidationError
from mcrcon import MCRcon

from utils import apikey_required

from model import db, Authme
from schemas import AuthmeSchema


class AuthmeView(FlaskView):
    authme_schema = AuthmeSchema(many=False, session=db.session)
    authme_schemas = AuthmeSchema(many=True)

    decorators = [apikey_required(True)]  # This is a privileged view

    def index(self):
        a = Authme.query.all()
        return jsonify(self.authme_schemas.dump(a))

    def get(self, _id: int):
        a = Authme.query.get_or_404(_id)
        return jsonify(self.authme_schema.dump(a))

    def delete(self):  # delete all
        aa = Authme.query.all()

        for a in aa:
            with MCRcon(current_app.config["RCON_HOST"], current_app.config["RCON_PASSWORD"]) as mcr:
                current_app.logger.debug(f"Kicking {a.username}...")
                current_app.logger.debug(
                    "MC RCON: " +
                    mcr.command(f"kick {a.username} Az EZO.TV regisztrációd megszűnt!")
                )

            db.session.delete(a)

        db.session.commit()
        return '', 204

    def patch(self, _id: int):  # update one
        a = Authme.query.get_or_404(_id)

        old_username = a.username
        old_isLogged = a.isLogged

        try:
            a = self.authme_schema.load(request.json, partial=True, instance=a)
        except ValidationError as e:
            abort(400, str(e))

        if a.username != old_username:
            with MCRcon(current_app.config["RCON_HOST"], current_app.config["RCON_PASSWORD"]) as mcr:
                current_app.logger.debug(f"Kicking {old_username}...")
                current_app.logger.debug(
                    "MC RCON: " +
                    mcr.command(
                        f"kick {old_username} A regisztrációdhoz tartozó felhasználónév megváltozott! Lépj be újra kérlek."
                    )
                )
            a.isLogged = 0
            a.hasSession = 0

        if a.isLogged != old_isLogged:
            with MCRcon(current_app.config["RCON_HOST"], current_app.config["RCON_PASSWORD"]) as mcr:
                # Old username will be the same as current if it's not changed
                current_app.logger.debug(f"Logging out {old_username}...")
                current_app.logger.debug(
                    "MC RCON: " +
                    mcr.command(f"kick {old_username} Ki lettél jelentkeztetve! Lépj be újra kérlek.")
                )
            if not a.isLogged:
                a.hasSession = 0

        db.session.add(a)
        db.session.commit()

        return jsonify(self.authme_schema.dump(a))

    def post(self):

        try:
            a = self.authme_schema.load(request.json)
        except ValidationError as e:
            abort(400, str(e))

        db.session.add(a)
        db.session.commit()

        return jsonify(self.authme_schema.dump(a))

    @route("<_id>", methods=["DELETE"])
    def delete_one(self, _id: int):
        a = Authme.query.get_or_404(_id)

        with MCRcon(current_app.config["RCON_HOST"], current_app.config["RCON_PASSWORD"]) as mcr:
            current_app.logger.debug(f"Kicking {a.username}...")
            current_app.logger.debug(
                "MC RCON: " +
                mcr.command(f"kick {a.username} Az EZO.TV regisztrációd megszűnt!")
            )

        db.session.delete(a)
        db.session.commit()
        return '', 204
