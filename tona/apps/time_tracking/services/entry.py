# -*- coding: utf-8 -*-
# Part of Sentilis. See LICENSE file for full copyright and licensing details.
from tona.apps.time_tracking.models.time_entry import TimeEntry
from tona.utils.exceptions import TonaException
from tona.utils.dt import format_datetime as fdt, FORMAT_DATETIME_UTC
from fastapi import status
import re

class Entry:

    def start(self, data: dict):
        if self.current() is not None:
            raise TonaException(status.HTTP_409_CONFLICT, "You have an active time entry")
        row = TimeEntry.create(**data)
        return row

    def current(self):
        try:
            row = TimeEntry.select().where(
                TimeEntry.active == True,
                TimeEntry.start != None,
                TimeEntry.stop == None).order_by(TimeEntry.start.desc()).limit(1).get()
            return row
        except Exception as e:
            pass
        return None

    def stop(self, id, data: dict):
        del data["id"]
        if id == 0:
            row = self.current()
            if row is None:
                raise Exception("Haven't an active time entry")
            id = row.id
        else:
            row = TimeEntry.get(id)
        start = row.start
        if isinstance(row.start, str):
            start = fdt(row.start, fmt_in=FORMAT_DATETIME_UTC, obj=True)
        duration = (data.get('stop') - start).total_seconds()
        data.update({"duration": duration})
        TimeEntry.update(data).where(TimeEntry.id == id).execute()
        return TimeEntry.get(id)

    def get_seconds(self, start, stop) -> float:
        return (stop - start).total_seconds()

    def create(self):
        pass

    def remove(self, id) -> bool:        
        TimeEntry.get(id)
        TimeEntry.delete().where(TimeEntry.id == id).execute()
        return True


    def edit(self, id, data: dict):
        time_entry = TimeEntry.get(id)
        duration = 0
        if 'start' in data.keys() and 'stop' not in data.keys():
            duration = self.get_seconds(data.get("start"),
                                        fdt(time_entry.stop, fmt_in=FORMAT_DATETIME_UTC, obj=True))
        elif 'stop' in data.keys() and 'start' not in data.keys():
            duration = self.get_seconds(fdt(time_entry.start, fmt_in=FORMAT_DATETIME_UTC, obj=True),
                                        data.get("stop"))
        elif 'start' in data.keys() and 'stop' in data.keys():
            duration = self.get_seconds(fdt(data.get("start"), fmt_in=FORMAT_DATETIME_UTC, obj=True),
                                        fdt(data.get("stop"), fmt_in=FORMAT_DATETIME_UTC, obj=True))
        if duration:
            if duration > 0:
                data.update(dict(duration=duration))
            else:
                raise TonaException(status.HTTP_400_BAD_REQUEST,
                                    "Duration has to be greater than zero. Change value Start or Stop")
        TimeEntry.update(data).where(TimeEntry.id == id).execute()
        return TimeEntry.get(id)


    def filter(self, params: dict):
        model = TimeEntry

        skip = params.get("skip", 0)
        limit = params.get("limit", 10)
        sort_by = params.get("sort_by")

        rows = model.select().where(model.active == True, model.stop != None)

        if sort_by and getattr(model, sort_by[1:], False):
            order_by_attr = getattr(model, sort_by[1:])
            order_by = order_by_attr.asc()
            if re.match("^-", sort_by):  # desc
                order_by = order_by_attr.desc()
            elif re.match("^\+", sort_by):  # asc
                pass
            rows = rows.order_by(order_by)
        return list(rows.offset(skip).limit(limit))