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

import re
from app.config import COOKIE_KEY_NAME, DOMAIN_NAME


def clear_auth_cookies(response):
    response.set_cookie(COOKIE_KEY_NAME, '', expires=0, httponly=True, secure=True, samesite='None')
    response.set_cookie(
        COOKIE_KEY_NAME,
        '',
        expires=0,
        httponly=True,
        secure=True,
        samesite='None',
        domain=DOMAIN_NAME,
    )
    return response


def is_valid_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None
