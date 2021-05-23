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
from tona.models.time_entry import TimeEntry, active_time_entry, start_time_entry, stop_time_entry, fetch
from tona.utils import api_response

timer_bp = Blueprint('timer_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets',
                        url_prefix='/time-entry')

timer_api_bp = Blueprint('timer_api_bp', __name__,
                        url_prefix='/api/time-entry')

@timer_bp.route("/")
@timer_bp.route("/<id>")
def time_entry(id=""):

    is_timer = False
    time_entries = []
    time_entry = None
    if id == "":
        is_timer = True
        now = datetime.datetime.utcnow()
        tt = TimeEntry.select().where(
            (TimeEntry.start.year == now.year) & (TimeEntry.start.month == now.month) & (TimeEntry.start.day == now.day),
            TimeEntry.active == True, TimeEntry.stop != None).order_by(TimeEntry.stop.desc())
        time_entry = active_time_entry()
        ids = [t.id for t in tt ]
        time_entries = fetch(condition=f" where id in ({str(ids)[1:-1]}) order by stop desc")

    rt = render_template("view.html",
                            is_timer=is_timer,
                            time_entries=time_entries,
                            time_entry=time_entry)
    return rt

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
        ##app.logger.error(e)
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
        #app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code