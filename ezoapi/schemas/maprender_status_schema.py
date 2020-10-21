#!/usr/bin/env python3
from marshmallow import Schema, fields, RAISE


class MaprenderStatusSchema(Schema):
    rendering = fields.Bool(required=True)

    class Meta:
        unknown = RAISE
