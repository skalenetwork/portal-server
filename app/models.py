#   -*- coding: utf-8 -*-
#
#   This file is part of SKALE portal-server
#
#   Copyright (C) 2024 SKALE Labs
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

import secrets
import hashlib
from datetime import datetime
from peewee import Model, CharField, IntegerField, ForeignKeyField, DateTimeField
from app.utils.database import db


class Account(Model):
    address = CharField(unique=True)
    sign_in_token = CharField(null=True)
    email = CharField(unique=True, null=True)

    class Meta:
        database = db

    @property
    def profile_completed(self):
        return self.email is not None


class App(Model):
    app_id = CharField(unique=True)
    like_count = IntegerField(default=0)

    class Meta:
        database = db


class LikedApp(Model):
    account = ForeignKeyField(Account, backref='liked_apps')
    app = ForeignKeyField(App, backref='likes')

    class Meta:
        database = db
        indexes = ((('account', 'app'), True),)


class APIKey(Model):
    key_hash = CharField(unique=True)
    name = CharField()
    created_at = DateTimeField(default=datetime.now)
    last_used = DateTimeField(null=True)

    class Meta:
        database = db

    @classmethod
    def create_key(cls, name):
        key = secrets.token_urlsafe(32)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        instance = cls.create(key_hash=key_hash, name=name)
        return instance, key

    @classmethod
    def validate_key(cls, key):
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        instance = cls.get_or_none(cls.key_hash == key_hash)
        if instance:
            instance.last_used = datetime.now()
            instance.save()
        return instance is not None


def initialize_db():
    db.connect()
    db.create_tables([Account, App, LikedApp, APIKey])
