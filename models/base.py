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
import datetime
from playhouse.shortcuts import model_to_dict
from utils import format_datetime, FORMAT_DATE

db = peewee.SqliteDatabase(None)

def setup(name):
    db.init(name)
    db.connect()


class BaseModel(peewee.Model):

    active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.utcnow)
    edited_at = peewee.DateTimeField(default=datetime.datetime.utcnow)


    class Meta:
        database = db

    @classmethod
    def check(cls, id):
        """ Deprecated """
        rows = cls.select().where(cls.id == id, cls.active == True).limit(1)
        if len(rows):
            return rows
        raise peewee.DoesNotExist(f"{cls.__name__}: Record ID {id} not found")

    @classmethod
    def exists(cls, id):
        row = cls.select().where(cls.id == id, cls.active == True).limit(1).get()
        if row is not None:
            return row
        raise peewee.DoesNotExist(f"{cls.__name__}: Record ID {id} not found")

    @classmethod
    def get_unarchived(cls):
        return cls.select().where(cls.active == True)

    @classmethod
    def get_archived(cls):
        return cls.select().where(cls.active == False)

    def to_dict(self):
        return model_to_dict(self, recurse=True, exclude=['active', 'created_at', 'edited_at'])

    @classmethod
    def prepare_fields(cls, data: dict, only: list = [], exclude: list = [], allowed: dict = {}):
        tmp = {}
        fields = allowed.keys()
        if len(only):
            fields = only
        for field in fields:
            if len(exclude) and field in exclude:
                continue
            if allowed.get(field) == 'str' and data.get(field, None):
                tmp.update({field: str(data.get(field))})
            if allowed.get(field) == 'int' and data.get(field, None):
                tmp.update({field: int(data.get(field))})
            if allowed.get(field) == 'date' and data.get(field, None):
                tmp.update({field: format_datetime(data.get(field), fmt_in=FORMAT_DATE, obj=True).date()})
            if allowed.get(field) == 'datetime' and data.get(field, None):
                tmp.update({field: format_datetime(data.get(field), obj=True)})
        if not len(tmp.keys()):
            raise Exception(f"{cls.__name__}: Fields allowed: {str(fields)} and exclude: {str(exclude)}")
        return tmp