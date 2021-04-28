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
from utils import name_constraint
from models.objective import Objective, objective_smart_name
import tabulate
from peewee import DoesNotExist

@click.command()
@click.option("--add","-a", is_flag=True)
@click.option("--delete","-d", type=click.INT)
@click.option("--edit","-e",type=click.INT)
@click.argument("name", nargs=-1)
def objective(add, delete, edit, name):
    """
        --add
        ! -> Priority 
        # -> Tags
        * -> Due date
        --delete ID
        --edit ID 
    """
    
    def print_objectives(rows):
        headers = [ 'id', 'Status', 'Start date', 'End date', 'Name']
        table = []
        for row in rows:
            table.append([ row.id, row.status, row.start_date, row.end_date, row.name])
        print(tabulate.tabulate(table, headers))

    if add:
        objective_name = name_constraint(name)
        objective = objective_smart_name(objective_name)
        id = Objective.create(**objective)
        rows = Objective.select().where(Objective.id==id).limit(1)
        print_objectives(rows)
    elif delete:
        try:
            rows = Objective.exists(delete)
            Objective.update({Objective.active: False}).where(Objective.id==delete).execute()
            print_objectives(rows)
        except DoesNotExist as e:
            print(f"Record ID {delete} not found")
    elif edit:
        try:
            objective_name = name_constraint(name)
            Objective.exists(edit)            
            objective = objective_smart_name(objective_name)
            Objective.update(**objective).where(Objective.id==edit).execute()
            row = Objective.select().where(Objective.id==edit).limit(1)
            print_objectives(row)
        except DoesNotExist as e:
            print(f"Record ID {delete} not found")
        except Exception as e:
            print(e)
    else:        
        rows = Objective.select().where(Objective.active == True)
        print_objectives(rows)
        