from flask import render_template, request, jsonify
import datetime
from tona.web.main import app
from tona.models.time_entry import TimeEntry, active_time_entry, start_time_entry, stop_time_entry, fetch
from tona.utils import api_response

@app.route("/time-entry")
@app.route("/time-entry/<id>")
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

    rt = render_template("timer.html",
                            is_timer=is_timer,
                            time_entries=time_entries,
                            time_entry=time_entry)
    return rt

@app.route("/api/time-entry/start", methods=['POST'])
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
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code

@app.route("/api/time-entry/stop", methods=['POST'])
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