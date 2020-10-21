#!/usr/bin/env python3
import requests

from marshmallow import ValidationError

from flask import abort, jsonify, current_app
from flask_classful import FlaskView

from utils import apikey_required

from schemas import MaprenderStatusSchema


class MaprenderView(FlaskView):
    decorators = [apikey_required(False)]

    maprender_status_schema = MaprenderStatusSchema(many=False)

    def index(self):
        source_url = current_app.config['MAPRENDER_STATUS_URL']  # Will contain a ParseResult

        maprender_status = None
        try:

            if source_url.scheme == 'file':
                with open(source_url.path, 'r') as f:
                    maprender_status = self.maprender_status_schema.loads(f.read())

            elif source_url.scheme in ['http', 'https']:
                r = requests.get(source_url.geturl(), timeout=5)
                r.raise_for_status()
                maprender_status = self.maprender_status_schema.load(r.json())

        except (ValidationError, FileNotFoundError, PermissionError, requests.Timeout, requests.HTTPError) as e:
            abort(500, f"Could not fetch status: {e}")

        if not maprender_status:
            abort(500, f"Could not fetch status: Unsupported Schema")

        return jsonify(maprender_status)
