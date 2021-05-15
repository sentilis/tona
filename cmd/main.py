# -*- coding: utf-8 -*-
#    Copyright (C) 2021 The Project TONA Authors
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
import click

import os
import sys

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from web.main import app as webapp
from models.base import setup as setup_db, db
from models.time_entry import TimeEntry
from models.project import Project
from models.project_task import ProjectTask
from models.objective import Objective
from models.objective_keyresult import ObjectiveKeyResult
from models.objective_keyresult_checkin import ObjectiveKeyResultCheckin
from models.habit import Habit
from models.habit_checkin import HabitCheckin

def extract_path(args):
    path = click.get_app_dir('tona')

    def index_path(key_arg):
        index = -1
        for i, arg in enumerate(args):
            if key_arg == arg:
                index = i + 1
                break
        return args[index]

    if '-s' in args:
        path = index_path('-s')
    elif '--storage' in args:
        path = index_path('--storage')
    elif os.environ.get('TONA_STORAGE', False):
        path = os.environ.get('TONA_STORAGE')

    if not os.path.exists(path):
        os.makedirs(path)
    return path

@click.group()
@click.pass_context
def cli(ctx):
    path = extract_path(ctx.obj)
    webapp.config['STORAGE'] = path
    setup_db(os.path.join(path, "tona.db"))
    db.create_tables([TimeEntry,
                        Project, ProjectTask,
                        Objective, ObjectiveKeyResult, ObjectiveKeyResultCheckin,
                        Habit, HabitCheckin])


help_storage = "Custom data storage e.g ~/tona-data or skip this option exporing var e.g TONA_STORAGE=~/tona-data"
help_time_zone = "Frontend render datetime e.g America/Mexico_City"

@click.command(name="webapp")
@click.option("--debug", "-d", is_flag=True)
@click.option("--port", "-p", type=click.INT, default=5001)
@click.option("--time-zone", "-t", type=click.STRING, default="UTC", help=help_time_zone)
@click.option("--storage", "-s", type=click.STRING, help=help_storage)
def cli_webapp(time_zone, port, debug, storage):

    webapp.secret_key = os.urandom(16)
    webapp.config['TZ'] = time_zone
    webapp.logger.info("Time Zone: ", time_zone)
    webapp.logger.info("Storage: ", storage)
    webapp.run(debug=debug, host='0.0.0.0', port=port)


cli.add_command(cli_webapp)

if __name__ == "__main__":
    cli(obj=sys.argv)