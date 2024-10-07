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

# This is a script to manage API keys to the portal-server.
# Usage:
# docker exec -it flask python manage_api_keys.py add "API_KEY_NAME_TO_ADD"
# docker exec -it flask python manage_api_keys.py remove "API_KEY_NAME_TO_REMOVE"
# docker exec -it flask python manage_api_keys.py list

import sys
from app.models import APIKey, initialize_db
from app.utils.database import db


def add_api_key(name):
    with db.atomic():
        instance, key = APIKey.create_key(name)
        print(f'Added new API key for {name}: {key}')
        print("Please store this key securely. It won't be displayed again.")


def remove_api_key(name):
    with db.atomic():
        query = APIKey.delete().where(APIKey.name == name)
        deleted = query.execute()
        if deleted:
            print(f"Removed API key for '{name}'")
        else:
            print(f"API key with name '{name}' not found")


def list_api_keys():
    keys = APIKey.select()
    for key in keys:
        print(f"Name: {key.name}, Created: {key.created_at}, Last Used: {key.last_used or 'Never'}")


if __name__ == '__main__':
    initialize_db()

    if len(sys.argv) < 2:
        print('Usage: python manage_api_keys.py [add|remove|list] [name|key]')
        sys.exit(1)

    action = sys.argv[1]

    if action == 'add' and len(sys.argv) == 3:
        add_api_key(sys.argv[2])
    elif action == 'remove' and len(sys.argv) == 3:
        remove_api_key(sys.argv[2])
    elif action == 'list':
        list_api_keys()
    else:
        print("Invalid command. Use 'add', 'remove', or 'list'.")
