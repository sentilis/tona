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
from tona.models.objective_keyresult import ObjectiveKeyResult


class ObjectiveKeyResultCheckin(BaseModel):

    class Meta:
        table_name = 'objective_keyresult_checkin'

    objective_keyresult_id = peewee.ForeignKeyField(ObjectiveKeyResult)

    name = peewee.TextField()
    checkin = peewee.DateField()

    @classmethod
    def prepare_fields(self, data, only=[], exclude=[], allowed={}):
        allowed = {
            'name': 'str',
            'checkin': 'date',
            'objective_keyresult_id': 'int'
        }
        return super(ObjectiveKeyResultCheckin, self).prepare_fields(data, only=only, exclude=exclude, allowed=allowed)

def create_objective_keyresult_checkin(**kwargs):
    data = ObjectiveKeyResultCheckin.prepare_fields(kwargs, only=['name', 'checkin','objective_keyresult_id'])
    row = ObjectiveKeyResultCheckin.create(**data)
    return row.to_dict()