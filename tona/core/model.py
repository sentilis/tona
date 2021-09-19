import peewee
from datetime import datetime
from tona.core.db import db
from playhouse.shortcuts import model_to_dict
from tona.utils.dt import format_datetime as fdt
import json
import re

class Model(peewee.Model):

    active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.utcnow)
    edited_at = peewee.DateTimeField(default=datetime.utcnow)
    deleted_at = peewee.DateTimeField(null=True)


    class Meta:
        database = db

    def dict(self):
        return model_to_dict(self, exclude=['deleted_at', 'active'])



def advance_filters(model, rows, params: dict):
    """

        create_at__lte : pub_date <= val
        create_at__gte :          >= val
        https://www.hacksoft.io/blog/django-filter-chaining
        https://django-property-filter.readthedocs.io/en/latest/ref/filters.html

    """
    skip = params.get("skip", 0)
    limit = params.get("limit", 100)
    sort_by = params.get("sort_by", "-created_at")
    filters  = {}
    try:
        filters = json.loads(params.get("filters", "{}"))
    except: 
        pass

    if sort_by and getattr(model, sort_by[1:], False):
        order_by_attr = getattr(model, sort_by[1:])
        order_by = order_by_attr.asc()
        if re.match("^-", sort_by):  # desc
            order_by = order_by_attr.desc()
        elif re.match("^\+", sort_by):  # asc
            pass
        rows = rows.order_by(order_by)
    
    if filters.keys():
        rows = rows.filter(**filters)

    if skip == 0 and limit == 0:
        return rows
    return list(rows.offset(skip).limit(limit))