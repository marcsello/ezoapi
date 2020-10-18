#!/usr/bin/env python3#!/usr/bin/env python3
from .db import db


class Authme(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    username = db.Column(db.String(255), nullable=False, unique=True)
    realname = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    salt = db.Column(db.String(50), nullable=True, default=None)
    ip = db.Column(db.String(40), nullable=False, default='127.0.0.1')
    lastlogin = db.Column(db.BigInteger, nullable=False, default=1451769207059)

    x = db.Column(db.Float, nullable=False, default=0)
    y = db.Column(db.Float, nullable=False, default=0)
    z = db.Column(db.Float, nullable=False, default=0)
    world = db.Column(db.String(255), nullable=False, default='world')

    email = db.Column(db.String(255), nullable=True, default=None)
    isLogged = db.Column(db.SmallInteger, nullable=False, default=0)
    hasSession = db.Column(db.SmallInteger, nullable=False, default=0)

    yaw = db.Column(db.Float, nullable=True, default=None)
    pitch = db.Column(db.Float, nullable=True, default=None)

    regdate = db.Column(db.BigInteger, nullable=False, default=0)
    regip = db.Column(db.String(40), nullable=True, default=None)

    totp = db.Column(db.String(32), nullable=True, default=None)
