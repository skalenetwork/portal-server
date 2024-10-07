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
from flask import Blueprint, jsonify
from app.models import Account
from app.auth import token_required

profile_status_bp = Blueprint('profile_status', __name__)
logger = logging.getLogger(__name__)


@profile_status_bp.route('/profile-status/<wallet_address>', methods=['GET'])
@token_required
def get_profile_status(wallet_address):
    try:
        account = Account.get_or_none(Account.address == wallet_address)
        if account:
            return jsonify({'exists': True, 'profile': account.profile_completed})
        else:
            return jsonify({'exists': False, 'profile': False})
    except Exception as e:
        logger.exception(f'Error in get_profile_status: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500
