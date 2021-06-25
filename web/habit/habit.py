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
import datetime
from flask import render_template, request, jsonify, flash, Blueprint
from tona.web.main import app
from tona.utils import HTTPResponse, str2int, format_datetime
from tona.models.habit import Habit
from tona.models.habit_checkin import HabitCheckin


habit_bp = Blueprint('habit_bp', __name__,
                        template_folder='templates',
                        static_folder='static', static_url_path='assets',
                        url_prefix='/habit')

habit_api_bp = Blueprint('habit_api_bp', __name__, url_prefix='/api/habit')

@habit_bp.route("/")
@habit_bp.route("/<habit_id>")
def habit(habit_id=""):

    is_today = False
    habits_aux = []

    habits = []
    is_habit = False
    habit = None

    habits = Habit.select().where(Habit.active == True).order_by(Habit.name.asc())

    if habit_id == "today" or habit_id == "":
        is_today = True
        today = datetime.date.today()
        weekday = format_datetime(today, fmt_out='%A')        
        checked = Habit.select().join(HabitCheckin).where(
            Habit.frequency == 'daily',
            Habit.every.contains(weekday.lower()),
            HabitCheckin.checkin == today
            )
        has_checkin = [ r.id for r in checked ]
        unchecked = Habit.select().where(
           Habit.frequency == 'daily',
           Habit.id.not_in( has_checkin)
        )
        habits_aux = {
            'unchecked': unchecked,
            'checked': checked
        }
    elif habit_id == "archive":
        pass
    else:
        try:
            habit_id = str2int(habit_id)
            habit = Habit.exists(habit_id)
            is_habit = True
        except Exception as e:
            flash(str(e))
    rt = render_template(
        "habit.html",
        habits_aux=habits_aux,
        habits=habits,
        habit=habit,
        is_habit=is_habit,
        is_today=is_today)
    return rt


@habit_api_bp.route("", methods=['POST', 'GET'])
def api_habit():
    resp = HTTPResponse()
    try:
        if request.method == 'POST':
            data = request.json
            resp.payload = Habit.add(**data).to_dict()
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            rows = Habit.select().order_by(Habit.name.desc()).paginate(offset, limit)
            data = []
            for row in rows:
                data.append(row.to_dict())
            resp.payload = data
        resp.ok = True
        resp.code = 200
    except Exception as e:
        app.logger.error(e)
        resp.message = str(e)
    return jsonify(resp.to_dict()), resp.code


@habit_api_bp.route("/checkin", methods=['POST', 'GET'])
def api_habit_checkin():
    resp = HTTPResponse()
    try:
        if request.method == 'POST':
            data = request.json
            resp.payload = HabitCheckin.add(**data).to_dict()
        else:
            offset = int(request.args.get('offset', 1))
            limit = int(request.args.get('limit', 10))
            habit_id = int(request.args.get('habit_id', 0))
            data = []
            rows = []
            if habit_id:
                rows = HabitCheckin.select().where(
                    HabitCheckin.habit_id == habit_id,
                ).order_by(HabitCheckin.checkin.desc()).paginate(offset, limit)
            else:
                rows = HabitCheckin.select().order_by(HabitCheckin.checkin.desc()).paginate(offset, limit)
            for row in rows:
                data.append(row.to_dict())
            resp.payload = data
        resp.ok = True
        resp.code = 200
    except Exception as e:
        app.logger.error(e)
        resp.message = str(e)
    return jsonify(resp.to_dict()), resp.code