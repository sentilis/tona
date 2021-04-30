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
from flask import Flask, render_template, request, jsonify
from os.path import join
from models.time_entry import start_time_entry, stop_time_entry, TimeEntry,\
                              active_time_entry, format_duration
from utils import api_response

app = Flask(__name__)
api = "/api"

@app.context_processor
def utility_processor():
    return dict(format_duration=format_duration)

@app.route("/")
def index():
    return render_template("index.html")

# Timer
#
@app.route("/timer")
def timer():
    rows = TimeEntry.select().where(TimeEntry.active == True).order_by(TimeEntry.stop.desc()).limit(10)
    te = active_time_entry()
    return render_template("timer/timer.html", rows=rows, time_entry=te)

# API Timer
@app.route(join(api, "time-entry/start"), methods=['POST'])
def api_time_entry_start():
    payload = api_response()
    code = 400
    try:
        data = request.json
        payload['payload'] = start_time_entry(data.get('name'), data.get('start'))
        payload['ok'] = True
        code = 200
    except Exception as e:
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code

@app.route(join(api, "time-entry/stop"), methods=['POST'])
def api_time_entry_stop():
    payload = api_response()
    code = 400
    try:
        data = request.json
        payload['payload'] = stop_time_entry(int(data.get('id')), data.get('stop'))
        payload['ok'] = True
        code = 200
    except Exception as e:
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code