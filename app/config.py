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

import os

MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'skale_portal')
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'db')

MYSQL_USER = os.environ['MYSQL_USER']
MYSQL_PASSWORD = os.environ['MYSQL_PASSWORD']

MYSQL_PORT = 3306

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'
SECRET_KEY = os.environ['SECRET_KEY']

DOMAIN_NAME = os.environ['DOMAIN_NAME']
COOKIE_KEY_NAME = f'auth_token_{DOMAIN_NAME}'

TOKEN_EXPIRATION = 3600 * 24 * 30
