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
from utils import format_datetime

class ProjectTask(BaseModel):

    class Meta:
        table_name = 'project_task'

    project_id = peewee.ForeignKeyField(Project)

    name = peewee.CharField()
    description = peewee.TextField(null=True)
    start = peewee.DateTimeField(null=True)
    due = peewee.DateTimeField(null=True)

    status = peewee.CharField(default='todo')  # todo, doing ,review, done
    priority = peewee.IntegerField(default=1)  # 1-high 2-medium 3-low


def create_project_task(project_id: int, name: str):
    Project.check(project_id)
    data = {"name": name, "project_id": project_id}
    id = ProjectTask.create(**data)
    return id.to_dict()

def edit_project_task(id: int, name: str = None, description: str = None, status: str = None, due: str = None):
    ProjectTask.check(id)
    data = {}
    if name is not None:
        data.update({ProjectTask.name: name})
    if description is not None:
        data.update({ProjectTask.description: description})
    if status is not None:
        data.update({ProjectTask.status: status})
    if due is not None:
        print(due)
        data.update({ProjectTask.due: format_datetime(due)})
    if not len(data.keys()):
        raise Exception("ProjectTask: is requried min 1 for update")

    ProjectTask.update(data).where(ProjectTask.id == id).execute()
    data = ProjectTask.check(id)[0]
    return data.to_dict()