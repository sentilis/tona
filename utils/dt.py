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
from datetime import datetime
import pytz

FORMAT_DATETIME_ISO8601 = '%Y-%m-%dT%H:%M:%S.%fZ'
FORMAT_DATETIME = '%Y-%m-%dT%H:%M:%S'

def format_datetime(str2obj: str = None, obj2str: datetime = None, fmt=FORMAT_DATETIME_ISO8601):
    dt = datetime.utcnow().strftime(fmt)
    if str2obj:
        dt = datetime.strptime(str2obj, fmt)
    elif obj2str:
        dt = obj2str.strftime(fmt)
    return dt

def convert_datetime_tz(str2obj: str = None, obj2str: datetime = None, fmt=FORMAT_DATETIME, tz=""):
    dt = datetime.utcnow().strftime(fmt)
    if obj2str:
        obj2str = obj2str.replace(tzinfo=pytz.utc)
        dt = obj2str.astimezone(pytz.timezone('Mexico/General')).strftime(fmt)
    return dt