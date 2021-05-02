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
import peewee
from models.base import BaseModel
import re
import datetime
from dateutil.relativedelta import relativedelta

Q  = '*q'
Q1 = '*q1'
Q2 = '*q2'
Q3 = '*q3'
Q4 = '*q4'
M  = '*m'
Y  = '*y'
D  = '*d'

class Objective(BaseModel):

    class Meta:
        table_name = 'objective'

    name = peewee.CharField()
    start_at = peewee.DateField()
    due_at = peewee.DateField()

"""
def get_quarter_by_date(dt: datetime.date):
    month = dt.month

    def get_quarter_dates(dt: datetime.date, max_month):
        m = (dt.month + 2) - max_month 
        dt_start = None
        dt_end = None
        if m == 0:
            dt_start =  dt
            dt_end = dt + relativedelta(months=2) 
        elif m == 1:
            dt_start = dt - relativedelta(months=1)
            dt_end = dt + relativedelta(months=1)
        else:
            dt_start = dt - relativedelta(months=2)
            dt_end =  dt            
        
        next_month = dt_end.replace(day=28) + datetime.timedelta(days=4)
        dt_end = next_month - datetime.timedelta(days=next_month.day)

        return dt_start.replace(day=1), dt_end
    
    data = {}

    if 1 <= month <= 3:
        start, end = get_quarter_dates(dt, 3)
        data.update( {
            'quarter_name': Q1,
            'quarter_start_date': start,
            'quarter_end_date': end
        })
    elif 4 <= month <= 6:
        start, end = get_quarter_dates(dt, 6)
        data.update({
            'quarter_name': Q2,
            'quarter_start_date': start,
            'quarter_end_date': end
        })
    elif 7 <= month <= 9:
        start, end = get_quarter_dates(dt, 9)
        data.update({
            'quarter_name': Q3,
            'quarter_start_date': start,
            'quarter_end_date': end
        })
    else: 
        start, end = get_quarter_dates(dt, 12)
        data.update({
            'quarter_name': Q4,
            'quarter_start_date': start,
            'quarter_end_date': end
        })
    return data

def get_quarter_by_name(name: str = Q):
    today = datetime.date.today()
    if name == Q1:
        return get_quarter_by_date(today.replace(month=2))
    elif name == Q2:
        return get_quarter_by_date(today.replace(month=5))
    elif name == Q3:
        return get_quarter_by_date(today.replace(month=8))
    elif name == Q4:
        return get_quarter_by_date(today.replace(month=11))
    return get_quarter_by_date(today)

def objective_smart_name(name):
    
        1.- This a simple objective name
            {
                'name': 'This a simple objective',
                'start_date': 'YYYY-MM-DD HH:MM:SS',
                'end_date': 'YYYY-MM-DD HH:MM:SS',
            }
        2.- This an objetive name with cicle *q1
        *q1 - Jan-Mar 
        *q2 - Apr-Jun
        *q3 - Jul-Sep
        *q4 - Oct-Dic
        *q  - current quarter
        *y  - year [Current year]
        *m  - month [Current month]
        *d  - day [Current day]
    
    data = {}
    find_date = re.search(r"(\*d)|(\*m)|(\*q1)|(\*q2)|(\*q3)|(\*q4)|(\*y)", name)
    objective_date = get_quarter_by_name()
    if find_date:
        smart_date = find_date.group()
        if smart_date in [Q1, Q2, Q3, Q4]:
            objective_date = get_quarter_by_name(smart_date)
    
    data.update({
        'name': name,
        'start_date': objective_date.get('quarter_start_date'),
        'end_date': objective_date.get('quarter_end_date'),
    })
    return data"""