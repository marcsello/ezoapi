#!/usr/bin/env python3
import glob
import os
import os.path

from flask import abort, jsonify, current_app
from flask_classful import FlaskView, route

from utils import apikey_required


class BackupsView(FlaskView):
    decorators = [apikey_required(False)]

    def index(self):
        list_of_files = glob.glob(os.path.join(current_app.config["BACKUPS_FOLDER"], "*.tar.gz"))
        return jsonify([os.path.basename(fname) for fname in list_of_files])  # empty lists handled by python properly

    @route("$latest")
    def get_latest(self):
        list_of_files = glob.glob(os.path.join(current_app.config["BACKUPS_FOLDER"], "*.tar.gz"))

        if not list_of_files:
            abort(404, "Backups folder empty")

        latest_file = max(list_of_files, key=os.path.getctime)
        return jsonify(os.path.basename(latest_file))
