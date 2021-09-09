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
from .drive_folder import DriveFolder
from typing import Optional, Any

class DriveFile(Model):

    name = peewee.CharField()
    mimetype = peewee.CharField()
    file = peewee.CharField()
    file_hash = peewee.CharField(null=True)

    drive_folder_id = peewee.ForeignKeyField(DriveFolder, null=True)

    class Meta:
        table_name = 'drive_file'

    class Pydantic(PydanticBaseModel):
        id: Optional[int]
        name: str
        mimetype: str
        file: Optional[str]
        drive_folder_id: Optional[Any]
        file_hash: Optional[str]
