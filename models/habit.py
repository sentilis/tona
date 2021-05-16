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
from tona.models.base import BaseModel

class Habit(BaseModel):

    class Meta:
        table_name = 'habit'

    name = peewee.CharField()
    frequency = peewee.CharField(default="daily")  # daily, weekly, interval
    # daily: mon,thus,wed ... weekly: 1week o  interval: 3days, 5days
    every = peewee.CharField(default="sunday,monday,tuesday,wednesday,thursday,friday,saturday")

    @classmethod
    def prepare_fields(self, data, only=[], exclude=[], allowed={}):
        allowed = {
            'name': 'str',
            'frequency': 'str',
            'every': 'str'
        }
        return super(Habit, self).prepare_fields(data, only=only, exclude=exclude, allowed=allowed)

def create_habit(**kwargs):
    data = Habit.prepare_fields(kwargs, only=['name'])
    row = Habit.create(**data)
    return row.to_dict()