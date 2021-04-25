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
from commands.objective import objective as command_objective
from models.base import setup, db
from models.objective import Objective
import os

@click.group()
def cli():
    #path= "~/.local/share/okresults"
    #if not os.path.exists(path):
    #    os.mkdir(path)
    setup("okresults.db")
    db.create_tables([Objective])
cli.add_command(command_objective)

if __name__ == "__main__":
    cli()