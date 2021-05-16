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
from flask import Flask, render_template
from tona.models.time_entry import format_duration
from tona.utils import convert_datetime, FORMAT_DATE, FORMAT_DATETIME, FORMAT_TIME

app = Flask(__name__)

@app.context_processor
def utility_processor():
    utility = dict(
        FORMAT_DATE=FORMAT_DATE,
        FORMAT_TIME=FORMAT_TIME,
        FORMAT_DATETIME=FORMAT_DATETIME,
        TZ=app.config['TZ'],
        format_duration=format_duration,
        convert_datetime=convert_datetime)
    return utility

@app.route("/")
def index():
    return render_template("index.html")

import tona.web.controllers.project
import tona.web.controllers.time_entry
import tona.web.controllers.objective
import tona.web.controllers.habit