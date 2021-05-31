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
import click
import os
from tona.utils import convert_datetime, FORMAT_DATE, FORMAT_DATETIME, FORMAT_TIME, format_time_duration
from tona.web.timer.timer import timer_bp,timer_api_bp

app = Flask(__name__)

@app.context_processor
def utility_processor():
    utility = dict(
        FORMAT_DATE=FORMAT_DATE,
        FORMAT_TIME=FORMAT_TIME,
        FORMAT_DATETIME=FORMAT_DATETIME,
        TZ=app.config['TZ'],
        format_time_duration=format_time_duration,
        convert_datetime=convert_datetime)
    return utility

@app.route("/")
def index():
    app.logger.info("Time Zone: "+ app.config['TZ'])
    app.logger.info("Storage: "+ app.config['STORAGE'])
    return render_template("index.html")

app.register_blueprint(timer_bp)
app.register_blueprint(timer_api_bp)

import tona.web.controllers.project
import tona.web.controllers.objective
import tona.web.controllers.habit



help_storage = "Custom data storage e.g ~/tona-data or skip this option exporing var e.g TONA_STORAGE=~/tona-data"
help_time_zone = "Frontend render datetime e.g America/Mexico_City"

@click.command(name="webapp")
@click.pass_context
@click.option("--debug", "-d", is_flag=True)
@click.option("--port", "-p", type=click.INT, default=5001)
@click.option("--time-zone", "-t", type=click.STRING, default="UTC", help=help_time_zone)
@click.option("--storage", "-s", type=click.STRING, help=help_storage)
def cli_webapp(ctx, time_zone, port, debug, storage):
    app.secret_key = os.urandom(16)
    app.config['STORAGE'] = ctx.obj.get('STORAGE')
    app.config['TZ'] = time_zone
    app.run(debug=debug, host='0.0.0.0', port=port)
    
    