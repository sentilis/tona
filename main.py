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

if os.getenv('TONA_ENV') == 'dev':
    PACKAGE_PARENT = '..'
    SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
    sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from tona.web.main import cli_webapp
from tona.models.base import setup as setup_db, db
from tona.models.time_entry import TimeEntry
from tona.models.project import Project
from tona.models.project_task import ProjectTask
from tona.models.objective import Objective
from tona.models.objective_keyresult import ObjectiveKeyResult
from tona.models.objective_keyresult_checkin import ObjectiveKeyResultCheckin
from tona.models.habit import Habit
from tona.models.habit_checkin import HabitCheckin

def extract_path(args):
    path = click.get_app_dir('tona')

    def index_path(key_arg):
        index = -1
        for i, arg in enumerate(args):
            if key_arg == arg:
                index = i + 1
                break
        return args[index]

    if args is not None and '-s' in args:
        path = index_path('-s')
    elif args is not None and '--storage' in args:
        path = index_path('--storage')
    elif os.environ.get('TONA_STORAGE', False):
        path = os.environ.get('TONA_STORAGE')

    if not os.path.exists(path):
        os.makedirs(path)
    return path

@click.group()
@click.pass_context
def cli(ctx):
    path = extract_path(ctx.obj.get('argv'))
    ctx.obj.update({'STORAGE': path})
    setup_db(os.path.join(path, "tona.db"))
    db.create_tables([TimeEntry,
                        Project, ProjectTask,
                        Objective, ObjectiveKeyResult, ObjectiveKeyResultCheckin,
                        Habit, HabitCheckin])

cli.add_command(cli_webapp)

def main():
    cli(obj={'argv': sys.argv})


if __name__ == "__main__":
    main()