#!/usr/bin/env python3
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, validates_schema, ValidationError
from marshmallow.validate import Length, Regexp, Email
from model import Authme


class AuthmeSchema(ModelSchema):
    username = fields.Str(required=True, validate=[Length(min=3, max=16), Regexp("^[a-z0-9_]*$")])
    realname = fields.Str(required=True, validate=[Length(min=3, max=16), Regexp("^[A-Za-z0-9_]*$")])

    email = fields.Str(validate=Email())

    @validates_schema(skip_on_field_errors=True)
    def validate_name(self, data):
        if data['username'] != data['realname'].lower():
            raise ValidationError(
                'Username should be a lowercase version of real name', 'username'
            )

    class Meta:
        model = Authme
        dump_only = [
            'ip',
            'lastlogin',
            'x',
            'y',
            'z',
            'world',
            'yaw',
            'pitch'
        ]
