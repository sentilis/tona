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
from flask import render_template, request, jsonify, flash
import datetime
from tona.web.main import app
from tona.utils import api_response
from tona.models.objective import Objective, create_objective
from tona.models.objective_keyresult import ObjectiveKeyResult, create_objective_keyresult, edit_objective_keyresult
from tona.models.objective_keyresult_checkin import create_objective_keyresult_checkin, ObjectiveKeyResultCheckin


@app.route("/objective")
@app.route("/objective/<objective_id>")
@app.route("/objective/<objective_id>/keyresult/<int:key_id>")
def objective(objective_id="", key_id=0):

    is_year = False
    is_objective = False
    is_keyresult = False

    objectives = []
    objective = None
    keyresults = []
    keyresult = None
    now = datetime.date.today()
    objectives = Objective.select().where(
        (Objective.start.year == now.year) & (Objective.due.year == now.year),
        Objective.active == True).order_by(Objective.name.asc())

    if objective_id == "year":
        is_year = True
        tmp = {}
        for o in objectives:
            tmp.update({ o : ObjectiveKeyResult.select().where(ObjectiveKeyResult.objective_id == o.id, ObjectiveKeyResult.active == True) })
        objectives = tmp
    else:
        try:
            objective_id = int("".join([n for n in objective_id if n.isdigit()]))
            if objective_id:
                objective = Objective.exists(objective_id)
                is_objective = True
                keyresults = ObjectiveKeyResult.select().where(ObjectiveKeyResult.objective_id == objective.id, ObjectiveKeyResult.active == True)
        except Exception as e:
            flash(str(e))

    if key_id:
        try:
            keyresult = ObjectiveKeyResult.exists(key_id)
            is_keyresult = True
        except Exception as e:
            flash(str(e))
    rt = render_template(
        "objective.html",
        is_year=is_year,
        is_objective=is_objective,
        objectives=objectives,
        objective=objective,
        is_keyresult=is_keyresult,
        keyresults=keyresults,
        keyresult=keyresult)
    return rt

@app.route("/api/objective", methods=['POST', 'GET'])
def api_objective():
    payload = api_response()
    code = 400
    try:
        if request.method == 'POST':
            data = request.json
            payload['payload'] = create_objective(data.get('name'), data.get('start'), data.get('due'))
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            rows = Objective.select().order_by(Objective.name.desc()).paginate(offset, limit)
            data = []
            for row in rows:
                data.append(row.to_dict())
            payload['payload'] = data
        payload['ok'] = True
        code = 200
    except Exception as e:
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code


@app.route("/api/objective/keyresult", methods=['POST'])
@app.route("/api/objective/keyresult/<int:id>", methods=['PUT'])
def api_objective_keyresult(id=0):
    payload = api_response()
    code = 400
    try:
        data = request.json
        if id and request.method == 'PUT':
            payload['payload'] = edit_objective_keyresult(id, **data)
        else:
            payload['payload'] = create_objective_keyresult(**data)
        payload['ok'] = True
        code = 200
    except Exception as e:
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code

@app.route("/api/objective/keyresult/checkin", methods=['POST', 'GET'])
def api_objective_keyresult_checkin(id=0):
    payload = api_response()
    code = 400
    try:
        if request.method == 'POST':
            data = request.json
            payload['payload'] = create_objective_keyresult_checkin(**data)
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            objective_keyresult_id = int(request.args.get('objective_keyresult_id', 0))
            data = []
            rows = []
            if objective_keyresult_id:
                rows = ObjectiveKeyResultCheckin.select().where(
                    ObjectiveKeyResultCheckin.objective_keyresult_id == objective_keyresult_id,
                ).order_by(ObjectiveKeyResultCheckin.checkin.desc()).paginate(offset, limit)
            else:
                rows = ObjectiveKeyResultCheckin.select().order_by(ObjectiveKeyResultCheckin.checkin.desc()).paginate(offset, limit)
            for row in rows:
                data.append(row.to_dict())
            payload['payload'] = data
        payload['ok'] = True
        code = 200
    except Exception as e:
        app.logger.error(e)
        payload['message'] = str(e)
    return jsonify(payload), code