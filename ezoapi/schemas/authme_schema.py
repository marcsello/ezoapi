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
    def validate_name(self, data, **kwargs):
        # Szóval itt most trükközünk
        # Partial validationnál nem tudhatjuk mindkettő értéket (vagy egyet vagy egyiket se kapjuk)
        # Az alábbi kondíció az pedig nem dob validációs hibát, ha mindkettő hiányzik
        # Illetve akkor se, ha mindkettő meg van adva (de jól)
        # Viszont ha csak az egyik, akkor be fog szólni
        if data.get('username', '') != data.get('realname', '').lower():
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
