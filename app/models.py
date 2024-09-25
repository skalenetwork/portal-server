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

from peewee import Model, CharField, IntegerField, ForeignKeyField
from app.utils.database import db


class Account(Model):
    address = CharField(unique=True)
    sign_in_token = CharField(null=True)

    class Meta:
        database = db


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


def initialize_db():
    db.connect()
    db.create_tables([Account, App, LikedApp])
