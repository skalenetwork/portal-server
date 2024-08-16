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

from flask import Blueprint, request, jsonify
from app.models import Account, App, LikedApp

like_bp = Blueprint("like", __name__)


@like_bp.route("/like", methods=["POST"])
def like_app():
    auth_token = request.cookies.get("auth_token")
    if not auth_token:
        return jsonify({"error": "Not authenticated"}), 401

    account = Account.get_or_none(Account.sign_in_token == auth_token)
    if not account:
        return jsonify({"error": "Invalid authentication"}), 401

    app_id = request.json["app_id"]
    app, created = App.get_or_create(app_id=app_id)

    liked_app, created = LikedApp.get_or_create(account=account, app=app)
    if created:
        app.like_count += 1
        app.save()

    return jsonify({"success": True, "like_count": app.like_count})


@like_bp.route("/unlike", methods=["POST"])
def unlike_app():
    auth_token = request.cookies.get("auth_token")
    if not auth_token:
        return jsonify({"error": "Not authenticated"}), 401

    account = Account.get_or_none(Account.sign_in_token == auth_token)
    if not account:
        return jsonify({"error": "Invalid authentication"}), 401

    app_id = request.json["app_id"]
    app = App.get_or_none(App.app_id == app_id)
    if app:
        deleted = (
            LikedApp.delete()
            .where(LikedApp.account == account, LikedApp.app == app)
            .execute()
        )
        if deleted:
            app.like_count = max(0, app.like_count - 1)
            app.save()

    return jsonify({"success": True, "like_count": app.like_count if app else 0})


@like_bp.route("/liked", methods=["GET"])
def get_liked_apps():
    auth_token = request.cookies.get("auth_token")
    if not auth_token:
        return jsonify({"error": "Not authenticated"}), 401

    account = Account.get_or_none(Account.sign_in_token == auth_token)
    if not account:
        return jsonify({"error": "Invalid authentication"}), 401

    liked_apps = [liked_app.app.app_id for liked_app in account.liked_apps]
    return jsonify({"liked_apps": liked_apps})


@like_bp.route("/all", methods=["GET"])
def get_all_app_likes():
    apps = App.select()
    likes_dict = {app.app_id: app.like_count for app in apps}
    return jsonify(likes_dict)
