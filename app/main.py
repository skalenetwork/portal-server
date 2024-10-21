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

from flask import Flask
from flask_cors import CORS
from app.routes.auth_routes import auth_bp
from app.routes.like_routes import like_bp
from app.routes.profile_status_routes import profile_status_bp
from app.models import initialize_db
from app.config import SECRET_KEY, DEBUG
from app.utils.logs import init_default_logger
from app.utils.database import db

init_default_logger()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['DEBUG'] = DEBUG

    CORS(app, supports_credentials=True)

    initialize_db()

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(like_bp, url_prefix='/api/apps')
    app.register_blueprint(profile_status_bp, url_prefix='/api/profile')

    @app.before_request
    def _db_connect():
        if db.is_closed():
            db.connect()

    @app.teardown_request
    def _db_close(exc):
        if not db.is_closed():
            db.close()

    return app
