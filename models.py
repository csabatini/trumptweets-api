from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, ForeignKey
from datetime import datetime

db = SQLAlchemy()


class BaseModel(object):
    def as_dict(self):
        return {c.key: getattr(self, c.key)
                for c in inspect(self).mapper.column_attrs}


class UserProfile(db.Model, BaseModel):
    __tablename__ = 'user_profile'
    guid = db.Column(db.String(36), primary_key=True)
    push_enabled = db.Column(db.Boolean)
    device_token = db.Column(db.String(200))
    created_time = db.Column(db.DateTime)
    status_max_created_at = db.Column(db.DateTime, nullable=True, default=None)

    def __init__(self, guid=None, push_enabled=None, device_token=None, status_max_created_at=None):
        self.guid = guid
        self.push_enabled = push_enabled
        self.device_token = device_token
        self.status_max_created_at = status_max_created_at

    def as_dict(self):
        dict = BaseModel.as_dict(self)
        del dict['created_time']
        del dict['status_max_created_at']
        return dict


class Status(db.Model, BaseModel):
    __tablename__ = 'status'
    status_id = db.Column(db.String(36), primary_key=True)
    text = db.Column(db.String(255))
    media_url = db.Column(db.String(100))
    created_at = db.Column(db.DateTime)

    tags = db.relationship("StatusTag", backref="status")

    def __init__(self, status_id=None, text=None, media_url=None, created_at=None):
        self.status_id = status_id
        self.text = text
        self.media_url = media_url
        self.created_at = created_at

    def as_dict(self):
        epoch = datetime.utcfromtimestamp(0)
        dict = {}
        dict['status'] = BaseModel.as_dict(self)
        dict['status']['created_at'] = int((self.created_at - epoch).total_seconds() * 1000.0)
        dict['tags'] = [x.as_dict() for x in self.tags]
        return dict


class Tag(db.Model, BaseModel):
    __tablename__ = 'tag'
    tag_id = db.Column(db.Integer, primary_key=True)
    tag = db.Column(db.String(25))

    def __init__(self, tag_id=None, tag=None):
        self.tag_id = tag_id
        self.tag = tag


class StatusTag(db.Model, BaseModel):
    __tablename__ = 'status_tag'
    status_tag_id = db.Column(db.Integer, primary_key=True)
    status_id = db.Column(db.String(36), ForeignKey(Status.status_id))
    tag_id = db.Column(db.Integer, ForeignKey(Tag.tag_id))

    tag = db.relationship('Tag', foreign_keys='StatusTag.tag_id', lazy='joined')

    def as_dict(self):
        return self.tag.as_dict()


class TagCountMaxCreated(db.Model, BaseModel):
    __tablename__ = 'vw_tag_count_max_created'
    tag_id = db.Column(db.Integer)
    tag = db.Column(db.String(25))
    max_created_at = db.Column(db.DateTime)
    count = db.Column(db.Integer)
