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
from models.base import BaseModel
from models.project import Project

class ProjectTask(BaseModel):

    project_id = peewee.ForeignKeyField(Project)

    name = peewee.CharField()
    description = peewee.TextField()
    start = peewee.DateTimeField()
    due = peewee.DateTimeField()

    status = peewee.CharField()  # todo, doing , done
    priority = peewee.IntegerField()