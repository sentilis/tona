# -*- coding: utf-8 -*-
#    Copyright (C) 2021  The Project TONA Authors
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
import re

def api_response(ok=False, message=None, payload=None):
    return {
        "ok": ok,
        "message": message,
        "payload": payload
    }

def str2int(val: str):
    try:
        val = int("".join([n for n in val if n.isdigit()]))
        return val
    except Exception as e: 
        pass
    return 0

def path_storage():
    pass

def name_constraint(name):
    if not name:
        print("The argument name is required")
        raise SystemExit(1)
    if not isinstance(name, tuple):
        print("The argument name not is tuple")
        raise SystemExit(1)
    return ' '.join(name)


