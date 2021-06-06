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


from flask import render_template, request, jsonify, flash, Blueprint
import datetime
from tona.web.app import app
from tona.models.project import create_project, Project
from tona.models.project_task import ProjectTask
from tona.utils import HTTPResponse, convert_datetime, str2int

project_bp = Blueprint('project_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets',
                        url_prefix='/project')

project_api_bp = Blueprint('project_api_bp', __name__, url_prefix='/api/project')

@project_bp.route("/")
@project_bp.route("/<project_id>")
@project_bp.route("/<project_id>/task")
@project_bp.route("/<project_id>/task/<int:task_id>")
def project(project_id="", task_id=0):

    is_today = False
    is_tomorrow = False
    is_week  = False
    is_project = False
    is_task = False

    projects = None
    project = None
    tasks = None
    task = None

    show_archive = request.args.get("archive", None)
    show_done = request.args.get("done", None)

    if project_id == "today":
        is_today = True
        now = datetime.datetime.utcnow()
        due = datetime.datetime.utcnow() + datetime.timedelta(days=-1)
        due = due.replace(hour=23, minute=59, second=59)

        tasks_due = ProjectTask.select().where(ProjectTask.due < due,
                                                    ProjectTask.due != None,
                                                    ProjectTask.status != 'done')
        tasks_today = ProjectTask.select().where( (ProjectTask.due.year == now.year) & (ProjectTask.due.month == now.month) & (ProjectTask.due.day == now.day),
                                                    ProjectTask.due != None,
                                                    ProjectTask.status != 'done')
        if not show_archive:
            tasks_due = tasks_due.where(ProjectTask.active == True)
            tasks_today = tasks_today.where(ProjectTask.active == True)
        tasks = {
            "overdue": tasks_due,
            "today": tasks_today,
        }
    elif project_id == "tomorrow":
        is_tomorrow = True
        now = datetime.datetime.utcnow() + datetime.timedelta(days=1)
        tasks_tomorrow = ProjectTask.select().where( (ProjectTask.due.year == now.year) & (ProjectTask.due.month == now.month) & (ProjectTask.due.day == now.day),
                                                    ProjectTask.due != None,
                                                    ProjectTask.status != 'done')
        if not show_archive:
            tasks_tomorrow = tasks_tomorrow.where(ProjectTask.active == True)

        tasks = {
            "tomorrow": tasks_tomorrow,
        }
    elif project_id == "week":
        is_week = True
        tasks = {}
        groups = {"overdue": -1, "today": 0, "+1": 1, "+2": 2,"+3": 3, "+4": 4, "+5": 5}

        for group in groups:
            now = datetime.datetime.utcnow() + datetime.timedelta(days=groups.get(group))
            if group == 'overdue':
                now = now.replace(hour=23, minute=59, second=59)
                tasks_due = ProjectTask.select().where(ProjectTask.due < now,
                                                    ProjectTask.due != None,
                                                    ProjectTask.status != 'done')
                if not show_archive:
                    tasks_due = tasks_due.where(ProjectTask.active == True)
                tasks[group] = tasks_due
            else:
                label = convert_datetime(now, tz_out=app.config['TZ'], fmt_out="%A, %b %d") if group != 'today' else 'today'
                tasks_week = ProjectTask.select().where(
                                                    (ProjectTask.due.year == now.year) &
                                                    (ProjectTask.due.month == now.month) &
                                                    (ProjectTask.due.day == now.day),
                                                    ProjectTask.due != None,
                                                    ProjectTask.status != 'done')
                if not show_archive:
                    tasks_week = tasks_week.where(ProjectTask.active == True)
                tasks[label] = tasks_week

    else:
        try:
            project_id = str2int(project_id)
            project = Project.get(project_id)
            is_project = True
            tasks = {}
            for status in ['todo', 'doing', 'review', 'done']:
                if status == 'done' and not show_done:
                    continue
                tasks_status = ProjectTask.select().where(ProjectTask.project_id == project.id,
                                                    ProjectTask.status == status)
                if not show_archive:
                    tasks_status = tasks_status.where(ProjectTask.active == True)
                tasks[status] = tasks_status
        except Exception as e:
            flash(str(e))

    if task_id:
        try:
            task = ProjectTask.get(task_id)
            is_task = True
        except Exception as e:
            flash(str(e))

    projects = Project.select().where(Project.active == True).order_by(Project.name.asc())

    rt = render_template(
        "project.html",
        is_today=is_today,
        is_tomorrow=is_tomorrow,
        is_week=is_week,
        is_project=is_project,
        projects=projects,
        project=project,
        is_task=is_task,
        tasks=tasks,
        task=task)
    return rt

@project_api_bp.route("", methods=['POST', 'GET'])
def api_project():
    res = HTTPResponse()
    res.code = 400
    try:
        if request.method == 'POST':
            data = request.json
            res.payload = create_project(data.get('name'))
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            rows = Project.select().order_by(Project.name.desc()).paginate(offset, limit)
            data = []
            for row in rows:
                data.append(row.to_dict())
            res.payload = data
        res.ok = True
        res.code = 200
    except Exception as e:
        app.logger.error(e)
        res.message = str(e)
    return jsonify(res.to_dict()), res.code

@project_api_bp.route("/task", methods=['POST'])
@project_api_bp.route("/task/<int:id>", methods=['PUT', 'DELETE'])
def api_project_task(id=0):
    res = HTTPResponse()
    res.code = 400
    try:
        data = request.json
        if request.method == 'POST':
            res.payload = ProjectTask.add(**data).to_dict()
        elif request.method in ['PUT']:
            res.payload = ProjectTask.edit(id, **data).to_dict()
        elif request.method == 'DELETE':
            ProjectTask.remove(id)
        res.ok = True
        res.code = 200
    except Exception as e:
        app.logger.error(e)
        res.message = str(e)
    return jsonify(res.to_dict()), res.code