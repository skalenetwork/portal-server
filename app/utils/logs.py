#   -*- coding: utf-8 -*-
#
#   This file is part of portal-server.
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

import sys
import logging
from logging import Formatter, StreamHandler


LOG_FORMAT = '[%(asctime)s %(levelname)s] %(name)s:%(lineno)d - %(threadName)s - %(message)s'


def init_default_logger():
    formatter = Formatter(LOG_FORMAT)
    stream_handler = StreamHandler(sys.stderr)
    stream_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.DEBUG, handlers=[stream_handler])
