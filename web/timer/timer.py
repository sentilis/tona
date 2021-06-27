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
from tona.models.attachment import Attachment
from tona.models.time_entry import TimeEntry, fetch
from tona.utils import api_response
from tona.models.project import Project
from tona.models.objective import Objective
from tona.models.habit import Habit
from tona.utils import (HTTPResponse, convert_datetime, format_time_duration,
                        FORMAT_DATETIME, FORMAT_DATE, build_csv, build_pdf,
                        save_attachment, remove_attachment)
from tona.web.app import app
import jinja2

timer_bp = Blueprint('timer_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets',
                        url_prefix='/time-entry')

timer_api_bp = Blueprint('timer_api_bp', __name__, url_prefix='/api/time-entry')

@timer_bp.route("/")
@timer_bp.route("/<int:id>")
def time_entry(id=0):
    time_entries = []
    now = datetime.date.today()
    time_entry = None
    tt = TimeEntry.select().where(
        (TimeEntry.start.year == now.year) & (TimeEntry.start.month == now.month) & (TimeEntry.start.day == now.day),
        TimeEntry.active == True, TimeEntry.stop != None).order_by(TimeEntry.stop.desc())
    ids = [t.id for t in tt ]
    time_entries = fetch(condition=f" where id in ({str(ids)[1:-1]}) order by stop desc")

    try:
        time_entry = TimeEntry.get(id)
    except Exception as e:
        pass
    rt = render_template("timer.html",
                            whoami='timer',
                            time_entry=time_entry,
                            time_entries=time_entries)
    return rt

@timer_bp.route("/analyze/<name>")
def time_entry_analyze(name):
    return render_template("timer_analyze.html", whoami=name)

@timer_bp.route("/settings/<name>")
def time_entry_settings(name):
    return render_template("timer.html", whoami=name)

@timer_api_bp.route("/<int:id>", methods=["PUT", "DELETE"])
def api_time_entry(id=0):
    res = HTTPResponse()
    try:
        if request.method == 'PUT':
            res.payload = TimeEntry.edit(id, **request.json).to_dict()
            res.code = 200
        elif request.method == 'DELETE':
            TimeEntry.remove(id)
            res.code = 201
        res.ok = True
    except Exception as e:
        res.message = str(e)
    return res.jsonify()

@timer_api_bp.route("/analyze", methods=['GET'])
def api_time_entry_analyze():
    resp = HTTPResponse()
    try:
        ttype = request.args.get('type', None)
        id = int(request.args.get('id', 0))
        start_date = request.args.get('start_date', None)
        end_date = request.args.get('end_date', None)
        export = request.args.get("export", None)

        data = {}
        rows = []

        if ttype == 'project':
            rows = TimeEntry.get_by_project(id, start_date, end_date)
        elif ttype == 'objective':
            rows = TimeEntry.get_by_objective(id, start_date, end_date)
        elif ttype == 'habit':
            rows = TimeEntry.get_by_habit(id, start_date, end_date)
        elif ttype == 'other':
            rows = TimeEntry.get_by_other(id, start_date, end_date)
        for row in rows:
            id = 0
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
                elif ttype == 'other':
                    type_data = {
                        'id': 0,
                        'name': 'Any time entry',
                    }
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

        resp.payload = {f'{ttype}s': data}
        if export and export in ['csv', 'pdf']:
            if export == 'csv':
                resp.payload = export_csv(ttype, resp.payload)
            elif export == 'pdf':
                resp.payload = export_pdf(ttype, resp.payload)
        resp.ok = True
        resp.code = 200
    except Exception as e:
        app.logger.error(e)
        resp.message = str(e)
        resp.payload = None
    return resp.jsonify()

@timer_api_bp.route("/running", methods=['GET'])
def api_time_entry_running():
    res = HTTPResponse()
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
    res = HTTPResponse()
    res.code = 400
    try:
        data = request.json
        res.payload = TimeEntry.start_timer(**data).to_dict()
        res.ok = True
        res.code = 200
    except Exception as e:
        app.logger.error(e)
        res.message = str(e)
    return jsonify(res.to_dict()), res.code

@timer_api_bp.route("/stop", methods=['POST'])
def api_time_entry_stop():
    res = HTTPResponse()
    res.code = 400
    try:
        data = request.json
        res.payload = TimeEntry.stop_timer(data.get("id"), stop=data.get('stop')).to_dict()
        res.ok = True
        res.code = 200
    except Exception as e:
        app.logger.error(e)
        res.message = str(e)
    return jsonify(res.to_dict()), res.code

def export_csv(ttype, data):
    rows = []
    for entry_type in data.keys():
        entry_group = data[entry_type]
        for entry_group_id in entry_group.keys():
            time_entries = entry_group[entry_group_id].get("time_entries")
            project = entry_group[entry_group_id].get(ttype)
            duration = entry_group[entry_group_id].get("duration")

            rows.append([project.get("name")])
            rows.append(["Name", "Start", "Stop", "Duration"])
            for time_entry in time_entries:
                rows.append([
                    time_entry.get("name"),
                    convert_datetime(time_entry.get("start"), fmt_out=FORMAT_DATETIME,  tz_out=app.config["TZ"]),
                    convert_datetime(time_entry.get("stop"), fmt_out=FORMAT_DATETIME, tz_out=app.config["TZ"]),
                    format_time_duration(time_entry.get("duration")),
                ])
            rows.append(["", "", "Total Hours:", format_time_duration(duration)])
            rows.append([])
    file_name = f"Tona Track - {str(ttype).capitalize()} - {datetime.date.today().strftime(FORMAT_DATE)}.csv"
    content = build_csv(app.config['STORAGE'], file_name, rows, is_tmp=True, is_base64=True)
    attachment = Attachment.select().where(Attachment.res_id == 1,
                                           Attachment.res_model == "timer_export_csv").first()
    if attachment:
        remove_attachment(app.config.get('STORAGE'), attachment=attachment)
        Attachment.remove(attachment.id)
    attachment = Attachment.add(name=file_name, mime="text/csv",
                                res_id=1, res_model="timer_export_csv")
    save_attachment(app.config.get('STORAGE'), attachment, content)
    return attachment.to_dict()


def export_pdf(ttype, data):
    loader = jinja2.FileSystemLoader("web/timer/templates")
    jenv = jinja2.Environment(loader=loader)
    template = jenv.get_or_select_template("timer_analyze_pdf_body.html")
    htmlout = template.render(
        ttype=ttype, payload=data,
        format_time_duration=format_time_duration,
        convert_datetime=convert_datetime,
        FORMAT_DATETIME=FORMAT_DATETIME,
        TZ=app.config["TZ"]
    )
    file_name = f"Tona Track - {str(ttype).capitalize()} - {datetime.date.today().strftime(FORMAT_DATE)}.pdf"
    content = build_pdf(app.config['STORAGE'], file_name,
                        "web/timer/templates/timer_analyze_pdf_header.html",
                        htmlout, "web/timer/templates/timer_analyze_pdf_footer.html",
                        is_tmp=True, is_base64=True)
    attachment = Attachment.select().where(Attachment.res_id == 1,
                                           Attachment.res_model == "timer_export_pdf").first()
    if attachment:
        remove_attachment(app.config.get('STORAGE'), attachment=attachment)
        Attachment.remove(attachment.id)
    attachment = Attachment.add(name=file_name, mime="application/pdf",
                                res_id=1, res_model="timer_export_pdf")
    save_attachment(app.config.get('STORAGE'), attachment, content)
    return attachment.to_dict()