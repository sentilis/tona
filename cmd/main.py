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

from web.main import  app as webapp
from models.base import setup, db
from models.objective import Objective
from models.keyresult import KeyResult

from objective import objective as command_objective
from keyresult import keyresult as command_keyresult

@click.group()
def cli():
    #path= "~/.local/share/okresults"
    #if not os.path.exists(path):
    #    os.mkdir(path)
    setup("tona.db")
    db.create_tables([Objective, KeyResult])

@click.command(name="web")
@click.option("--conf","-c", is_flag=True)
def cli_web(conf):
    webapp.run(debug=True, host='0.0.0.0', port=5001)

cli.add_command(cli_web)
cli.add_command(command_objective)
cli.add_command(command_keyresult)

if __name__ == "__main__":
    cli()