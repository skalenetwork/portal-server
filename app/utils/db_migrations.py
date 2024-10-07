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

import logging
from peewee import CharField
from playhouse.migrate import MySQLMigrator, migrate
from app.utils.database import db
from app.models import APIKey

logger = logging.getLogger('portal:db_migrations')


def add_email_field_to_account():
    migrator = MySQLMigrator(db)
    email_field = CharField(null=True, unique=True)
    try:
        with db.connection_context():
            if 'email' not in db.get_columns('account'):
                with db.atomic():
                    migrate(
                        migrator.add_column('account', 'email', email_field),
                    )
                print('Migration completed: Added email field to Account model')
            else:
                print('Email field already exists in Account model')
    except Exception as e:
        print(f'Error during migration: {e}')


def create_api_key_table():
    try:
        with db.connection_context():
            if not APIKey.table_exists():
                db.create_tables([APIKey])
                print('Migration completed: Created APIKey table')
            else:
                print('APIKey table already exists')
    except Exception as e:
        print(f'Error during migration: {e}')


def run_all_migrations():
    add_email_field_to_account()
    create_api_key_table()
