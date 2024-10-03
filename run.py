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
from app.main import create_app
from app.utils.db_migrations import add_email_field_to_account
from app.utils.database import db

logger = logging.getLogger('portal:run')


def run_migrations():
    logger.info('Running database migrations...')
    with db:
        add_email_field_to_account()
    logger.info('Database migrations completed.')


run_migrations()
app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
