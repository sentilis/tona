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

class Attachment(BaseModel):

    class Meta:
        table_name = 'attachment'

    name = peewee.CharField()
    mime = peewee.CharField()

    res_model = peewee.CharField()
    res_id = peewee.IntegerField()

    @classmethod
    def edit(cls, id, **kwargs):
        cls.get(id)
        data = cls.prepare_fields(kwargs, only=['name'])
        cls.update(data).where(cls.id == id).execute()
        return super(Attachment, cls).edit(id, **kwargs)

    @classmethod
    def add(cls, **kwargs):
        data = cls.prepare_fields(kwargs, only=['name', 'mime', 'res_id', 'res_model'], required=True)
        return cls.create(**data)