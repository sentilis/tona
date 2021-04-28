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
from peewee import *
from models.base import BaseModel
from models.objective import Objective
import re

INCREASING = 'increasing'
DECREASING = 'decreasing'

class KeyResult(BaseModel):
    
    objective_id = ForeignKeyField(Objective)

    name = CharField()
    metric_measure = CharField(max_length=10, default='percent') # percent%, number# , currency$, custom x
    changes_metric = CharField(max_length=20, default='increasing') # increasing+, decreasing-
    start_value = IntegerField( default=0)
    target_value = IntegerField( default=100)
    start_date = DateField()
    end_date = DateField()
    status = CharField(max_length=10, default='off-track') # off-track (<60) at-risk (>60 80<) on-track (>80)

def get_metric_measure(name):
    find_metric_measure = re.search(r"(\/\S+)", name)
    metric_measure = 'percent'
    if find_metric_measure:
        metric_measure = find_metric_measure.group().replace('/','')
        if metric_measure == '$':
            metric_measure = 'currency'
        elif metric_measure == '#':
            metric_measure = 'number'
        elif metric_measure == '%':
            metric_measure = 'percent'
    return metric_measure

def get_changes_metric(name):
    find_changes_metric = re.search(r"(\+)|(\-)", name)
    changes_metric = 'increasing'
    if find_changes_metric:
        changes_metric = find_changes_metric.group()
        if changes_metric == '-':
            changes_metric = 'decreasing'
    return changes_metric

def get_start_target_value(name):
    start = 0 
    target = 100
    find_st = re.search(r"(\d+\+)|(\d+\-)", name)
    cm = get_changes_metric(name)
    if find_st: 
        val = find_st.group()
        if '-' in val:
            start = int(val.replace('-',''))
            target = 0
        else:
            start = 0
            target = int(val.replace('+',''))
    return start, target

def get_objective_id(name):
    id = 0
    find_oi = re.search(r"(\d+\.)", name)
    if find_oi:
        id = int(find_oi.group().replace(".", ""))
        Objective.exists(id)
    else:
        raise Exception("The Key Result not has objective ID e.g 12. keyResult")
    return id 

def get_start_end_date(name):
    objective_id = get_objective_id(name)
    rows = Objective.exists(objective_id)
    return rows[0].start_date, rows[0].end_date

def keyresult_smart_name(name, objective_id=True):
    
    metric_measure = get_metric_measure(name)
    changes_metric = get_changes_metric(name)    
    start_value, target_value = get_start_target_value(name)

    if isinstance(objective_id, bool) and objective_id:
        objective_id = get_objective_id(name)
        start_date, end_date = get_start_end_date(name)
    data = {
        "name": name,
        "objective_id": objective_id or None,
        "metric_measure": metric_measure,
        "changes_metric": changes_metric,
        "start_value": start_value,
        "target_value": target_value,
        "start_date": start_date,
        "end_date": end_date,
    }

    return data