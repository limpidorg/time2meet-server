from typing import List
from mongoengine import Document, StringField
from mongoengine.document import EmbeddedDocument
from mongoengine.fields import EmailField, EmbeddedDocumentListField, FloatField, ListField


class PlannerPermission(Document):
    userId = StringField(required=True, unique=True)
    plannerId = StringField(required=True)
    permissions = ListField(StringField(), default=[])

class Planner(Document):
    plannerId = StringField(required=True, unique=True)
    plannerName = StringField(required=True)
    notBefore = FloatField(required=True)
    notAfter = FloatField(required=True)
    # Default permission for all users. For an individual user, use PlannerPermission
    permissions = ListField(StringField(), default=[])
    createdBy = StringField(required=True)
    creationTime = FloatField(required=True)

class Token(EmbeddedDocument):
    token = StringField(required=True)
    expires = FloatField(required=True)
    scopes = ListField(StringField(), default=[])


class User(Document):
    userId = StringField(required=True, unique=True)
    userName = StringField(required=True)
    email = EmailField(required=True, unique=True)
    registerationTime = FloatField(required=True)
    password = StringField(required=True)
    salt = StringField(required=True)
    # The user's time shift relative to GMT
    timeShift = FloatField(default=0)
    tokens = EmbeddedDocumentListField(Token)
    status = StringField(default='require-email-verification')


class TimePreference(Document):
    slotId = StringField(required=True, unique=True)
    userId = StringField(required=True)
    plannerId = StringField(required=True)
    notBefore = FloatField(required=True)
    notAfter = FloatField(required=True)
    status = StringField(default="available")
    # status can be available, preferred, notpreferred
