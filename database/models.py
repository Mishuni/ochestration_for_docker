from .db import db
import datetime

# class Movie(db.Document):
#     name = db.StringField(required=True, unique=True)
#     casts = db.ListField(db.StringField(), required=True)
#     genres = db.ListField(db.StringField(), required=True)


class Device(db.Document):
    id = db.IntField(required=True, unique=True, primary_key=True)
    name = db.StringField(required=True)
    ipv4Addr = db.StringField(required=True)
    register = db.DateTimeField(default=datetime.utcnow)