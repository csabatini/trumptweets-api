from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, ForeignKey
from datetime import datetime

db = SQLAlchemy()


class BaseModel(object):
    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


# class UserProfile(db.Model, BaseModel):
#     __tablename__ = 'user_profile'
#     guid = db.Column(db.String(64), primary_key=True)
#     email = db.Column(db.String(100))
#     auth_provider = db.Column(db.String(25))
#     display_name = db.Column(db.String(100))
#     locale = db.Column(db.String(50))
#     picture = db.Column(db.String(200))
#     gender = db.Column(db.String(10))
#     last_active_time = db.Column(db.Integer)
#     device_token = db.Column(db.String(200))
#     created_time = db.Column(db.Integer)
#     last_updated_time = db.Column(db.DateTime)
#
#     def __init__(self, guid=None, email=None, auth_provider=None, display_name=None, locale=None, picture=None,
#                  gender=None, last_active_time=0, device_token=None, last_updated_time=None):
#         self.guid = guid
#         self.email = email
#         self.auth_provider = auth_provider
#         self.display_name = display_name
#         self.locale = locale
#         self.picture = picture
#         self.gender = gender
#         self.last_active_time = last_active_time
#         self.device_token = device_token
#         self.last_updated_time = last_updated_time
#
#     def as_dict(self):
#         dict = BaseModel.as_dict(self)
#         dict['change_state'] = 'NONE'
#         dict['is_verified'] = True
#         dict['device_token'] = ''
#         del dict['gender']
#         del dict['locale']
#         del dict['created_time']
#         del dict['last_updated_time']
#         return dict


class Status(db.Model, BaseModel):
    __tablename__ = 'status'
    status_id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255))
    created_at = db.Column(db.DateTime)

    def __init__(self, status_id=None, text=None, created_at=None):
        self.status_id = status_id
        self.text = text
        self.created_at = created_at

    def as_dict(self):
        epoch = datetime.utcfromtimestamp(0)
        dict = BaseModel.as_dict(self)
        dict['created_at'] = int((self.created_at - epoch).total_seconds() * 1000.0)  # millis since 1970
        return dict
