from mongoengine import Document, StringField
from mongoengine.fields import EmailField, FloatField, ListField


class Planner(Document):
    plannerId = StringField(required=True, unique=True)
    plannerName = StringField(required=True)
    userIds = ListField(StringField(), default=[])

# Not using a global user account as that will complicate things. That's a feature for the future.

# class User(Document):
#     userId = StringField(required=True, unique=True)
#     userName = StringField(required=True)
#     email = EmailField()
#     password = StringField()
#     salt = StringField()
#     # The user's time shift relative to GMT
#     timeShift = FloatField(required=True)


class PlannerUser(Document):
    userId = StringField(required=True)
    plannerId = StringField(required=True)
    password = StringField()
    salt = StringField()
    # The user's time shift relative to GMT
    timeShift = FloatField(required=True)


class TimePreference(Document):
    userId = StringField(required=True)
    plannerId = StringField(required=True)
    notBefore = FloatField(required=True)
    notAfter = FloatField(required=True)
    status = StringField(default="available")
    # status can be available, preferred, notpreferred
