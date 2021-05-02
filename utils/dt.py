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
FORMAT_DATE = '%Y-%m-%d'
FORMAT_TIME = '%H:%M:%S'
FORMAT_DATETIME = FORMAT_DATE + ' ' + FORMAT_TIME

def format_datetime(dt, fmt_in=FORMAT_DATETIME_ISO8601,
                        fmt_out=FORMAT_DATETIME_ISO8601, obj=False):
    if isinstance(dt, datetime):
        pass
    elif isinstance(dt, str):
        dt = datetime.strptime(dt, fmt_in)
    if obj:
        return dt
    return dt.strftime(fmt_out)

def convert_datetime(dt, tz_in=pytz.utc, tz_out=pytz.utc,
                        fmt_in=FORMAT_DATETIME_ISO8601,
                        fmt_out=FORMAT_DATETIME_ISO8601, obj=False):

    if isinstance(dt, datetime):
        pass
    elif isinstance(dt, str):
        if dt != "":
            dt = datetime.strptime(dt, fmt_in)
        else:
            raise Exception("Args: dt is empty")
    if tz_in != pytz.utc:
        tz_in = pytz.timezone(tz_in)
    if tz_out != pytz.utc:
        tz_out = pytz.timezone(tz_out)

    dt = dt.replace(tzinfo=tz_in)
    dt = dt.astimezone(tz_out)
    if obj:
        return dt
    return dt.strftime(fmt_out)