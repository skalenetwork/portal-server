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
import secrets
from flask import Blueprint, request, jsonify, make_response
from siwe import SiweMessage, ExpiredMessage
from peewee import IntegrityError

from app.models import Account
from app.config import DOMAIN_NAME, COOKIE_KEY_NAME
from app.utils import clear_auth_cookies, is_valid_email

auth_bp = Blueprint('auth', __name__)
logger = logging.getLogger('portal:auth')


@auth_bp.route('/nonce', methods=['GET'])
def get_nonce():
    return jsonify({'nonce': secrets.token_hex(32)})


@auth_bp.route('/signin', methods=['POST'])
def sign_in():
    logger.info('sign_in called')
    try:
        message = request.json['message']
        signature = request.json['signature']

        logger.info('message')
        logger.info(message)

        siwe_message = SiweMessage(
            **message, issued_at=message['issuedAt'], chain_id=message['chainId']
        )

        try:
            siwe_message.verify(signature)
        except ExpiredMessage:
            return jsonify({'error': 'Message has expired'}), 400
        except Exception as e:
            return jsonify({'error': f'Verification failed: {str(e)}'}), 400

        account, created = Account.get_or_create(address=siwe_message.address)
        account.sign_in_token = secrets.token_hex(32)
        account.save()

        response = jsonify({'success': True})
        response.set_cookie(
            COOKIE_KEY_NAME,
            account.sign_in_token,
            httponly=True,
            secure=True,
            samesite='None',
            domain=DOMAIN_NAME,
        )
        return response
    except Exception as e:
        logger.error(f'Unexpected error: {str(e)}')
        logger.exception(e)
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 400


@auth_bp.route('/signout', methods=['POST'])
def sign_out():
    logger.info('sign_out called')
    try:
        auth_token = request.cookies.get(COOKIE_KEY_NAME)

        if auth_token:
            account = Account.get_or_none(Account.sign_in_token == auth_token)

            if account:
                account.sign_in_token = None
                account.save()

        response = make_response(jsonify({'success': True}))
        return clear_auth_cookies(response), 200
    except Exception as e:
        logger.error(f'Error during sign out: {str(e)}')
        return jsonify({'error': 'An error occurred during sign out'}), 500


@auth_bp.route('/status', methods=['GET'])
def auth_status():
    auth_token = request.cookies.get(COOKIE_KEY_NAME)
    if auth_token:
        account = Account.get_or_none(Account.sign_in_token == auth_token)
        if account:
            return jsonify({'isSignedIn': True, 'address': account.address})
    return jsonify({'isSignedIn': False, 'address': None})


@auth_bp.route('/email', methods=['GET'])
def get_email():
    auth_token = request.cookies.get(COOKIE_KEY_NAME)
    if not auth_token:
        return jsonify({'error': 'Not authenticated'}), 401

    account = Account.get_or_none(Account.sign_in_token == auth_token)
    if not account:
        return jsonify({'error': 'Invalid authentication'}), 401

    if account.email:
        return jsonify({'email': account.email}), 200
    else:
        return jsonify({'message': 'Email not set'}), 204


@auth_bp.route('/update_email', methods=['POST'])
def update_email():
    auth_token = request.cookies.get(COOKIE_KEY_NAME)
    if not auth_token:
        return jsonify({'error': 'Not authenticated'}), 401

    account = Account.get_or_none(Account.sign_in_token == auth_token)
    if not account:
        return jsonify({'error': 'Invalid authentication'}), 401

    email = request.json.get('email')
    if not email:
        return jsonify({'error': 'Email is required'}), 400

    if not is_valid_email(email):
        return jsonify({'error': 'Invalid email format'}), 400

    try:
        account.email = email
        account.save()
        return jsonify({'success': True, 'message': 'Email updated successfully'}), 200
    except IntegrityError:
        return jsonify({'error': 'Email already in use'}), 400
    except Exception as e:
        logger.error(f'Error updating email: {str(e)}')
        return jsonify({'error': 'An unexpected error occurred'}), 500
