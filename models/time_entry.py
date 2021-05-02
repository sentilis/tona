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
from models.base import BaseModel, db
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


def create_time_entry(name: str, start: str, stop: str, res_model: str = None, res_id: str = None):
    raise NotImplementedError

def start_time_entry(name: str, start: str, res_model: str = None, res_id: str = None):
    if active_time_entry() is not None:
        raise Exception("You have an active time entry")
    data = {"name": name, 'start': format_datetime(start, obj=True) }
    if res_model and res_id:
        res_id = int(res_id)
        data.update({"res_model": res_model, "res_id": res_id})
    id = TimeEntry.create(**data)
    return id.to_dict()

def stop_time_entry(id: int, stop: str):
    if id == 0:
        row = active_time_entry()
        if row is None:
            raise Exception("Haven't an active time entry")
        id = row.id
    else:
        row = TimeEntry.check(id)[0]
    stoptmp = format_datetime(stop, obj=True)
    duration = (stoptmp - row.start).total_seconds()
    data = {TimeEntry.stop: stoptmp, TimeEntry.duration: duration}
    TimeEntry.update(data).where(TimeEntry.id == id).execute()
    return TimeEntry.check(id)[0].to_dict()

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

def fetch(condition=""):
    sql = f"""
        select * from (select
            t.id,
            ( p.name || ' / '|| pt.name) as name,
            t.start, t.stop , t.duration
        from time_entry t
        inner join project_task pt on t.res_id = pt.id
        inner join project p on pt.project_id = p.id
        where t.active = TRUE and t.res_model != '' and t.res_id != 0 and t.res_model = 'project_task'

        union

        select
            t.id,
            t.name,
            t.start, t.stop , t.duration
        from time_entry t
        where t.res_model is null and t.res_id is null and t.active = TRUE) T1 {condition} ; 
    """
    rows = []
    cursor = db.execute_sql(sql)
    for row in cursor.fetchall():
        rows.append(row)
    return rows