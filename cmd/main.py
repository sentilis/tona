# -*- coding: utf-8 -*-
#    Copyright (C) 2021  The Project OKRESULTS Authors
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
from models.base import setup, db
from models.time_entry import TimeEntry
from models.project import Project
from models.project_task import ProjectTask
from models.objective import Objective
from models.objective_keyresult import ObjectiveKeyResult

@click.group()
def cli():
    setup("tona.db")
    db.create_tables([TimeEntry, Project, ProjectTask, Objective, ObjectiveKeyResult])

@click.command(name="webapp")
@click.option("--debug", "-d", is_flag=True)
@click.option("--port", "-p", type=click.INT, default=5001)
@click.option("--time-zone", "-t", type=click.STRING, default="UTC", help="Linux tz: https://superuser.com/a/1589527")
def cli_webapp(time_zone, port, debug):
    webapp.secret_key = os.urandom(16)
    webapp.config['tz'] = time_zone
    webapp.run(debug=debug, host='0.0.0.0', port=port)


cli.add_command(cli_webapp)

if __name__ == "__main__":
    cli()