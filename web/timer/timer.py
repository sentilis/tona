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
from flask import Blueprint, render_template, request, jsonify
import datetime
from tona.models.time_entry import TimeEntry, start_time_entry, stop_time_entry, fetch
from tona.utils import api_response
from tona.models.project import Project
from tona.models.objective import Objective
from tona.models.habit import Habit
from tona.utils import APIResponse

timer_bp = Blueprint('timer_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets',
                        url_prefix='/time-entry')

timer_api_bp = Blueprint('timer_api_bp', __name__, url_prefix='/api/time-entry')

@timer_bp.route("/")
def time_entry():
    time_entries = []
    now = datetime.date.today()
    tt = TimeEntry.select().where(
        (TimeEntry.start.year == now.year) & (TimeEntry.start.month == now.month) & (TimeEntry.start.day == now.day),
        TimeEntry.active == True, TimeEntry.stop != None).order_by(TimeEntry.stop.desc())
    ids = [t.id for t in tt ]
    time_entries = fetch(condition=f" where id in ({str(ids)[1:-1]}) order by stop desc")

    rt = render_template("timer.html",
                            whoami='timer',
                            time_entries=time_entries)
    return rt

@timer_bp.route("/analyze/<name>")
def time_entry_analyze(name):
    return render_template("timer_analyze.html", whoami=name)


@timer_bp.route("/settings/<name>")
def time_entry_settings(name):
    return render_template("timer.html", whoami=name)


@timer_api_bp.route("/analyze", methods=['GET'])
def api_time_entry():
    payload = api_response()
    code = 400
    try:
        ttype = request.args.get('type', None)
        id = int(request.args.get('id', 0))
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)

        data = {}
        rows = []

        if ttype == 'project':
            rows = TimeEntry.get_by_project(id, start_date, end_date)
        elif ttype == 'objective':
            rows = TimeEntry.get_by_objective(id, start_date, end_date)
        elif ttype == 'habit':
            rows = TimeEntry.get_by_habit(id, start_date, end_date)

        for row in rows:
            id = row.id
            name = row.name
            if ttype == 'project':
                id = row.projecttask.project_id.id
                name = row.projecttask.name
            elif ttype == 'objective':
                id = row.objectivekeyresult.objective_id.id
                name = row.objectivekeyresult.name
            elif ttype == 'habit':
                id = row.habit.id
                name = row.habit.name

            if not data.get(id, None):
                if ttype == 'project':
                    type_data = Project.exists(id).to_dict()
                elif ttype == 'objective':
                    type_data = Objective.exists(id).to_dict()
                elif ttype == 'habit':
                    type_data = Habit.exists(id).to_dict()
                data[id] = {
                    'time_entries': [],
                    "duration": 0,
                    f"{ttype}": type_data
                }
            data[id]['time_entries'].append({
                    'name': name,
                    'start': row.start,
                    'stop': row.stop,
                    'duration': row.duration,
                    'id': row.id
            })
            data[id]['duration'] += row.duration

        payload['payload'] = {
            f'{ttype}s': data,
        }
        payload['ok'] = True
        code = 200
    except Exception as e:
        print(e)
        payload['message'] = str(e)
    return jsonify(payload), code

@timer_api_bp.route("/running", methods=['GET'])
def api_time_entry_running():
    res = APIResponse()
    res.code = 404
    try:
        time_entry = TimeEntry.running()
        if time_entry:
            res.payload = time_entry.to_dict()
            data = fetch(condition=f" where id = ({res.payload.get('id')})")
            if len(data):
                res.payload.update({'name': data[0][1]})
            res.ok = True
            res.code = 200
    except Exception as e:
        res.message = str(e)
    return jsonify(res.to_dict()), res.code

@timer_api_bp.route("/start", methods=['POST'])
def api_time_entry_start():
    payload = api_response()
    code = 400
    try:
        data = request.json
        payload['payload'] = start_time_entry(
            data.get('name', ''),
            data.get('start'),
            res_model=data.get('res_model', None),
            res_id=data.get('res_id', None))
        payload['ok'] = True
        code = 200
    except Exception as e:
        payload['message'] = str(e)
    return jsonify(payload), code

@timer_api_bp.route("/stop", methods=['POST'])
def api_time_entry_stop():
    payload = api_response()
    code = 400
    try:
        data = request.json
        payload['payload'] = stop_time_entry(int(data.get('id')), data.get('stop'))
        payload['ok'] = True
        code = 200
    except Exception as e:
        payload['message'] = str(e)
    return jsonify(payload), code