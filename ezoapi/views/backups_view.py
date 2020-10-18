#!/usr/bin/env python3
import glob
import os

from flask import abort, jsonify, current_app
from flask_classful import FlaskView, route

from utils import apikey_required


class BackupsView(FlaskView):
    decorators = [apikey_required(False)]

    def index(self):
        list_of_files = glob.glob(current_app.config["BACKUPS_FOLDER"])
        return jsonify(list_of_files)

    @route("$latest")
    def get_latest(self):
        list_of_files = glob.glob(current_app.config["BACKUPS_FOLDER"])

        if not list_of_files:
            abort(404)

        latest_file = max(list_of_files, key=os.path.getctime)
        return jsonify(latest_file)
