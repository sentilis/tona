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
import peewee
from models.base import BaseModel
from utils import format_datetime

class TimeEntry(BaseModel):

    class Meta:
        table_name = 'time_entry'

    name = peewee.CharField()
    start = peewee.DateTimeField()  # Datetime must be in ISO-8601 format (eg. "2019-04-16T05:15:32.998Z") UTC
    stop = peewee.DateTimeField(null=True)  # Datetime must be in ISO-8601 format (eg. "2019-04-16T05:15:32.998Z") UTC
    duration = peewee.FloatField(default=0)  # time entry duration in seconds.

    res_model = peewee.CharField(null=True)  # Model name
    res_id = peewee.IntegerField(null=True)  # Model record id


def create_time_entry(name: str, start: str, stop: str, res_model: str = None, res_id: int = None):
    raise NotImplementedError

def start_time_entry(name: str, start: str, res_model: str = None, res_id: int = None):
    data = {"name": name, 'start': format_datetime(start) }
    id = TimeEntry.create(**data)
    data.update({"id": id.id, 'start': start})
    return data

def stop_time_entry(id: int, stop: str):
    row = TimeEntry.check(id)[0]
    stoptmp = format_datetime(stop)
    duration = (stoptmp - row.start).total_seconds()
    data = {TimeEntry.stop: stoptmp, TimeEntry.duration: duration}
    TimeEntry.update(data).where(TimeEntry.id == id).execute()
    return {
        "id": row.id,
        "start": format_datetime(obj2str=row.start),
        "stop": stop,
        "name": row.name
    }

def active_time_entry():
    try:
        row = TimeEntry.select().where(TimeEntry.active == True,
                                    TimeEntry.start != None,
                                    TimeEntry.stop == None).order_by(TimeEntry.start.desc()).limit(1).get()
        return row
    except Exception as e:
        pass
    return None

def format_duration(seconds: float, format: str = "clock"):

    minutes = int(seconds / 60)
    hours  = int(minutes / 60)
    seconds = int(seconds - minutes * 60)
    minutes = int(minutes - hours * 60)

    def pad(v):
        v = str(v)
        if len(v) == 1:
            return '0' + v
        return v
    d = pad(hours) + ":" + pad(minutes) + ":" + pad(seconds)
    if format == 'human':
        d = pad(hours) + "H" + pad(minutes) + "M" + pad(seconds) + "S"
    return d