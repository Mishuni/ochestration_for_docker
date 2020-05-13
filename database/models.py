from .db import db
import datetime

# class Movie(db.Document):
#     name = db.StringField(required=True, unique=True)
#     casts = db.ListField(db.StringField(), required=True)
#     genres = db.ListField(db.StringField(), required=True)


class Device(db.Document):
    id = db.IntField(required=True, primary_key=True)
    name = db.StringField(required=True, unique=True)
    ipv4Addr = db.StringField(required=True)
    register = db.DateTimeField(default=datetime.datetime.utcnow)

class RegisterQueue(db.Document):
    #id = db.IntField(required=True, primary_key=True)
    name = db.StringField(required=True, unique=True)
    ipv4Addr = db.StringField(required=True)
    register = db.DateTimeField(default=datetime.datetime.utcnow)
    cpu_count = db.IntField()
    os_system = db.StringField()
    hostname = db.StringField()
