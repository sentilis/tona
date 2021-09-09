# -*- coding: utf-8 -*-
#   Copyright (C) The TONA Authors
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
from tona.core import Model, PydanticBaseModel
from typing import Optional, Any

class DriveFolder(Model):

    name = peewee.CharField()
    parent_id = peewee.ForeignKeyField('self', null=True)
    path_hash = peewee.CharField(null=True)

    class Meta:
        table_name = 'drive_folder'

    class Pydantic(PydanticBaseModel):
        id: Optional[int]
        name: str
        parent_id: Optional[Any]
        path_hash: Optional[str]