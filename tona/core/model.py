import peewee
from datetime import datetime
from tona.core.db import db
from playhouse.shortcuts import model_to_dict

class Model(peewee.Model):

    active = peewee.BooleanField(default=True)
    created_at = peewee.DateTimeField(default=datetime.utcnow)
    edited_at = peewee.DateTimeField(default=datetime.utcnow)
    deleted_at = peewee.DateTimeField(null=True)


    class Meta:
        database = db

    def dict(self):
        return model_to_dict(self, exclude=['deleted_at', 'active'])
