# -*- coding: utf-8 -*-
# Part of Sentilis. See LICENSE file for full copyright and licensing details.
import peewee
#from tona.models.base import BaseModel, db
#from tona.models.project_task import ProjectTask
#from tona.models.habit import Habit
#from tona.models.objective_keyresult import ObjectiveKeyResult
#from tona.utils import format_datetime, FORMAT_DATE
from tona.core import Model, PydanticBaseModel, PydanticHTTPResponseModel
from typing import Optional, Any, List
from datetime import datetime

class TimeEntry(Model):

    class Meta:
        table_name = 'time_entry'

    name = peewee.CharField(null=True)
    start = peewee.DateTimeField()
    stop = peewee.DateTimeField(null=True)
    duration = peewee.FloatField(default=0)

    res_model = peewee.CharField(null=True)
    res_id = peewee.IntegerField(null=True)

    class Pydantic(PydanticBaseModel):
        id: Optional[int]
        name: str
        start: datetime
        stop: Optional[datetime]
        duration: Optional[float]

        res_model: Optional[str]
        res_id: Optional[int]

class TimeEntryStart(PydanticBaseModel):
    name: Optional[str] = ""
    start: datetime

class TimeEntryStop(PydanticBaseModel):
    id: Optional[int] = 0
    stop: datetime

class TimeEntryEdit(TimeEntry.Pydantic):
    name: Optional[str]
    start: Optional[datetime]

class TimeEntryDelete(PydanticHTTPResponseModel):
    pass

class TimeEntryItems(PydanticHTTPResponseModel):
    payload: Optional[List[TimeEntry.Pydantic]]

class TimeEntryItem(PydanticHTTPResponseModel):
    payload: Optional[TimeEntry.Pydantic]


class TimeEntryAnlyzeMeta(PydanticBaseModel):
    slug: Optional[str]
    value: Optional[str]

class TimeEntryAnlyzeItems(TimeEntryItems):
    meta: Optional[List[TimeEntryAnlyzeMeta]]

    """
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


 """


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

