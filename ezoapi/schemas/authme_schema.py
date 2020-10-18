#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from model import Authme


class AuthmeSchema(ModelSchema):
    class Meta:
        model = Authme
