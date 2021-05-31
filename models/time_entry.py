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
from tona.models.base import BaseModel, db
from tona.models.project_task import ProjectTask
from tona.models.habit import Habit
from tona.models.objective_keyresult import ObjectiveKeyResult
from tona.utils import format_datetime, FORMAT_DATE

class TimeEntry(BaseModel):

    class Meta:
        table_name = 'time_entry'

    name = peewee.CharField(null=True)
    start = peewee.DateTimeField()  # Datetime must be in ISO-8601 format (eg. "2019-04-16T05:15:32.998Z") UTC
    stop = peewee.DateTimeField(null=True)  # Datetime must be in ISO-8601 format (eg. "2019-04-16T05:15:32.998Z") UTC
    duration = peewee.FloatField(default=0)  # time entry duration in seconds.

    res_model = peewee.CharField(null=True)  # Model name
    res_id = peewee.IntegerField(null=True)  # Model record id

    @classmethod
    def apply_filter(cls, time_entries, start_date=None, end_date=None):

        if start_date and end_date is None:
            start_date = format_datetime(start_date, fmt_in=FORMAT_DATE, obj=True).date()
            time_entries = time_entries.where(
                (TimeEntry.start.year >= start_date.year) &
                (TimeEntry.start.month >= start_date.month) &
                (TimeEntry.start.day >= start_date.day)
            )
        elif start_date is None and end_date:
            end_date = format_datetime(end_date, fmt_in=FORMAT_DATE, obj=True).date()
            time_entries = time_entries.where(
                (TimeEntry.stop.year <= end_date.year) &
                (TimeEntry.stop.month <= end_date.month) &
                (TimeEntry.stop.day <= end_date.day)
            )
        elif start_date and end_date:
            start_date = format_datetime(start_date, fmt_in=FORMAT_DATE, obj=True).date()
            end_date = format_datetime(end_date, fmt_in=FORMAT_DATE, obj=True).date()
            time_entries = time_entries.where(
                (TimeEntry.start.year >= start_date.year) &
                (TimeEntry.start.month >= start_date.month) &
                (TimeEntry.start.day >= start_date.day),
                (TimeEntry.stop.year <= end_date.year) &
                (TimeEntry.stop.month <= end_date.month) &
                (TimeEntry.stop.day <= end_date.day)
            )

        return time_entries

    @classmethod
    def get_by_project(cls, id, start_date, end_date):

        time_entries = TimeEntry.select(
            TimeEntry.id,
            TimeEntry.start,
            TimeEntry.stop,
            TimeEntry.duration,
            ProjectTask.name,
            ProjectTask.project_id
        ).join(ProjectTask, on = (TimeEntry.res_id == ProjectTask.id)).where(
            TimeEntry.stop != None,
            TimeEntry.res_model == 'project_task')

        time_entries = cls.apply_filter(time_entries, start_date, end_date)
        if id:
            time_entries = time_entries.where(ProjectTask.project_id == id)
        return time_entries

    @classmethod
    def get_by_habit(cls, id, start_date, end_date):

        time_entries = TimeEntry.select(
            TimeEntry.id,
            TimeEntry.start,
            TimeEntry.stop,
            TimeEntry.duration,
            Habit.name,
            Habit.id,
        ).join(Habit, on = (TimeEntry.res_id == Habit.id)).where(
            TimeEntry.stop != None,
            TimeEntry.res_model == 'habit')

        time_entries = cls.apply_filter(time_entries, start_date, end_date)
        if id:
            time_entries = time_entries.where(Habit.id == id)
        return time_entries

    @classmethod
    def get_by_objective(cls, id, start_date, end_date):

        time_entries = TimeEntry.select(
            TimeEntry.id,
            TimeEntry.start,
            TimeEntry.stop,
            TimeEntry.duration,
            ObjectiveKeyResult.name,
            ObjectiveKeyResult.id,
            ObjectiveKeyResult.objective_id
        ).join(ObjectiveKeyResult, on = (TimeEntry.res_id == ObjectiveKeyResult.id)).where(
            TimeEntry.stop != None,
            TimeEntry.res_model == 'objective_keyresult')
        time_entries = cls.apply_filter(time_entries, start_date, end_date)
        if id:
            time_entries = time_entries.where(ObjectiveKeyResult.objective_id == id)
        return time_entries

    @classmethod
    def get_by_other(cls, id, start_date, end_date):
        time_entries = TimeEntry.select(
            TimeEntry.id,
            TimeEntry.start,
            TimeEntry.stop,
            TimeEntry.duration,
            TimeEntry.name,
        ).where(
            TimeEntry.stop != None,
            TimeEntry.res_model == None, 
            TimeEntry.res_id == None)
        time_entries = cls.apply_filter(time_entries, start_date, end_date)
        return time_entries

    @classmethod
    def running(cls):
        try:
            row = TimeEntry.select().where(
                TimeEntry.active == True,
                TimeEntry.start != None,
                TimeEntry.stop == None).order_by(TimeEntry.start.desc()).limit(1).get()
            return row
        except Exception as e:
            pass
        return None

def start_time_entry(name: str, start: str, res_model: str = None, res_id: str = None):
    if TimeEntry.running() is not None:
        raise Exception("You have an active time entry")
    data = {"name": name, 'start': format_datetime(start, obj=True) }
    if res_model and res_id:
        res_id = int(res_id)
        data.update({"res_model": res_model, "res_id": res_id})
    id = TimeEntry.create(**data)
    return id.to_dict()

def stop_time_entry(id: int, stop: str):
    if id == 0:
        row = TimeEntry.running()
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

def fetch(condition=""):
    sql = f"""
        select * from (

        select
            t.id,
            ( 'Habit' || ' / '|| h.name) as name,
            t.start, t.stop , t.duration
        from time_entry t
        inner join habit h on t.res_id = h.id
        where t.active = TRUE and t.res_model != '' and t.res_id != 0 and t.res_model = 'habit'

        union

        select
            t.id,
            ( 'Objective / ' || o.name || ' / '|| ok.name) as name,
            t.start, t.stop , t.duration
        from time_entry t
        inner join objective_keyresult ok on t.res_id = ok.id
        inner join objective o on ok.objective_id = o.id
        where t.active = TRUE and t.res_model != '' and t.res_id != 0 and t.res_model = 'objective_keyresult'

        union

        select
            t.id,
            ( 'Project / ' || p.name || ' / '|| pt.name) as name,
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
        where t.res_model is null and t.res_id is null and t.active = TRUE) T1 {condition}
    """
    rows = []
    cursor = db.execute_sql(sql)
    for row in cursor.fetchall():
        rows.append(row)
    return rows
