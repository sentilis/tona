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

db = peewee.SqliteDatabase(None)

def setup(name):
    db.init(name)
    db.connect()


class BaseModel(peewee.Model):

    active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.datetime.now)
    edited_at = peewee.DateTimeField(default=datetime.datetime.now)


    class Meta:
        database = db

    @classmethod
    def check(cls, id):
        rows = cls.select().where(cls.id == id, cls.active == True).limit(1)
        if len(rows):
            return rows
        raise DoesNotExist(f"{cls.__name__}: Record ID {id} not found")

    @classmethod
    def get_unarchived(cls):
        return cls.select().where(cls.active == True)

    @classmethod
    def get_archived(cls):
        return cls.select().where(cls.active == False)