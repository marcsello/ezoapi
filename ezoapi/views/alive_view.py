#!/usr/bin/env python3
from flask import jsonify
from flask_classful import FlaskView


class AliveView(FlaskView):

    def index(self):
        return jsonify({'alive': True})
