from typing import List
from mongoengine import Document, StringField
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmailField, EmbeddedDocumentListField, FloatField, ListField


class PlannerPermission(Document):
    userId = StringField(required=True, unique=True)
    plannerId = StringField(required=True)
    permissions = ListField(StringField(), default=[], required=True)

class Planner(Document):
    plannerId = StringField(required=True, unique=True)
    plannerName = StringField(required=True)
    notBefore = FloatField(required=True)
    notAfter = FloatField(required=True)
    # Default permission for all users. For an individual user, use PlannerPermission
    permissions = ListField(StringField(), default=[], required=True)

class Token(EmbeddedDocument):
    token = StringField(required=True)
    expires = FloatField(required=True)
    scopes = ListField(StringField(), default=[], required=True)
    
class User(Document):
    userId = StringField(required=True, unique=True)
    userName = StringField(required=True)
    email = EmailField()
    password = StringField()
    salt = StringField()
    # The user's time shift relative to GMT
    timeShift = FloatField(required=True)
    tokens = EmbeddedDocumentListField(Token)

class TimePreference(Document):
    userId = StringField(required=True)
    plannerId = StringField(required=True)
    notBefore = FloatField(required=True)
    notAfter = FloatField(required=True)
    status = StringField(default="available")
    # status can be available, preferred, notpreferred
