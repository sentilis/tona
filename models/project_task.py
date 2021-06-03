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
from tona.models.project import Project

class ProjectTask(BaseModel):

    class Meta:
        table_name = 'project_task'

    project_id = peewee.ForeignKeyField(Project)

    name = peewee.CharField()
    description = peewee.TextField(null=True)
    start = peewee.DateTimeField(null=True)
    due = peewee.DateTimeField(null=True)

    status = peewee.CharField(default='todo')  # todo, doing ,review, done
    priority = peewee.IntegerField(default=0)  # 1-high 2-medium 3-low

    @classmethod
    def edit(cls, id, **kwargs):
        data = cls.prepare_fields(kwargs, only=['name', 'description', 'status', 'due', 'priority'])
        if 'due' in kwargs.keys():
            due = kwargs.pop('due')
            if not due:
                data['due'] = None
        cls.update(data).where(cls.id == id).execute()
        return super(ProjectTask, cls).edit(id, **kwargs)

    @classmethod
    def add(cls, **kwargs):
        data = cls.prepare_fields(kwargs, only=['name', 'project_id'], required=True)
        Project.exists(data.get("project_id"))
        data_opt = cls.prepare_fields(kwargs, only=['description', 'status', 'due', 'priority'])
        data = {**data, **data_opt}
        id = cls.create(**data)
        return id.to_dict()
